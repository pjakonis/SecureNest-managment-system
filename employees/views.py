from django.http import QueryDict
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.db.models import Q, Prefetch
from django.core.mail import send_mail
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import Invitation
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import update_session_auth_hash

from .models import Employee, Employee_information, Department, Position, Internal_permission, External_permission, \
    DeactivationLog

from .forms import EmployeeForm, EmployeeInformationForm, DeactivationLogForm, InternalPermissionForm, \
    ExternalPermissionForm

from datetime import date

from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy

from django.shortcuts import render
from django.db.models import Count
from .models import Employee
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UsernameChangeForm  # We'll create this form sho
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def valid_employees(request):
    search_query = request.GET.get('q', '').strip()
    department_id = request.GET.get('department_id', None)
    department = None
    sort_by = request.GET.get('sort', 'first_name')
    order = request.GET.get('order', 'asc')

    employees = Employee.objects.filter(verification=Employee.VERIFICATION_ACTIVE)

    if department_id:
        department = get_object_or_404(Department, pk=department_id)
        employees = employees.filter(department=department)

    if search_query:
        employees = employees.filter(
            Q(first_name__istartswith=search_query) |
            Q(last_name__istartswith=search_query) |
            Q(department__name__istartswith=search_query) |
            Q(position__name__istartswith=search_query)
        )

    if order == 'desc':
        sort_by = f'-{sort_by}'
    employees = employees.order_by(sort_by)

    # Implement pagination here
    paginator = Paginator(employees, 10)  # Show 10 employees per page
    page = request.GET.get('page')
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        employees = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        employees = paginator.page(paginator.num_pages)

    return render(request, 'employees/active_employees.html', {
        'employees': employees,
        'department': department
    })




@login_required
def inactive_employees(request):
    search_query = request.GET.get('q', '').strip()
    sort_by = request.GET.get('sort', 'first_name')
    order = request.GET.get('order', 'asc')

    # Prefetch sorted internal and external permissions
    internal_permissions_prefetch = Prefetch('internal_permission_set',
                                             queryset=Internal_permission.objects.order_by('-permit_expiry_date'))
    external_permissions_prefetch = Prefetch('external_permission_set',
                                             queryset=External_permission.objects.order_by('-permit_expiry_date'))

    employees = Employee.objects.filter(
        verification=Employee.VERIFICATION_INACTIVE
    ).select_related('department').prefetch_related('employee_information', internal_permissions_prefetch,
                                                    external_permissions_prefetch)

    if search_query:
        employees = employees.filter(
            Q(first_name__istartswith=search_query) |
            Q(last_name__istartswith=search_query) |
            Q(department__name__istartswith=search_query) |
            Q(position__name__istartswith=search_query)
        )

    if order == 'desc':
        sort_by = f'-{sort_by}'
    employees = employees.order_by(sort_by)

    # Pagination
    paginator = Paginator(employees, 10)  # Show 10 employees per page
    page_number = request.GET.get('page')
    employees_paged = paginator.get_page(page_number)

    return render(request, 'employees/inactive_employees.html', {
        'employees': employees_paged,
    })


@login_required
def view_employee(request, id):
    employee = get_object_or_404(Employee, pk=id)
    employee_information = get_object_or_404(Employee_information, employee=employee)
    deactivationlog = get_object_or_404(DeactivationLog, employee=employee)
    department = employee.department
    position = employee.position

    context = {
        'employee': employee,
        'employee_information': employee_information,
        'department': department,
        'position': position,
        'deactivationlog': deactivationlog
    }
    return render(request, 'employees/view_employees.html', context)


@login_required
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            new_employee = form.save()
            return render(request, 'employees/add.html', {
                'form': EmployeeForm(),
                'success': True
            })
        else:
            return render(request, 'employees/add.html', {
                'form': form
            })
    else:
        form = EmployeeForm()
        return render(request, 'employees/add.html', {
            'form': form
        })


@login_required
def add_employee_information(request):
    if request.method == 'POST':
        form = EmployeeInformationForm(request.POST)
        if form.is_valid():
            new_employee_information = form.save()
            return render(request, 'employees/add.html', {
                'form': EmployeeInformationForm(),
                'success': True
            })
        else:
            return render(request, 'employees/add.html', {
                'form': form
            })
    else:
        form = EmployeeInformationForm()
        return render(request, 'employees/add.html', {
            'form': form
        })


@login_required
def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee_information = get_object_or_404(Employee_information, employee=employee)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        info_form = EmployeeInformationForm(request.POST, instance=employee_information)
        if form.is_valid() and info_form.is_valid():
            form.save()
            info_form.save()
            return redirect('employee_profile', id=employee.id)
    else:
        form = EmployeeForm(instance=employee)
        info_form = EmployeeInformationForm(instance=employee_information)

    return_url = request.GET.get('return_url', 'default_fallback_url')
    return render(request, 'employees/edit.html', {
        'form': form,
        'info_form': info_form,
        'employee': employee,
        'return_url': return_url
    })


