from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from openpyxl import Workbook
from datetime import date
import pandas as pd

from .models import Employee, EmployeeDocument
from .forms import EmployeeForm


# LOGIN

def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    error = ''

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        # ONLY ADMIN LOGIN

        if user is not None and user.is_staff:

            login(request, user)

            return redirect('dashboard')

        else:

            error = 'Only Admin Can Login'

    return render(request, 'login.html', {
        'error': error
    })


# LOGOUT

def logout_view(request):

    logout(request)

    return redirect('login')


# DASHBOARD

@login_required(login_url='login')
def dashboard(request):

    employees = Employee.objects.all().order_by('-id')

    total_employees = Employee.objects.count()

    departments_count = Employee.objects.values(
        'department'
    ).distinct().count()

    documents_count = EmployeeDocument.objects.count()

    context = {

        'employees': employees,

        'total_employees': total_employees,

        'departments_count': departments_count,

        'documents_count': documents_count,

    }

    return render(
        request,
        'dashboard.html',
        context
    )


# EMPLOYEE LIST + SEARCH

@login_required(login_url='login')
def employee_list(request):

    employees = Employee.objects.all().order_by('-id')

    today = date.today().isoformat()

    # SEARCH

    search = request.GET.get('search')

    if search:

        employees = employees.filter(
            name__icontains=search
        ) | employees.filter(
            employee_id__icontains=search
        ) | employees.filter(
            department__icontains=search
        ) | employees.filter(
            designation__icontains=search
        ) | employees.filter(
            mobile__icontains=search
        )

    # DATE FILTER

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


# ADD EMPLOYEE

@login_required(login_url='login')
def add_employee(request):

    if request.method == 'POST':

        form = EmployeeForm(
            request.POST,
            request.FILES
        )

        files = request.FILES.getlist('documents')

        if form.is_valid():

            employee = form.save()

            # SAVE MULTIPLE DOCUMENTS

            for file in files:

                EmployeeDocument.objects.create(
                    employee=employee,
                    document_name=file.name,
                    file=file
                )

            return redirect(
                'employee_detail',
                id=employee.id
            )

        else:

            print(form.errors)

    else:

        form = EmployeeForm()

    return render(
        request,
        'employees/employee_form.html',
        {
            'form': form
        }
    )

    if request.method == 'POST':

        form = EmployeeForm(
            request.POST,
            request.FILES
        )

        files = request.FILES.getlist('documents')

        if form.is_valid():

            employee = form.save()

            # MULTIPLE DOCUMENT SAVE

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

# EDIT EMPLOYEE

@login_required(login_url='login')
# EDIT EMPLOYEE

@login_required(login_url='login')
def edit_employee(request, id):

    employee = Employee.objects.get(id=id)

    if request.method == 'POST':

        form = EmployeeForm(
            request.POST,
            request.FILES,
            instance=employee
        )

        if form.is_valid():

            updated_employee = form.save()

            # SAVE NEW DOCUMENTS

            files = request.FILES.getlist('documents')

            for file in files:

                EmployeeDocument.objects.create(
                    employee=updated_employee,
                    document_name=file.name,
                    file=file
                )

            return redirect(
                'employee_detail',
                id=updated_employee.id
            )

        else:

            print(form.errors)

    else:

        form = EmployeeForm(instance=employee)

    return render(
        request,
        'employees/employee_form.html',
        {
            'form': form,
            'employee': employee,
            'edit_mode': True
        }
    )

    employee = Employee.objects.get(id=id)

    if request.method == 'POST':

        form = EmployeeForm(
            request.POST,
            request.FILES,
            instance=employee
        )

        files = request.FILES.getlist('documents')

        if form.is_valid():

            employee = form.save()

            # SAVE NEW DOCUMENTS

            for file in files:

                EmployeeDocument.objects.create(
                    employee=employee,
                    document_name=file.name,
                    file=file
                )

            return redirect(
                'employee_detail',
                id=employee.id
            )

        else:

            print(form.errors)

    else:

        form = EmployeeForm(instance=employee)

    return render(
        request,
        'employees/employee_form.html',
        {
            'form': form,
            'employee': employee,
            'edit_mode': True
        }
    )

    employee = Employee.objects.get(id=id)

    if request.method == 'POST':

        form = EmployeeForm(
            request.POST,
            request.FILES,
            instance=employee
        )

        files = request.FILES.getlist('documents')

        if form.is_valid():

            employee = form.save()

            # SAVE NEW DOCUMENTS

            for file in files:

                EmployeeDocument.objects.create(
                    employee=employee,
                    document_name=file.name,
                    file=file
                )

            return redirect(
                'employee_detail',
                id=employee.id
            )

    else:

        # PREFILLED FORM

        form = EmployeeForm(
            instance=employee
        )

    return render(
        request,
        'employees/employee_form.html',
        {
            'form': form,
            'employee': employee,
            'edit_mode': True
        }
    )

