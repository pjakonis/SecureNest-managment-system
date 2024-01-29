from django.db import models


# Create your models here.

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
    date_of_birth = models.DateField()
    department = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    hire_date = models.DateField(null=True)
    verification = models.CharField(max_length=1, choices=VERIFICATION_CHOICES, default=VERIFICATION_ACTIVE)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Employee_information(models.Model):
    email = models.EmailField(unique=True, null=True)
    phone_number = models.CharField(max_length=30, unique=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True)


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='employee_department')


class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='employee_position')


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

    permit_number = models.CharField(max_length=10, unique=True)
    permit_issue_date = models.DateField()
    permit_expiry_date = models.DateField()
    description = models.TextField(max_length=255)
    tag = models.CharField(max_length=2, choices=TAG_CHOICES, default=TAG_REJECTED)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)


class External_permission(models.Model):
    permit_number = models.CharField(max_length=10, unique=True)
    permit_issue_date = models.DateField()
    permit_expiry_date = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)