@login_required
def delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    deactivationlog = get_object_or_404(DeactivationLog, employee=employee)

    if request.method == 'POST':
        form = DeactivationLogForm(request.POST, instance=deactivationlog)
        if form.is_valid():
            form.save()
            employee.verification = Employee.VERIFICATION_INACTIVE
            employee.save()
            return redirect('inactive_employees')

    form = DeactivationLogForm(instance=deactivationlog)

    return render(request, 'employees/deactivate_employee.html', {
        'form': form,
        'employee': employee
    })


@login_required
@require_POST
def reactivate_employee(request, id):
    employee = get_object_or_404(Employee, pk=id)
    employee.verification = Employee.VERIFICATION_ACTIVE
    employee.save()
    return redirect('inactive_employees')


@login_required
def index(request):
    today = date.today()
    six_months_ahead = timezone.now().date() + timedelta(days=30 * 6)

    employees_birthday_list = Employee_information.objects.filter(
        date_of_birth__month=today.month,
        employee__verification=Employee.VERIFICATION_ACTIVE
    ).select_related('employee').order_by('date_of_birth__day')
    internal_permissions_list = Internal_permission.objects.filter(
        employee__verification=Employee.VERIFICATION_ACTIVE,
        permit_expiry_date__gte=today,
        permit_expiry_date__lte=six_months_ahead
    ).select_related('employee').distinct()
    external_permissions_list = External_permission.objects.filter(
        employee__verification=Employee.VERIFICATION_ACTIVE,
        permit_expiry_date__gte=today,
        permit_expiry_date__lte=six_months_ahead
    ).select_related('employee').distinct()

    # Pagination for employees_birthday_this_month
    employees_birthday_paginator = Paginator(employees_birthday_list, 3)  # Show 10 employees per page
    employees_birthday_page = request.GET.get('employees_birthday_page')
    try:
        employees_birthday_this_month = employees_birthday_paginator.get_page(employees_birthday_page)
    except PageNotAnInteger:
        employees_birthday_this_month = employees_birthday_paginator.page(1)
    except EmptyPage:
        employees_birthday_this_month = employees_birthday_paginator.page(employees_birthday_paginator.num_pages)

    # Pagination for internal_permissions_expiring
    internal_permissions_paginator = Paginator(internal_permissions_list, 3)  # Show 10 permissions per page
    internal_permissions_page = request.GET.get('internal_permissions_page')
    try:
        internal_permissions_expiring = internal_permissions_paginator.get_page(internal_permissions_page)
    except PageNotAnInteger:
        internal_permissions_expiring = internal_permissions_paginator.page(1)
    except EmptyPage:
        internal_permissions_expiring = internal_permissions_paginator.page(internal_permissions_paginator.num_pages)

    # Pagination for external_permissions_expiring
    external_permissions_paginator = Paginator(external_permissions_list, 3)  # Show 10 permissions per page
    external_permissions_page = request.GET.get('external_permissions_page')
    try:
        external_permissions_expiring = external_permissions_paginator.get_page(external_permissions_page)
    except PageNotAnInteger:
        external_permissions_expiring = external_permissions_paginator.page(1)
    except EmptyPage:
        external_permissions_expiring = external_permissions_paginator.page(external_permissions_paginator.num_pages)

    return render(request, 'employees/index.html', {
        'employees_birthday_this_month': employees_birthday_this_month,
        'internal_permissions_expiring': internal_permissions_expiring,
        'external_permissions_expiring': external_permissions_expiring,
    })


