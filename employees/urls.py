from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetConfirmView, delete_external_permission, delete_internal_permission, \
    create_invitation, register

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
                  path('delete_internal_permission/<int:permission_id>/', delete_internal_permission,
                       name='delete_internal_permission'),
                  path('delete_external_permission/<int:permission_id>/', delete_external_permission,
                       name='delete_external_permission'),
                  path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('password_reset/',
                       auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
                       name='password_reset'),
                  path('password_reset/done/',
                       auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
                       name='password_reset_done'),
                  path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
                       name='password_reset_confirm'),
                  path('create_invitation/', create_invitation, name='create_invitation'),
                  path('register/', register, name='register'),
                  path('expired_token/', register, name='expired_token'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
