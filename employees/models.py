from django.db import models

# Create your models here.

class Employee(models.Model):
    employee_number = models.PositiveIntegerField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    department = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    phone_number = models.CharField(max_length=30)
    address = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
