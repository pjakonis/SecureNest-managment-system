from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Employee



# Create your views here.
def index (request):
    return render(request,'employees/index.html', {
        'employees': Employee.objects.all()
    })

def view_employee(request, id):
    employee = Employee.objects.get(pk=id)
    return HttpResponseRedirect(reverse('index'))