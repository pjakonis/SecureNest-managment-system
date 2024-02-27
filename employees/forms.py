from django import forms
from .models import Employee, Employee_information, Department, Position, Internal_permission, External_permission, \
    DeactivationLog
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.models import User



class EmployeeForm(forms.ModelForm):
    hire_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        required=False,
        label=_('Hire date')
    )
    class Meta:
        model = Employee
        fields = '__all__'
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'photo': _('Photo'),
            'hire_date': _('Hire Date'),
            'department': _('Department'),
            'position': _('Position'),
            'verification': _('Verification'),
            'attachment': _('Employment Contract'),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'verification': forms.HiddenInput(),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }


class EmployeeInformationForm(forms.ModelForm):
    class Meta:
        model = Employee_information
        fields = '__all__'
        labels = {
            'date_of_birth': _('Date of Birth'),
            'email': _('Email'),
            'phone_number': _('Phone Number'),
            'address': _('Address'),
        }
        widgets = {
            'employee': forms.HiddenInput(),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DeactivationLogForm(forms.ModelForm):
    class Meta:
        model = DeactivationLog
        fields = '__all__'
        labels = {
            'employee': _('Employee'),
            'deactivation_date': _('Deactivation Date'),
            'comments': _('Comments')
        }
        widgets = {
            'employee': forms.HiddenInput(),
            'deactivation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'comments': forms.Textarea(attrs={'class': 'form-control'}),
        }


class InternalPermissionForm(forms.ModelForm):
    class Meta:
        model = Internal_permission
        fields = '__all__'
        labels = {
            'employee': _('Employee'),
            'permit_number': _('Permit Number'),
            'permit_issue_date': _('Permit Issue Date'),
            'permit_expiry_date': _('Permit Expiration Date'),
            'description': _('Description'),
            'tag': _('Tag'),
            'attachment': _('Documents'),
        }
        widgets = {
            'employee': forms.HiddenInput(),
            'permit_number': forms.TextInput(attrs={'class': 'form-control'}),
            'permit_issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'permit_expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'tag': forms.Select(attrs={'class': 'form-control'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ExternalPermissionForm(forms.ModelForm):
    class Meta:
        model = External_permission
        fields = '__all__'
        labels = {
            'employee': _('Employee'),
            'permit_number': _('Permit Number'),
            'permit_issue_date': _('Permit Issue Date'),
            'permit_expiry_date': _('Permit Expiration Date'),
            'attachment': _('Documents'),
        }
        widgets = {
            'employee': forms.HiddenInput(),
            'permit_number': forms.TextInput(attrs={'class': 'form-control'}),
            'permit_issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'permit_expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }


class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)


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

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if new_password and new_password != confirm_new_password:
            self.add_error('confirm_new_password', "The two password fields must match.")
        return cleaned_data