# EMPLOYEE API

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

            # BASIC DETAILS

            'employee_id': employee.employee_id,
            'employee_register_no': employee.employee_register_no,
            'name': employee.name,
            'gender': employee.gender,
            'father_spouse_name': employee.father_spouse_name,
            'dob': str(employee.dob) if employee.dob else '',
            'nationality': employee.nationality,
            'education_level': employee.education_level,
            'department': employee.department,
            'designation': employee.designation,
            'category': employee.category,
            'employment_type': employee.employment_type,
            'mobile': employee.mobile,
            'joining_date': str(employee.joining_date),

            # GOVERNMENT DETAILS

            'uan': employee.uan,
            'pan': employee.pan,
            'esic_ip': employee.esic_ip,
            'lwf': employee.lwf,
            'aadhaar': employee.aadhaar,

            # BANK DETAILS

            'bank_account_no': employee.bank_account_no,
            'bank_name': employee.bank_name,
            'ifsc': employee.ifsc,

            # ADDRESS

            'present_address': employee.present_address,
            'permanent_address': employee.permanent_address,

            # EXIT DETAILS

            'service_book_no': employee.service_book_no,
            'exit_date': str(employee.exit_date) if employee.exit_date else '',
            'exit_reason': employee.exit_reason,

            # IDENTIFICATION

            'identification_mark': employee.identification_mark,
            'remarks': employee.remarks,

            # PART B

            'owner_name': employee.owner_name,
            'token_number': employee.token_number,
            'first_appointment_date': str(employee.first_appointment_date)
            if employee.first_appointment_date else '',

            'age_fitness_certificate': employee.age_fitness_certificate,
            'place_of_employment': employee.place_of_employment,
            'vocational_training_number': employee.vocational_training_number,

            'vocational_training_date': str(employee.vocational_training_date)
            if employee.vocational_training_date else '',

            'nominee_name': employee.nominee_name,
            'nominee_address': employee.nominee_address,

            'emergency_contact_name': employee.emergency_contact_name,
            'emergency_contact_address': employee.emergency_contact_address,
            'emergency_mobile': employee.emergency_mobile,

            # IMAGES

            'photo': request.build_absolute_uri(employee.photo.url)
            if employee.photo else '',

            'signature': request.build_absolute_uri(employee.signature.url)
            if employee.signature else '',

            'qr_code': request.build_absolute_uri(employee.qr_code.url)
            if employee.qr_code else '',

            # DOCUMENTS

            'joining_letter': request.build_absolute_uri(employee.joining_letter.url)
            if employee.joining_letter else '',

            'appointment_letter': request.build_absolute_uri(employee.appointment_letter.url)
            if employee.appointment_letter else '',

            'documents': documents

        })

    return JsonResponse(data, safe=False)


# EMPLOYEE DETAIL API

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
        'employee_register_no': employee.employee_register_no,
        'name': employee.name,
        'gender': employee.gender,
        'father_spouse_name': employee.father_spouse_name,
        'dob': str(employee.dob) if employee.dob else '',
        'nationality': employee.nationality,
        'education_level': employee.education_level,
        'department': employee.department,
        'designation': employee.designation,
        'category': employee.category,
        'employment_type': employee.employment_type,
        'mobile': employee.mobile,
        'joining_date': str(employee.joining_date),

        'uan': employee.uan,
        'pan': employee.pan,
        'esic_ip': employee.esic_ip,
        'lwf': employee.lwf,
        'aadhaar': employee.aadhaar,

        'bank_account_no': employee.bank_account_no,
        'bank_name': employee.bank_name,
        'ifsc': employee.ifsc,

        'present_address': employee.present_address,
        'permanent_address': employee.permanent_address,

        'service_book_no': employee.service_book_no,
        'exit_date': str(employee.exit_date) if employee.exit_date else '',
        'exit_reason': employee.exit_reason,

        'identification_mark': employee.identification_mark,
        'remarks': employee.remarks,

        'owner_name': employee.owner_name,
        'token_number': employee.token_number,

        'first_appointment_date': str(employee.first_appointment_date)
        if employee.first_appointment_date else '',

        'age_fitness_certificate': employee.age_fitness_certificate,
        'place_of_employment': employee.place_of_employment,
        'vocational_training_number': employee.vocational_training_number,

        'vocational_training_date': str(employee.vocational_training_date)
        if employee.vocational_training_date else '',

        'nominee_name': employee.nominee_name,
        'nominee_address': employee.nominee_address,

        'emergency_contact_name': employee.emergency_contact_name,
        'emergency_contact_address': employee.emergency_contact_address,
        'emergency_mobile': employee.emergency_mobile,

        'photo': request.build_absolute_uri(employee.photo.url)
        if employee.photo else '',

        'signature': request.build_absolute_uri(employee.signature.url)
        if employee.signature else '',

        'qr_code': request.build_absolute_uri(employee.qr_code.url)
        if employee.qr_code else '',

        'documents': documents

    }

    return JsonResponse(data)


