from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
                  path('', views.index, name='index'),
                  path('<int:id>', views.view_employee, name='view_employee'),
                  path('add/', views.add_employee, name='add'),
                  path('edit/<int:pk>/', views.edit_employee, name='edit_employee'),
                  path('delete/<int:pk>/', views.delete, name='delete'),
                  path('active/', views.valid_employees, name='active_employees'),
                  path('inactive/', views.inactive_employees, name='inactive_employees'),
                  path('reactivate/<int:id>/', views.reactivate_employee, name='reactivate_employee'),
                  path('add_internal_permission/<int:employee_id>/', views.add_internal_permission,
                       name='add_internal_permission'),
                  path('add_external_permission/<int:employee_id>/', views.add_external_permission,
                       name='add_external_permission'),
                  path('edit_internal_permission/<int:permission_id>/', views.edit_internal_permission,
                       name='edit_internal_permission'),
                  path('edit_external_permission/<int:permission_id>/', views.edit_external_permission,
                       name='edit_external_permission'),
                  path('employee/<int:pk>/delete_permanently/', views.delete_employee_permanently,
                       name='delete_employee_permanently'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
