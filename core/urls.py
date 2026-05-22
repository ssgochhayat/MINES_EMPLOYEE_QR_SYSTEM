from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from employees import views

urlpatterns = [

    # ADMIN

    path(
        'admin/',
        admin.site.urls
    ),

    # LOGIN

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    # LOGOUT

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # DASHBOARD

    path(
        '',
        views.dashboard,
        name='dashboard'
    ),

    # EMPLOYEE LIST

    path(
        'employees/',
        views.employee_list,
        name='employee_list'
    ),

    # ADD EMPLOYEE

    path(
        'employees/add/',
        views.add_employee,
        name='add_employee'
    ),

    # EDIT EMPLOYEE

    path(
        'employees/edit/<int:id>/',
        views.edit_employee,
        name='edit_employee'
    ),

    # EMPLOYEE DETAIL PAGE

    path(
        'employees/<int:id>/',
        views.employee_detail,
        name='employee_detail'
    ),

    # EMPLOYEE API

    path(
        'api/employees/',
        views.employee_api
    ),

    path(
        'api/employees/<str:employee_id>/',
        views.employee_detail_api
    ),

    # EXCEL UPLOAD

    path(
        'upload-excel/',
        views.upload_employee_excel,
        name='upload_excel'
    ),

    # EXPORT EXCEL

    path(
        'export-excel/',
        views.export_employees_excel,
        name='export_excel'
    ),

]

# MEDIA FILES

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)