# UPLOAD EXCEL

@login_required(login_url='login')
def upload_employee_excel(request):

    if request.method == "POST":

        excel_file = request.FILES.get("file")

        if not excel_file:

            return JsonResponse({
                "error": "No file uploaded"
            }, status=400)

        try:

            df = pd.read_excel(excel_file)

            created = 0
            skipped = 0

            for _, row in df.iterrows():

                try:

                    emp_id = str(
                        row.get("employee_id", "")
                    ).strip()

                    if not emp_id:

                        skipped += 1
                        continue

                    if Employee.objects.filter(
                        employee_id=emp_id
                    ).exists():

                        skipped += 1
                        continue

                    employee = Employee(

                        employee_id=emp_id,
                        employee_register_no=row.get("employee_register_no", ""),
                        name=row.get("name", ""),
                        gender=row.get("gender", ""),
                        father_spouse_name=row.get("father_spouse_name", ""),
                        dob=row.get("dob"),
                        nationality=row.get("nationality", ""),
                        education_level=row.get("education_level", ""),
                        department=row.get("department", ""),
                        designation=row.get("designation", ""),
                        category=row.get("category", ""),
                        employment_type=row.get("employment_type", ""),
                        mobile=str(row.get("mobile", "")),
                        joining_date=row.get("joining_date"),

                        uan=row.get("uan", ""),
                        pan=row.get("pan", ""),
                        esic_ip=row.get("esic_ip", ""),
                        lwf=row.get("lwf", ""),
                        aadhaar=row.get("aadhaar", ""),

                        bank_account_no=row.get("bank_account_no", ""),
                        bank_name=row.get("bank_name", ""),
                        ifsc=row.get("ifsc", ""),

                        present_address=row.get("present_address", ""),
                        permanent_address=row.get("permanent_address", ""),

                        service_book_no=row.get("service_book_no", ""),
                        exit_date=row.get("exit_date"),
                        exit_reason=row.get("exit_reason", ""),

                        identification_mark=row.get("identification_mark", ""),
                        remarks=row.get("remarks", ""),

                        owner_name=row.get("owner_name", ""),
                        token_number=row.get("token_number", ""),
                        first_appointment_date=row.get("first_appointment_date"),
                        age_fitness_certificate=row.get("age_fitness_certificate", ""),
                        place_of_employment=row.get("place_of_employment", ""),
                        vocational_training_number=row.get("vocational_training_number", ""),
                        vocational_training_date=row.get("vocational_training_date"),

                        nominee_name=row.get("nominee_name", ""),
                        nominee_address=row.get("nominee_address", ""),

                        emergency_contact_name=row.get("emergency_contact_name", ""),
                        emergency_contact_address=row.get("emergency_contact_address", ""),
                        emergency_mobile=row.get("emergency_mobile", "")
                    )

                    employee.save()

                    created += 1

                except Exception as e:

                    print("Row error:", e)

                    skipped += 1

            return JsonResponse({

                "message": "Upload completed",
                "created": created,
                "skipped": skipped

            })

        except Exception as e:

            return JsonResponse({

                "error": "Invalid Excel file",
                "details": str(e)

            }, status=400)

    return JsonResponse({
        "error": "Invalid request"
    }, status=400)

@login_required(login_url='login')
def employee_detail(request, id):

    employee = Employee.objects.get(id=id)

    return render(
        request,
        'employees/employee_detail.html',
        {
            'employee': employee
        }
    )

# EXPORT EXCEL

@login_required(login_url='login')
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
        'Employee Register No',
        'Name',
        'Gender',
        'Department',
        'Designation',
        'Mobile',
        'Joining Date',
        'Nationality',
        'Education Level',
        'UAN',
        'PAN',
        'AADHAAR'

    ]

    worksheet.append(headers)

    for employee in employees:

        worksheet.append([

            employee.employee_id,
            employee.employee_register_no,
            employee.name,
            employee.gender,
            employee.department,
            employee.designation,
            employee.mobile,
            str(employee.joining_date),
            employee.nationality,
            employee.education_level,
            employee.uan,
            employee.pan,
            employee.aadhaar

        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = (
        'attachment; filename=employees.xlsx'
    )

    workbook.save(response)

    return response