from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Permission, User
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from .models import Employee, EmployeeDocument


ACCESS_PERMISSION_FIELDS = (
    ('can_view_dashboard', 'employees.view_dashboard'),
    ('can_view_employees', 'employees.view_employee'),
    ('can_add_employees', 'employees.add_employee'),
    ('can_edit_employees', 'employees.change_employee'),
    ('can_delete_employees', 'employees.delete_employee'),
    ('can_upload_excel', 'employees.import_employee_excel'),
    ('can_export_excel', 'employees.export_employee_excel'),
    ('can_use_qr_scanner', 'employees.scan_employee_qr'),
)


class UserAccessForm(UserChangeForm):
    can_view_dashboard = forms.BooleanField(
        label='Dashboard',
        required=False,
        help_text='Allow this user to open the dashboard page.'
    )
    can_view_employees = forms.BooleanField(
        label='View Employees',
        required=False,
        help_text='Allow employee list and employee detail pages.'
    )
    can_add_employees = forms.BooleanField(
        label='Add Employee',
        required=False,
        help_text='Allow creating new employee records.'
    )
    can_edit_employees = forms.BooleanField(
        label='Edit Employee',
        required=False,
        help_text='Allow editing employee records.'
    )
    can_delete_employees = forms.BooleanField(
        label='Delete Employee',
        required=False,
        help_text='Allow deleting employee records.'
    )
    can_upload_excel = forms.BooleanField(
        label='Upload Excel',
        required=False,
        help_text='Allow importing employee data from Excel.'
    )
    can_export_excel = forms.BooleanField(
        label='Export Excel / Reports',
        required=False,
        help_text='Allow downloading employee Excel reports.'
    )
    can_use_qr_scanner = forms.BooleanField(
        label='QR Scanner',
        required=False,
        help_text='Allow using the web QR scanner.'
    )

    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = self.instance

        if user and user.pk:
            for field_name, permission in ACCESS_PERMISSION_FIELDS:
                self.fields[field_name].initial = user.has_perm(permission)

    def save_access_permissions(self):
        user = self.instance

        if not user or not user.pk:
            return

        permissions = Permission.objects.filter(
            content_type__app_label='employees',
            codename__in=[
                permission.split('.', 1)[1]
                for _, permission in ACCESS_PERMISSION_FIELDS
            ]
        )
        permissions_by_codename = {
            permission.codename: permission
            for permission in permissions
        }

        for field_name, permission in ACCESS_PERMISSION_FIELDS:
            codename = permission.split('.', 1)[1]
            permission_obj = permissions_by_codename.get(codename)

            if not permission_obj:
                continue

            if self.cleaned_data.get(field_name):
                user.user_permissions.add(permission_obj)
            else:
                user.user_permissions.remove(permission_obj)


