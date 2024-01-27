from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Employee
from .forms import EmployeeForm



# Create your views here.
def index (request):
    return render(request,'employees/index.html', {
        'employees': Employee.objects.all()
    })

def view_employee(request, id):
    employee = Employee.objects.get(pk=id)
    return HttpResponseRedirect(reverse('index'))

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            # Form processing and saving new employee
            new_employee = form.save()
            # Redirecting to the index page or showing success message
            # If you want to redirect:
            # return HttpResponseRedirect(reverse('index'))
            return render(request, 'employees/add.html', {
                'form': EmployeeForm(),  # Initializing a new blank form
                'success': True
            })
        else:
            # If the form is not valid, render the page with the form containing errors
            return render(request, 'employees/add.html', {
                'form': form
            })
    else:
        # Initializing a blank form for GET requests
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