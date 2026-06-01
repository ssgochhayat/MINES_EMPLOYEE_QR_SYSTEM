
from django.db import models
import qrcode

from io import BytesIO
from django.core.files import File


class Employee(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    CATEGORY_CHOICES = [
        ('Highly Skilled', 'Highly Skilled'),
        ('Skilled', 'Skilled'),
        ('Semi Skilled', 'Semi Skilled'),
        ('Un Skilled', 'Un Skilled'),
    ]

    PLACE_CHOICES = [
        ('Underground', 'Underground'),
        ('Open Cast', 'Open Cast'),
        ('Surface', 'Surface'),
    ]

    # BASIC DETAILS

    employee_id = models.CharField(
        max_length=20,
        unique=True
    )

    

    name = models.CharField(max_length=100)

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )

    father_spouse_name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    dob = models.DateField(
        blank=True,
        null=True
    )

    nationality = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    education_level = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    department = models.CharField(max_length=100)

    designation = models.CharField(max_length=100)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        blank=True,
        null=True
    )

    employment_type = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    mobile = models.CharField(max_length=15)

    joining_date = models.DateField()

    # GOVERNMENT DETAILS

    uan = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    pan = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    place_of_birth = models.CharField(
    max_length=200,
    blank=True,
    null=True
)

    eps_nps = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    family_details = models.TextField(
        blank=True,
        null=True
    )

    posting_details = models.TextField(
        blank=True,
        null=True
    )

    pay = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    promotion = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    esic_ip = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

   

    aadhaar = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # BANK DETAILS

    bank_account_no = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    bank_name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    ifsc = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # ADDRESS

    present_address = models.TextField(
        blank=True,
        null=True
    )

    permanent_address = models.TextField(
        blank=True,
        null=True
    )

    # EXIT DETAILS

    service_book_no = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    exit_date = models.DateField(
        blank=True,
        null=True
    )

    exit_reason = models.TextField(
        blank=True,
        null=True
    )

    # IDENTIFICATION

    identification_mark = models.TextField(
        blank=True,
        null=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    # PHOTO

    photo = models.ImageField(
        upload_to='employee_photos/',
        blank=True,
        null=True
    )

    # SIGNATURE

    signature = models.ImageField(
        upload_to='employee_signatures/',
        blank=True,
        null=True
    )

    # QR CODE

    qr_code = models.ImageField(
        upload_to='qr_codes/',
        blank=True,
        null=True
    )

    # PDF DOCUMENTS

    joining_letter = models.FileField(
        upload_to='documents/joining_letters/',
        blank=True,
        null=True
    )

    appointment_letter = models.FileField(
        upload_to='documents/appointment_letters/',
        blank=True,
        null=True
    )


    nominee_name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )


   

    # SAVE METHOD

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        # QR URL

        qr_data = f"http://10.36.83.65:8000/employee-pdf/{self.id}/"

        # FOR LIVE SERVER:
        # qr_data = f"https://yourdomain.com/employees/{self.id}/"

        # GENERATE QR

        qr_img = qrcode.make(qr_data)

        buffer = BytesIO()

        qr_img.save(buffer, format='PNG')

        file_name = f'{self.employee_id}.png'

        # SAVE QR IMAGE

        self.qr_code.save(
            file_name,
            File(buffer),
            save=False
        )

        super().save(update_fields=['qr_code'])

    # STRING METHOD

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ('view_dashboard', 'Can view dashboard'),
            ('import_employee_excel', 'Can upload employee Excel'),
            ('export_employee_excel', 'Can export employee Excel'),
            ('scan_employee_qr', 'Can use employee QR scanner'),
        )


class EmployeeDocument(models.Model):

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='documents'
    )

    document_name = models.CharField(
        max_length=200
    )

    file = models.FileField(
        upload_to='employee_documents/'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.document_name

