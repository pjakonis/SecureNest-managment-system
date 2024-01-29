from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Employee, Department, Position, Employee_information, Internal_permission, External_permission

import datetime
from django.utils import timezone
from datetime import timedelta

admin.site.site_header = 'EMS Admin'

class EmployeeInformationInline(admin.StackedInline):
    model = Employee_information
    extra = 0

class InternalPermissionInline(admin.StackedInline):
    model = Internal_permission
    extra = 0

class ExternalPermissionInline(admin.StackedInline):
    model = External_permission
    extra = 0

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    autocomplete_fields = ['department', 'position']
    list_display = ['first_name', 'last_name', 'department', 'position', 'verification']
    list_per_page = 10
    list_editable = ['verification']
    list_filter = ['department', 'verification']
    search_fields = ['first_name__istartswith', 'last_name__istartswith', 'department__name__istartswith', 'position__name__istartswith']
    inlines = [EmployeeInformationInline, InternalPermissionInline, ExternalPermissionInline]


@admin.register(Employee_information)
class Employee_informationAdmin(admin.ModelAdmin):
    autocomplete_fields = ['employee']
    list_display = ['employee']
    list_per_page = 10
    search_fields = ['employee__first_name__istartswith', 'employee__last_name__istartswith']
    list_filter = ['city']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'number_of_employees']
    list_per_page = 10
    search_fields = ['name__istartswith']

    @admin.display(ordering='employees_count')
    def number_of_employees(self, department):
        url = (
                reverse('admin:employees_employee_changelist')
                + '?'
                + urlencode({
            'department__id': str(department.id)
        }))
        return format_html('<a href="{}">{}</a>', url, department.employees_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            employees_count=Count('employee')
        )


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_per_page = 10
    search_fields = ['name__istartswith']


class PermissionFilter(admin.SimpleListFilter):
    title = 'Permit Expiry'  # or use _('Permit Expiry') for translation
    parameter_name = 'expiry'

    def lookups(self, request, model_admin):
        return [
            ('Valid', 'Valid'),
            ('<3months', '< 3 months'),
            ('Expired', 'Expired'),
        ]

    def queryset(self, request, queryset):
        today = timezone.now().date()
        three_months_from_now = today + timedelta(days=90)
        valid = today + timedelta(days=0)

        if self.value() == '<3months':
            return queryset.filter(permit_expiry_date__gte=today, permit_expiry_date__lt=three_months_from_now)
        elif self.value() == 'Valid':
            return queryset.filter(permit_expiry_date__gte=today)
        elif self.value() == 'Expired':
            return queryset.filter(permit_expiry_date__lte=valid)

@admin.register(Internal_permission)
class Internal_permissionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['employee']
    list_display = ['employee', 'permit_number', 'tag', 'expires_in']
    list_per_page = 10
    search_fields = ['employee__first_name__startswith', 'employee__last_name__startswith', 'permit_number__startswith']
    list_filter = ['tag', PermissionFilter]

    @admin.display(ordering='permit_expiry_date')
    def expires_in(self, internal_permission):
        today = datetime.date.today()
        days_until_expiry = (internal_permission.permit_expiry_date - today).days

        if internal_permission.permit_expiry_date < today:
            return 'Expired'
        elif days_until_expiry <= 90 and days_until_expiry >= 60:
            return 'Expires in less than 3 months'
        elif days_until_expiry <= 60 and days_until_expiry >= 30:
            return 'Expires in less than 2 months'
        elif days_until_expiry <= 30 and days_until_expiry >= 14:
            return 'Expires in less than 1 month'
        elif days_until_expiry <= 14 and days_until_expiry >= 7:
            return 'Expires in less than 2 weeks'
        elif days_until_expiry <= 7 and days_until_expiry >= 2:
            return f'{days_until_expiry} days'
        elif days_until_expiry <= 2 and days_until_expiry >= 1:
            return f'{days_until_expiry} day left'
        elif days_until_expiry <= 1 and days_until_expiry >= 0:
            return f'{days_until_expiry} days left'
        else:
            return f'Valid'


@admin.register(External_permission)
class External_permissionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['employee']
    list_display = ['employee', 'permit_number', 'expires_in']
    list_per_page = 10
    search_fields = ['employee__first_name__istartswith', 'employee__last_name__istartswith', 'permit_number__istartswith']
    list_filter = [PermissionFilter]

    @admin.display(ordering='permit_expiry_date')
    def expires_in(self, external_permission):
        today = datetime.date.today()
        days_until_expiry = (external_permission.permit_expiry_date - today).days

        if external_permission.permit_expiry_date < today:
            return 'Expired'
        elif days_until_expiry <= 90 and days_until_expiry >= 60:
            return 'Expires in less than 3 months'
        elif days_until_expiry <= 60 and days_until_expiry >= 30:
            return 'Expires in less than 2 months'
        elif days_until_expiry <= 30 and days_until_expiry >= 14:
            return 'Expires in less than 1 month'
        elif days_until_expiry <= 14 and days_until_expiry >= 7:
            return 'Expires in less than 2 weeks'
        elif days_until_expiry <= 7 and days_until_expiry >= 2:
            return f'{days_until_expiry} days'
        elif days_until_expiry <= 2 and days_until_expiry >= 1:
            return f'{days_until_expiry} day left'
        elif days_until_expiry <= 1 and days_until_expiry >= 0:
            return f'{days_until_expiry} days left'
        else:
            return f'Valid'
