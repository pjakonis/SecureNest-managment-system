import uuid

from django.db import models
from django.core.validators import MinValueValidator
from datetime import date, timedelta
from django.utils.translation import gettext_lazy as _
from PIL import Image
from django.db import models
from django.utils import timezone
from datetime import timedelta, date


class Employee(models.Model):
    VERIFICATION_ACTIVE = _('A')
    VERIFICATION_INACTIVE = _('I')
    VERIFICATION_ACTIVE_NAME = _('Active')
    VERIFICATION_INACTIVE_NAME = _('Inactive')

    VERIFICATION_CHOICES = [
        (VERIFICATION_ACTIVE, VERIFICATION_ACTIVE_NAME),
        (VERIFICATION_INACTIVE, VERIFICATION_INACTIVE_NAME),
    ]

    first_name = models.CharField(max_length=25, verbose_name=_('First name'))
    last_name = models.CharField(max_length=50, verbose_name=_('Last name'))
    photo = models.ImageField(upload_to='employee_photos/', default='default_photo.jpg', blank=True, null=True, verbose_name=_('Photo'))
    hire_date = models.DateField(default=None, null=True, verbose_name=_('Hire date'))
    department = models.ForeignKey('Department', on_delete=models.CASCADE, verbose_name=_('Department'))
    position = models.ForeignKey('Position', on_delete=models.CASCADE, verbose_name=_('Position'))
    verification = models.CharField(max_length=1, choices=VERIFICATION_CHOICES, default=VERIFICATION_ACTIVE, verbose_name=_('Verification'))
    attachment = models.FileField(upload_to='employees/', null=True, blank=True, verbose_name=_('Attachment'))

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['first_name']
        verbose_name_plural = _('Employees')
        verbose_name = _('Employee')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.photo:
            img = Image.open(self.photo.path)

            # Using Image.Resampling.LANCZOS for high-quality downsampling
            img.thumbnail((300, 300), Image.Resampling.LANCZOS)

            # Check if the image needs to be cropped to 300x300
            img_width, img_height = img.size
            if img_width > 300 or img_height > 300:
                left = (img_width - 300) / 2
                top = (img_height - 300) / 2
                right = (img_width + 300) / 2
                bottom = (img_height + 300) / 2
                img = img.crop((left, top, right, bottom))

            img.save(self.photo.path)


class Employee_information(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True, verbose_name=_('Employee'))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('Date of birth'))
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name=_('Email'))
    phone_number = models.CharField(max_length=30, unique=True, null=True, blank=True, default=None, verbose_name=_('Phone number'))
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Address'))

    def __str__(self):
        return f'{self.employee.first_name} {self.employee.last_name}'

    class Meta:
        ordering = ['employee__first_name']
        verbose_name_plural = _('Employee information')

    def is_birthday_today(self):
        return self.date_of_birth.month == date.today().month and \
            self.date_of_birth.day == date.today().day


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = _('Departments')
        verbose_name = _('Department')


class Position(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = _('Positions')
        verbose_name = _('Position')


class Internal_permission(models.Model):
    TAG_SECRET = _('S')
    TAG_CONFIDENTIAL = _('C')
    TAG_RESTRICTED = _('R')
    TAG_REJECTED = _('X')
    TAG_SECRET_NAME = _('Secret')
    TAG_CONFIDENTIAL_NAME = _('Confidential')
    TAG_RESTRICTED_NAME = _('Restricted')
    TAG_REJECTED_NAME = _('Rejected')

    TAG_CHOICES = [
        (TAG_SECRET, TAG_SECRET_NAME),
        (TAG_CONFIDENTIAL, TAG_CONFIDENTIAL_NAME),
        (TAG_RESTRICTED, TAG_RESTRICTED_NAME),
        (TAG_REJECTED, TAG_REJECTED_NAME),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_('Employee'))
    permit_number = models.CharField(max_length=10, unique=True, null=True, blank=True, verbose_name=_('Permit number'))
    permit_issue_date = models.DateField(null=True, blank=True, verbose_name=_('Permit issue date'))
    permit_expiry_date = models.DateField(null=True, blank=True, verbose_name=_('Permit expiry date'))
    description = models.TextField(max_length=255, null=True, blank=True, verbose_name=_('Description'))
    tag = models.CharField(max_length=2, choices=TAG_CHOICES, default=TAG_REJECTED, verbose_name=_('Tag'))
    attachment = models.FileField(upload_to='internal_permissions/', null=True, blank=True, verbose_name=_('Attachment'))

    @property
    def is_expiring_or_expired(self):
        today = timezone.now().date()
        six_months_ahead = today + timedelta(days=30 * 6)
        if self.permit_expiry_date < today:
            return _('expired')
        elif self.permit_expiry_date <= six_months_ahead:
            return _('expiring')
        else:
            return _('active')

    def __str__(self):
        return f'{self.employee.first_name} {self.employee.last_name} {self.permit_number}'

    class Meta:
        ordering = ['employee__first_name']
        verbose_name_plural = _('Internal permissions')
        verbose_name = _('Internal permission')


class External_permission(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_('Employee'))
    permit_number = models.CharField(max_length=10, unique=True, null=True, blank=True, verbose_name=_('Permit number'))
    permit_issue_date = models.DateField(null=True, blank=True, verbose_name=_('Permit issue date'))
    permit_expiry_date = models.DateField(null=True, blank=True, verbose_name=_('Permit expiry date'))
    attachment = models.FileField(upload_to='external_permissions/', null=True, blank=True, verbose_name=_('Attachment'))

    @property
    def is_expiring_or_expired(self):
        today = timezone.now().date()
        six_months_ahead = today + timedelta(days=30 * 6)
        if self.permit_expiry_date < today:
            return _('expired')
        elif self.permit_expiry_date <= six_months_ahead:
            return _('expiring')
        else:
            return _('active')

    def __str__(self):
        return f'{self.employee.first_name} {self.employee.last_name} {self.permit_number}'

    class Meta:
        ordering = ['employee__first_name']
        verbose_name_plural = _('External permissions')
        verbose_name = _('External permission')


class DeactivationLog(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True, verbose_name=_('Employee'))
    deactivation_date = models.DateField(null=True, blank=True, verbose_name=_('Deactivation date'))
    comments = models.TextField(null=True, blank=True, verbose_name=_('Comments'))

    def __str__(self):
        return f'{self.employee.first_name} {self.employee.last_name}'


class Invitation(models.Model):
    email = models.EmailField(unique=False, verbose_name=_('Email'))
    token = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name=_('Token'))
    is_used = models.BooleanField(default=False, verbose_name=_('Is used'))
    is_expired = models.BooleanField(default=False, verbose_name=_('Is expired'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    def __str__(self):
        return self.email
