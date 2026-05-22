from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = '__all__'

        widgets = {

            # DATE FIELDS

            'dob': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'joining_date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'exit_date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'first_appointment_date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'vocational_training_date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            # TEXTAREA

            'present_address': forms.Textarea(
                attrs={'rows': 3}
            ),

            'permanent_address': forms.Textarea(
                attrs={'rows': 3}
            ),

            'remarks': forms.Textarea(
                attrs={'rows': 3}
            ),

            'identification_mark': forms.Textarea(
                attrs={'rows': 2}
            ),

            'exit_reason': forms.Textarea(
                attrs={'rows': 3}
            ),

            'nominee_address': forms.Textarea(
                attrs={'rows': 3}
            ),

            'emergency_contact_address': forms.Textarea(
                attrs={'rows': 3}
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # PROFESSIONAL DROPDOWN DEFAULTS

        self.fields['gender'].choices = [
            ('', 'Select one     ')
        ] + list(Employee.GENDER_CHOICES)

        self.fields['category'].choices = [
            ('', 'Select one     ')
        ] + list(Employee.CATEGORY_CHOICES)

        self.fields['place_of_employment'].choices = [
            ('', 'Select one     ')
        ] + list(Employee.PLACE_CHOICES)

        # PLACEHOLDER

        for field_name, field in self.fields.items():

            field.widget.attrs.update({
                'class': 'form-control'
            })

            if isinstance(field.widget, forms.Select):

                field.widget.attrs.update({
                    'class': 'form-select modern-select'
                })