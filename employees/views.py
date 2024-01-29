from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Employee, Employee_information, Department, Position, Internal_permission, External_permission
from .forms import EmployeeForm


# Create your views here.
def index(request):
    sort_by = request.GET.get('sort', 'id')
    order = request.GET.get('order', 'asc')
    if order == 'desc':
        sort_by = '-' + sort_by
    employees = Employee.objects.all().order_by(sort_by)

    return render(request, 'employees/index.html', {
        'employees': employees
    })

def view_employee(request, id):
    employee = Employee.objects.get(pk=id)
    return HttpResponseRedirect(reverse('index'))

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

def edit(request, id):
    if request.method == 'POST':
        employee = Employee.objects.get(pk=id)
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return  render(request, 'employees/edit.html', {
                'form': form,
                'success': True
            })
    else:
        employee = Employee.objects.get(pk=id)
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/edit.html', {
        'form': form
    })

def delete(request, id):
    if request.method == 'POST':
        employee = Employee.objects.get(pk=id)
        employee.delete()
    return HttpResponseRedirect(reverse('index'))