class EmployeeDocumentInline(admin.TabularInline):
    model = EmployeeDocument
    extra = 0
    fields = ('document_name', 'file', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
    show_change_link = True


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'employee_id',
        'name',
        'department',
        'designation',
        'mobile',
        'joining_date',
        'documents_count',
        'photo_preview',
        'qr_preview',
        'main_page_button',
    )
    search_fields = (
        'employee_id',
        'name',
        'department',
        'designation',
        'mobile',
        'aadhaar',
        'pan',
        'uan',
    )
    list_filter = (
        'department',
        'designation',
        'gender',
        'category',
        'employment_type',
        'joining_date',
    )
    readonly_fields = (
        'main_page_button',
        'photo_preview_large',
        'signature_preview',
        'qr_preview_large',
    )
    ordering = ('-joining_date', '-id')
    date_hierarchy = 'joining_date'
    list_per_page = 20
    list_select_related = ()
    save_on_top = True
    inlines = [EmployeeDocumentInline]

    fieldsets = (
        ('Main Website Shortcut', {
            'description': 'Open the public employee profile exactly as normal users see it.',
            'fields': (
                'main_page_button',
            )
        }),
        ('Basic Information', {
            'fields': (
                ('employee_id', 'name'),
                ('gender', 'father_spouse_name'),
                ('dob', 'place_of_birth'),
                ('nationality', 'education_level'),
                ('department', 'designation'),
                ('category', 'employment_type'),
                ('joining_date', 'mobile'),
            )
        }),
        ('Government Information', {
            'classes': ('collapse',),
            'fields': (
                ('uan', 'pan'),
                ('aadhaar', 'esic_ip'),
                'eps_nps',
            )
        }),
        ('Employment Information', {
            'classes': ('collapse',),
            'fields': (
                'posting_details',
                'pay',
                'promotion',
                'family_details',
                'service_book_no',
            )
        }),
        ('Bank Details', {
            'classes': ('collapse',),
            'fields': (
                ('bank_account_no', 'bank_name'),
                'ifsc',
            )
        }),
        ('Address Information', {
            'fields': (
                'present_address',
                'permanent_address',
            )
        }),
        ('Nominee Information', {
            'classes': ('collapse',),
            'fields': (
                'nominee_name',
            )
        }),
        ('Identification', {
            'classes': ('collapse',),
            'fields': (
                'identification_mark',
                'remarks',
            )
        }),
        ('Documents', {
            'classes': ('collapse',),
            'fields': (
                'joining_letter',
                'appointment_letter',
            )
        }),
        ('Images and QR Code', {
            'fields': (
                'photo',
                'photo_preview_large',
                'signature',
                'signature_preview',
                'qr_code',
                'qr_preview_large',
            )
        }),
        ('Exit Information', {
            'classes': ('collapse',),
            'fields': (
                'exit_date',
                'exit_reason',
            )
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            documents_total=Count('documents')
        )

    @admin.display(description='Docs', ordering='documents_total')
    def documents_count(self, obj):
        return getattr(obj, 'documents_total', obj.documents.count())

    @admin.display(description='Main Page')
    def main_page_button(self, obj):
        if not obj or not obj.pk:
            return 'Save this employee first'

        return format_html(
            '<a class="admin-main-link" href="{}">Open Main Page</a>',
            reverse('employee_detail', args=[obj.pk])
        )

    @admin.display(description='Photo')
    def photo_preview(self, obj):
        if not obj.photo:
            return '-'

        return format_html(
            '<img src="{}" width="45" height="45" style="object-fit:cover;border-radius:50%;" />',
            obj.photo.url
        )

    @admin.display(description='Photo Preview')
    def photo_preview_large(self, obj):
        if not obj.photo:
            return 'No photo'

        return format_html(
            '<img src="{}" width="140" style="border-radius:12px;border:1px solid #ddd;" />',
            obj.photo.url
        )

    @admin.display(description='Signature Preview')
    def signature_preview(self, obj):
        if not obj.signature:
            return 'No signature'

        return format_html(
            '<img src="{}" width="180" style="background:white;padding:10px;border:1px solid #ddd;" />',
            obj.signature.url
        )

    @admin.display(description='QR')
    def qr_preview(self, obj):
        if not obj.qr_code:
            return '-'

        return format_html(
            '<img src="{}" width="45" height="45" />',
            obj.qr_code.url
        )

    @admin.display(description='QR Preview')
    def qr_preview_large(self, obj):
        if not obj.qr_code:
            return 'No QR code'

        return format_html(
            '<img src="{}" width="150" />',
            obj.qr_code.url
        )


@admin.register(EmployeeDocument)
class EmployeeDocumentAdmin(admin.ModelAdmin):
    list_display = (
        'employee',
        'document_name',
        'file',
        'uploaded_at',
    )
    autocomplete_fields = ('employee',)
    ordering = ('-uploaded_at',)
    list_select_related = ('employee',)
    search_fields = (
        'employee__name',
        'employee__employee_id',
        'document_name',
    )
    list_filter = ('uploaded_at',)
    list_per_page = 25


admin.site.site_header = 'GVPR Employee Management System'
admin.site.site_title = 'GVPR Admin'
admin.site.index_title = 'Admin Dashboard'
admin.site.site_url = '/'


admin.site.unregister(User)


@admin.register(User)
class UserAccessAdmin(DefaultUserAdmin):
    form = UserAccessForm
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'is_superuser',
    )
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'groups',
    )
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
    )
    filter_horizontal = ('groups',)
    ordering = ('username',)
    save_on_top = True
    readonly_fields = ('last_login', 'date_joined', 'main_page_button')
    fieldsets = (
        ('Main Website Shortcut', {
            'fields': (
                'main_page_button',
            )
        }),
        ('Login Details', {
            'fields': (
                'username',
                'password',
            )
        }),
        ('Personal Information', {
            'fields': (
                ('first_name', 'last_name'),
                'email',
            )
        }),
        ('Account Status', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
        ('Main Webpage Access', {
            'description': (
                'Tick only the pages and actions this user can access. '
                'The main website menu and direct page access will follow these choices automatically.'
            ),
            'fields': (
                ('can_view_dashboard', 'can_view_employees'),
                ('can_add_employees', 'can_edit_employees'),
                ('can_delete_employees', 'can_use_qr_scanner'),
                ('can_upload_excel', 'can_export_excel'),
            )
        }),
        ('Groups', {
            'classes': ('collapse',),
            'description': (
                'Optional: use groups for role-based access. The simple checkboxes above are best for most users.'
            ),
            'fields': (
                'groups',
            )
        }),
        ('Important Dates', {
            'classes': ('collapse',),
            'fields': (
                'last_login',
                'date_joined',
            )
        }),
    )

    @admin.display(description='Main Page')
    def main_page_button(self, obj):
        return format_html(
            '<a class="admin-main-link" href="{}">Open Main Website</a>',
            reverse('dashboard')
        )

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        if hasattr(form, 'save_access_permissions'):
            form.save_access_permissions()


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'codename',
        'content_type',
    )
    search_fields = (
        'name',
        'codename',
        'content_type__app_label',
        'content_type__model',
    )
    list_filter = (
        'content_type__app_label',
        'content_type__model',
    )
