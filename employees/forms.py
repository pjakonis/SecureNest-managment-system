from django import forms
from .models import Employee, Employee_information, Department, Position, Internal_permission, External_permission


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'hire_date': 'Hire Date',
            'department': 'Department',
            'position': 'Position',
            'verification': 'Verification',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'verification': forms.Select(attrs={'class': 'form-control'}),
        }


class EmployeeInformationForm(forms.ModelForm):
    class Meta:
        model = Employee_information
        fields = '__all__'
        labels = {
            'date_of_birth': 'Date of Birth',
            'email': 'Email',
            'phone_number': 'Phone Number',
            'street': 'Street',
            'city': 'City',
            'zip_code': 'Zip Code',
            'country': 'Country',
        }
        widgets = {
            'employee': forms.HiddenInput(),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }

