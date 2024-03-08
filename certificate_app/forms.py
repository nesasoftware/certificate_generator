from django import forms
from .models import Student


class MyForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        widgets = {
            'start_date': forms.TextInput(attrs={'type': 'date'}),
            'end_date': forms.TextInput(attrs={'type': 'date'}),
            'course': forms.Select(choices=[('', 'Select Course')]  + list(Student.objects.values_list('course', 'course').distinct())),
        }
