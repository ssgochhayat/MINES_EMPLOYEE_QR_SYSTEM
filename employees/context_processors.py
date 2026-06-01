from datetime import timedelta

from django.db.models import Count
from django.utils import timezone

from .models import Employee, EmployeeDocument


def employee_notifications(request):
    if not request.user.is_authenticated:
        return {
            'notifications': [],
            'notifications_count': 0,
        }

    if not request.user.has_perm('employees.view_employee'):
        return {
            'notifications': [],
            'notifications_count': 0,
        }

    today = timezone.localdate()
    recent_date = today - timedelta(days=7)
    recent_datetime = timezone.now() - timedelta(days=7)

    recent_employees_count = Employee.objects.filter(
        joining_date__gte=recent_date
    ).count()

    missing_documents_count = Employee.objects.annotate(
        documents_total=Count('documents')
    ).filter(documents_total=0).count()

    recent_documents_count = EmployeeDocument.objects.filter(
        uploaded_at__gte=recent_datetime
    ).count()

    missing_qr_count = (
        Employee.objects.filter(qr_code='').count() +
        Employee.objects.filter(qr_code__isnull=True).count()
    )

    notifications = []

    if recent_employees_count:
        notifications.append({
            'icon': 'fa-user-plus',
            'title': f'{recent_employees_count} recent employee record(s)',
            'message': 'Joined in the last 7 days.',
            'url': '/employees/',
            'tone': 'blue',
        })

    if missing_documents_count:
        notifications.append({
            'icon': 'fa-file-circle-exclamation',
            'title': f'{missing_documents_count} employee(s) need documents',
            'message': 'No uploaded employee documents found.',
            'url': '/employees/',
            'tone': 'orange',
        })

    if recent_documents_count:
        notifications.append({
            'icon': 'fa-file-arrow-up',
            'title': f'{recent_documents_count} document upload(s)',
            'message': 'Uploaded in the last 7 days.',
            'url': '/admin/employees/employeedocument/',
            'tone': 'green',
        })

    if missing_qr_count:
        notifications.append({
            'icon': 'fa-qrcode',
            'title': f'{missing_qr_count} employee(s) without QR code',
            'message': 'Open the employee record to regenerate.',
            'url': '/employees/',
            'tone': 'purple',
        })

    if not notifications:
        notifications.append({
            'icon': 'fa-circle-check',
            'title': 'All records look good',
            'message': 'No document or QR alerts right now.',
            'url': '/employees/',
            'tone': 'green',
        })

    return {
        'notifications': notifications[:5],
        'notifications_count': sum(
            1 for notification in notifications
            if notification['title'] != 'All records look good'
        ),
    }
