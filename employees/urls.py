from django.urls import path
from . import views
from . import views
from . import api_views
from .views import *

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('export-excel/', views.export_employees_excel, name='export_excel'),
    path('employees/', api_views.employee_list_api),
    path('employee/<str:employee_id>/', api_views.employee_detail_api),
    path('api/employees/', employee_api, name='employee_api'),
    path('api/employees/', employee_api),
path('api/employee/<str:employee_id>/', employee_detail_api),
]
                    