@login_required
def add_internal_permission(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        form = InternalPermissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Internal permission added successfully.")
            return redirect('active_employees')
    else:
        form = InternalPermissionForm(initial={'employee': employee})

    # If the form is not valid, or if it's a GET request, render the page with the form.
    return render(request, 'employees/add_internal_permission.html', {
        'form': form,
        'employee': employee
    })


@login_required
def add_external_permission(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        form = ExternalPermissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "External permission added successfully.")
            return redirect('active_employees')
    else:
        form = ExternalPermissionForm(initial={'employee': employee})
    return render(request, 'employees/add_external_permission.html', {
        'form': form,
        'employee': employee
    })


@login_required
def edit_internal_permission(request, permission_id):
    permission = get_object_or_404(Internal_permission, pk=permission_id)
    if request.method == 'POST':
        form = InternalPermissionForm(request.POST, request.FILES, instance=permission)
        if form.is_valid():
            form.save()
            return redirect('active_employees')
    else:
        form = InternalPermissionForm(instance=permission)

    return render(request, 'employees/internal_permission_edit_template.html', {'form': form})


@login_required
def edit_external_permission(request, permission_id):
    permission = get_object_or_404(External_permission, pk=permission_id)
    if request.method == 'POST':
        form = ExternalPermissionForm(request.POST, request.FILES, instance=permission)
        if form.is_valid():
            form.save()
            return redirect('active_employees')
    else:
        form = ExternalPermissionForm(instance=permission)

    return render(request, 'employees/external_permission_edit_template.html', {'form': form})


@require_POST
def delete_employee_permanently(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    messages.success(request, f"The employee {employee.first_name} {employee.last_name} has been deleted permanently.")
    return redirect('inactive_employees')


@require_POST
def delete_internal_permission(request, permission_id):
    permission = get_object_or_404(Internal_permission, pk=permission_id)
    permission.delete()
    messages.success(request, 'Internal permission deleted successfully.')
    return redirect('active_employees')


@login_required
@require_POST
def delete_external_permission(request, permission_id):
    permission = get_object_or_404(External_permission, pk=permission_id)
    permission.delete()
    messages.success(request, 'External permission deleted successfully.')
    return redirect('active_employees')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    template_name_invalid = 'registration/password_reset_confirm_invalid.html'
    success_url = reverse_lazy('password_reset_complete')

    def get_template_names(self):
        """
        Return the template name to be used for the request.
        If the token is invalid, use `template_name_invalid`.
        """
        if not self.validlink:
            return [self.template_name_invalid]
        return [self.template_name]


@login_required
def create_invitation(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Check if a user with this email already exists
        if User.objects.filter(email=email).exists():
            # Customize this message as needed
            messages.error(request, 'An account with this email already exists.')
        else:
            # Expire any existing invitations for this email
            Invitation.objects.filter(email=email, is_used=False).update(is_expired=True)

            # Create a new invitation
            new_invitation = Invitation.objects.create(email=email)

            # Construct the invitation link (adjust URL as needed)
            invite_link = request.build_absolute_uri('/register/') + '?token=' + str(new_invitation.token)

            # Logic to send an email with the new invitation
            try:
                send_mail(
                    subject='Kvietimas registruotis SecureNest // Invitation to Register at SecureNest',
                    message=f'Nuoroda registracijai // Please use the following link to register: {invite_link}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,
                )
                messages.success(request, 'A new invitation has been sent successfully to ' + email)
            except Exception as e:
                messages.error(request, f'An error occurred while sending the invitation: {e}')

    return render(request, 'new_user/create_invitation.html')


def register(request):
    token = request.GET.get('token')
    # Attempt to fetch an invitation that is not expired and not used
    invitation = Invitation.objects.filter(token=token, is_expired=False, is_used=False).first()

    if not invitation or invitation.is_used:
        # If no invitation is found, or it's already been used, show the expired token page
        return render(request, 'new_user/expired_token.html')

    # Check if the invitation has expired by time
    if timezone.now() > invitation.created_at + timedelta(minutes=15):
        invitation.is_expired = True
        invitation.save()
        return render(request, 'new_user/expired_token.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        else:
            try:
                validate_password(password)
                # Assuming you want to proceed with user creation
                user = User.objects.create_user(username=username, password=password, email=invitation.email)
                # Mark the invitation as used
                invitation.is_used = True
                invitation.save()
                # Redirect or log in the user
                return redirect('login')
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)

        # If validation fails, reload the registration page with the token
        return render(request, 'new_user/register.html', {'token': token})

    # Handle GET request with token for initial registration page load
    return render(request, 'new_user/register.html', {'token': token})


@login_required
def employee_profile(request, id):
    employee = get_object_or_404(Employee, pk=id)
    # Assuming you have reverse relations set up or use related_name in models
    return render(request, 'employees/employee_profile.html', {'employee': employee})


@login_required
def departments(request):
    search_query = request.GET.get('q', '').strip()

    departments = Department.objects.all()

    if search_query:
        departments = departments.filter(name__startswith=search_query)

    # Calculate employee count for each department
    departments_with_counts = []
    for department in departments:
        employee_count = department.employee_set.filter(verification=Employee.VERIFICATION_ACTIVE).count()
        departments_with_counts.append((department, employee_count))

    context = {
        'departments': departments_with_counts,
    }
    return render(request, 'employees/departments.html', context)


@login_required
def department_employees(request, department_id):
    search_query = request.GET.get('q', '').strip()
    department = get_object_or_404(Department, pk=department_id)
    employees = Employee.objects.filter(department=department)

    if search_query:
        employees = employees.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(position__name__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(employees, 10)  # Show 10 employees per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'employees/active_employees.html', {
        'employees': page_obj,  # Pass the page object to the template
        'department': department
    })


@login_required
def user_settings(request):
    user_form = UsernameChangeForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)  # Initialize without POST data initially

    if request.method == 'POST':
        if 'change_username' in request.POST:
            user_form = UsernameChangeForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Your username was successfully updated!')
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(data=request.POST, user=request.user)  # Instantiate with POST data only here
            if password_form.is_valid():
                user = request.user
                user.set_password(password_form.cleaned_data['new_password'])
                user.save()
                update_session_auth_hash(request, user)  # Important to keep the user logged in
                messages.success(request, 'Your password was successfully updated!')

    return render(request, 'settings.html', {
        'user_form': user_form,
        'password_form': password_form
    })


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(), label="Old password")
    new_password = forms.CharField(widget=forms.PasswordInput(), label="New password")
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm new password")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not check_password(old_password, self.user.password):
            raise forms.ValidationError('Old password is incorrect.')
        return old_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        try:
            validate_password(new_password, self.user)
        except ValidationError as e:
            self.add_error('new_password', e)
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if new_password and new_password != confirm_new_password:
            self.add_error('confirm_new_password', "The two password fields must match.")
        return cleaned_data