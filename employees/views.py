from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Employee, Employee_information, Department, Position, Internal_permission, External_permission
from .forms import EmployeeForm, EmployeeInformationForm


# Create your views here.
def index(request):
    sort_by = request.GET.get('sort', 'id')
    order = request.GET.get('order', 'asc')
    if order == 'desc':
        sort_by = '-' + sort_by
    employees = Employee.objects.all().prefetch_related('employee_information').order_by(sort_by)

    return render(request, 'employees/index.html', {
        'employees': employees
    })


def view_employee(request, id):
    employee = get_object_or_404(Employee, pk=id)
    employee_information = get_object_or_404(Employee_information, employee=employee)
    department = employee.department
    position = employee.position

    context = {
        'employee': employee,
        'employee_information': employee_information,
        'department': department,
        'position': position
    }
    return render(request, 'employees/view_employee.html', context)


def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
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

def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee_information = get_object_or_404(Employee_information, employee=employee)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        info_form = EmployeeInformationForm(request.POST, instance=employee_information)
        if form.is_valid() and info_form.is_valid():
            form.save()
            info_form.save()
            return redirect('index')
    else:
        form = EmployeeForm(instance=employee)
        info_form = EmployeeInformationForm(instance=employee_information)

    return render(request, 'employees/edit.html', {
        'form': form,
        'info_form': info_form,
        'employee': employee  # Pass the employee object to the template
    })
def delete(request, id):
    if request.method == 'POST':
        employee = Employee.objects.get(pk=id)
        employee.delete()
    return HttpResponseRedirect(reverse('index'))

