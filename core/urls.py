from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from employees import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('access-denied/', views.access_denied, name='access_denied'),

    path('', views.dashboard, name='dashboard'),

    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employees/edit/<int:id>/', views.edit_employee, name='edit_employee'),
    path('employees/code/<str:employee_id>/', views.employee_detail_by_code, name='employee_detail_by_code'),
    path('employees/<int:id>/', views.employee_detail, name='employee_detail'),
    path('employee/delete/<int:id>/', views.delete_employee, name='delete_employee'),
    path('employee-pdf/<int:id>/', views.employee_pdf, name='employee_pdf'),

    path('api/employees/', views.employee_api, name='employee_api'),
    path('api/employees/<str:employee_id>/', views.employee_detail_api, name='employee_detail_api'),

    path('upload-excel/', views.upload_employee_excel, name='upload_employee_excel'),
    path('upload-excel-page/', views.upload_excel_page, name='upload_excel_page'),
    path('reports/', views.reports, name='reports'),
    path('export-excel/', views.export_employees_excel, name='export_excel'),

    path('qr-scanner/', views.qr_scanner, name='qr_scanner'),
    path('qr-scanner/decode/', views.decode_qr_code, name='decode_qr_code'),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
