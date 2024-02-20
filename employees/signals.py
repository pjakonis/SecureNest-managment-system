from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee, Employee_information, DeactivationLog, Internal_permission, External_permission


@receiver(post_save, sender=Employee)
def create_employee_information(sender, instance, created, **kwargs):
    if created:
        Employee_information.objects.create(employee=instance)
        DeactivationLog.objects.create(employee=instance)
        # Internal_permission.objects.create(employee=instance)
        # External_permission.objects.create(employee=instance)
