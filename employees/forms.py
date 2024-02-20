from django import forms
from .models import Employee, Employee_information, Department, Position, Internal_permission, External_permission, \
    DeactivationLog


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'photo': 'Employee Photo',
            'hire_date': 'Hire Date',
            'department': 'Department',
            'position': 'Position',
            'verification': 'Verification',
            'attachment': 'Attachment',
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
            'date_of_birth': 'Date of Birth',
            'email': 'Email',
            'phone_number': 'Phone Number',
            'address': 'Address',
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
            'employee': 'Employee',
            'deactivation_date': 'Deactivation Date',
            'comments': 'Comments',
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
            'employee': 'Employee',
            'permit_number': 'Permit Number',
            'permit_issue_date': 'Permit Issue Date',
            'permit_expiry_date': 'Permit Expiry Date',
            'description': 'Description',
            'tag': 'Tag',
            'attachment': 'Attachment',
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
            'employee': 'Employee',
            'permit_number': 'Permit Number',
            'permit_issue_date': 'Permit Issue Date',
            'permit_expiry_date': 'Permit Expiry Date',
            'attachment': 'Attachment',
        }
        widgets = {
            'employee': forms.HiddenInput(),
            'permit_number': forms.TextInput(attrs={'class': 'form-control'}),
            'permit_issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'permit_expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }

