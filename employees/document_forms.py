from django import forms

from .models import EmployeeDocument


class EmployeeDocumentForm(forms.ModelForm):

    class Meta:

        model = EmployeeDocument

        fields = ['file']