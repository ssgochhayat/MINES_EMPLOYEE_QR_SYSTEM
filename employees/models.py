from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File


class Employee(models.Model):

    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    joining_date = models.DateField()

    # PHOTO
    photo = models.ImageField(
        upload_to='employee_photos/',
        blank=True,
        null=True
    )

    # QR CODE
    qr_code = models.ImageField(
        upload_to='qr_codes/',
        blank=True
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

    document_name = models.CharField(max_length=200)

    file = models.FileField(
        upload_to='employee_documents/'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.document_name