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

        # ONLY THESE FIELDS REQUIRED

        required_fields = [

            'employee_id',
            'name',
            'department',
            'designation',
            'mobile',
            'joining_date'

        ]

        # MAKE OTHER FIELDS OPTIONAL

        for field_name, field in self.fields.items():

            if field_name not in required_fields:

                field.required = False

        # DROPDOWN DEFAULTS

        self.fields['gender'].choices = [
            ('', 'Select Gender  ▼')
        ] + list(Employee.GENDER_CHOICES)

        self.fields['category'].choices = [
            ('', 'Select Category  ▼')
        ] + list(Employee.CATEGORY_CHOICES)

       

        # STYLING

        for field_name, field in self.fields.items():

            field.widget.attrs.update({
                'class': 'form-control'
            })

            if isinstance(field.widget, forms.Select):

                field.widget.attrs.update({
                    'class': 'form-select modern-select'
                })