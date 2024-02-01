from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>', views.view_employee, name='view_employee'),
    path('add/', views.add_employee, name='add'),
    path('edit/<int:pk>/', views.edit_employee, name='edit_employee'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('active/', views.valid_employees, name='active_employees'),
    path('inactive/', views.inactive_employees, name='inactive_employees'),
    path('reactivate/<int:id>/', views.reactivate_employee, name='reactivate_employee'),

]
