from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Employee


# Create your views here.
def index (request):
    return render(request,'employees/index.html', {
        'employees': Employee.objects.all()
    })

