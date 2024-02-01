from django.db import models
from django.core.validators import MinValueValidator


class Employee(models.Model):
    VERIFICATION_ACTIVE = 'A'
    VERIFICATION_INACTIVE = 'I'
    VERIFICATION_ACTIVE_NAME = 'Active'
    VERIFICATION_INACTIVE_NAME = 'Inactive'

    VERIFICATION_CHOICES = [
        (VERIFICATION_ACTIVE, VERIFICATION_ACTIVE_NAME),
        (VERIFICATION_INACTIVE, VERIFICATION_INACTIVE_NAME),
    ]

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=50)
    hire_date = models.DateField(default=None, null=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    position = models.ForeignKey('Position', on_delete=models.CASCADE)
    verification = models.CharField(max_length=1, choices=VERIFICATION_CHOICES, default=VERIFICATION_ACTIVE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['first_name']
        verbose_name_plural = 'Employees'
        verbose_name = 'Employee'


class Employee_information(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=30, unique=True, null=True, blank=True, default=None)
    street = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.employee.first_name} {self.employee.last_name}'

    class Meta:
        ordering = ['employee__first_name']
        verbose_name_plural = 'Employee information'


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Departments'
        verbose_name = 'Department'


class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Positions'
        verbose_name = 'Position'


class Internal_permission(models.Model):
    TAG_SECRET = 'S'
    TAG_CONFIDENTIAL = 'KF'
    TAG_RESTRICTED = 'RN'
    TAG_REJECTED = 'N'
    TAG_SECRET_NAME = 'Secret'
    TAG_CONFIDENTIAL_NAME = 'Confidential'
    TAG_RESTRICTED_NAME = 'Restricted'
    TAG_REJECTED_NAME = 'Rejected'

    TAG_CHOICES = [
        (TAG_SECRET, TAG_SECRET_NAME),
        (TAG_CONFIDENTIAL, TAG_CONFIDENTIAL_NAME),
        (TAG_RESTRICTED, TAG_RESTRICTED_NAME),
        (TAG_REJECTED, TAG_REJECTED_NAME),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    permit_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    permit_issue_date = models.DateField(null=True, blank=True)
    permit_expiry_date = models.DateField(null=True, blank=True)
    description = models.TextField(max_length=255, null=True, blank=True)
    tag = models.CharField(max_length=2, choices=TAG_CHOICES, default=TAG_REJECTED)

    def __str__(self):
        return f'{self.employee.first_name} {self.employee.last_name} {self.permit_number}'

    class Meta:
        ordering = ['employee__first_name']
        verbose_name_plural = 'Internal permissions'
        verbose_name = 'Internal permission'


class External_permission(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    permit_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    permit_issue_date = models.DateField(null=True, blank=True)
    permit_expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.employee.first_name} {self.employee.last_name} {self.permit_number}'

    class Meta:
        ordering = ['employee__first_name']
        verbose_name_plural = 'External permissions'
        verbose_name = 'External permission'

