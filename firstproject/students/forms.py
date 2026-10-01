from django import forms
from .models import Student, Course


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'roll_number',
            'first_name',
            'last_name',
            'email',
            'phone',
            'date_of_birth',
            'gender',
            'course',
            'enrollment_date',
            'gpa',
            'status',
            'address',
        ]
        widgets = {
            'roll_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. STU-2026-001'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'student@university.edu'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 000-0000'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'enrollment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '10', 'placeholder': 'e.g. 3.85'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Current residential address'}),
        }

    def clean_gpa(self):
        gpa = self.cleaned_data.get('gpa')
        if gpa is not None and (gpa < 0 or gpa > 10):
            raise forms.ValidationError("GPA must be between 0.0 and 10.0.")
        return gpa


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'duration_years', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Computer Science'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CSE'}),
            'duration_years': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 6}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief course overview...'}),
        }
