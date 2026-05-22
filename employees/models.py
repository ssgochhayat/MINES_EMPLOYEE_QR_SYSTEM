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
        ('HS', 'Highly Skilled'),
        ('S', 'Skilled'),
        ('SS', 'Semi Skilled'),
        ('US', 'Un Skilled'),
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

    employee_register_no = models.CharField(
        max_length=100,
        blank=True,
        null=True
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
        max_length=10,
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

    esic_ip = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    lwf = models.CharField(
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

    # PART-B MINES DETAILS

    owner_name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    token_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    first_appointment_date = models.DateField(
        blank=True,
        null=True
    )

    age_fitness_certificate = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    place_of_employment = models.CharField(
        max_length=50,
        choices=PLACE_CHOICES,
        blank=True,
        null=True
    )

    vocational_training_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    vocational_training_date = models.DateField(
        blank=True,
        null=True
    )

    nominee_name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    nominee_address = models.TextField(
        blank=True,
        null=True
    )

    emergency_contact_name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    emergency_contact_address = models.TextField(
        blank=True,
        null=True
    )

    emergency_mobile = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):

        qr_data = f"""
Employee ID: {self.employee_id}
Name: {self.name}
Department: {self.department}
Designation: {self.designation}
Mobile: {self.mobile}
"""

        qr_img = qrcode.make(qr_data)

        buffer = BytesIO()

        qr_img.save(buffer, format='PNG')

        file_name = f'{self.employee_id}.png'

        self.qr_code.save(
            file_name,
            File(buffer),
            save=False
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


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