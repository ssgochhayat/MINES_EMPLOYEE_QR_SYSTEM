from django.contrib import admin

from .models import Employee
from .models import EmployeeDocument


class EmployeeDocumentInline(admin.TabularInline):

    model = EmployeeDocument

    extra = 3

    fields = ('file',)

    verbose_name = "Employee Document"

    verbose_name_plural = "Employee Documents"


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        'employee_id',
        'name',
        'department',
        'designation',
        'mobile',
        'joining_date'
    )

    search_fields = (
        'employee_id',
        'name',
        'department'
    )

    list_filter = (
        'department',
        'joining_date'
    )

    inlines = [
        EmployeeDocumentInline
    ]


@admin.register(EmployeeDocument)
class EmployeeDocumentAdmin(admin.ModelAdmin):

    list_display = (
        'employee',
        'file',
        'uploaded_at'
    )
admin.site.site_header = "GVPR Employee Log In"

admin.site.site_title = "GVPR Admin Portal"

admin.site.index_title = "Welcome to GVPR Employee Management System"