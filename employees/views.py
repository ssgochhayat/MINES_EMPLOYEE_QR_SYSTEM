from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from openpyxl import Workbook
from datetime import date

from .models import Employee, EmployeeDocument
from .forms import EmployeeForm


def dashboard(request):

    total_employees = Employee.objects.count()

    return render(request, 'dashboard.html', {
        'total_employees': total_employees
    })


def employee_list(request):

    employees = Employee.objects.all()

    today = date.today().isoformat()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date', today)

    if start_date and end_date:
        employees = employees.filter(
            joining_date__range=[start_date, end_date]
        )

    return render(request, 'employees/employee_list.html', {
        'employees': employees,
        'today': today
    })


def add_employee(request):

    if request.method == 'POST':

        form = EmployeeForm(
            request.POST,
            request.FILES
        )

        files = request.FILES.getlist('documents')

        if form.is_valid():

            employee = form.save()

            for file in files:

                EmployeeDocument.objects.create(
                    employee=employee,
                    document_name=file.name,
                    file=file
                )

            return redirect('employee_list')

    else:

        form = EmployeeForm()

    return render(
        request,
        'employees/employee_form.html',
        {
            'form': form
        }
    )


def employee_api(request):

    employees = Employee.objects.all()

    data = []

    for employee in employees:

        documents = []

        for doc in employee.documents.all():

            documents.append({
                'document_name': doc.document_name,
                'file': request.build_absolute_uri(doc.file.url)
            })

        data.append({

            'employee_id': employee.employee_id,
            'name': employee.name,
            'department': employee.department,
            'designation': employee.designation,
            'mobile': employee.mobile,
            'joining_date': str(employee.joining_date),

            'photo': request.build_absolute_uri(employee.photo.url)
            if employee.photo else '',

            'qr_code': request.build_absolute_uri(employee.qr_code.url)
            if employee.qr_code else '',

            'documents': documents
        })

    return JsonResponse(data, safe=False)


def employee_detail_api(request, employee_id):

    employee = Employee.objects.get(employee_id=employee_id)

    documents = []

    for doc in employee.documents.all():

        documents.append({
            'document_name': doc.document_name,
            'file': request.build_absolute_uri(doc.file.url)
        })

    data = {

        'employee_id': employee.employee_id,
        'name': employee.name,
        'department': employee.department,
        'designation': employee.designation,
        'mobile': employee.mobile,
        'joining_date': str(employee.joining_date),

        'photo': request.build_absolute_uri(employee.photo.url)
        if employee.photo else '',

        'qr_code': request.build_absolute_uri(employee.qr_code.url)
        if employee.qr_code else '',

        'documents': documents
    }

    return JsonResponse(data)


def export_employees_excel(request):

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    employees = Employee.objects.all()

    if start_date and end_date:
        employees = employees.filter(
            joining_date__range=[start_date, end_date]
        )

    workbook = Workbook()

    worksheet = workbook.active
    worksheet.title = 'Employees'

    headers = [
        'Employee ID',
        'Name',
        'Department',
        'Designation',
        'Mobile',
        'Joining Date'
    ]

    worksheet.append(headers)

    for employee in employees:

        worksheet.append([
            employee.employee_id,
            employee.name,
            employee.department,
            employee.designation,
            employee.mobile,
            str(employee.joining_date)
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = 'attachment; filename=employees.xlsx'

    workbook.save(response)

    return response