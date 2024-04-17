from django import forms
from django.core.validators import FileExtensionValidator
from .models import Student,StudentIV



class MyForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"


class MyIvForm(forms.ModelForm):
    class Meta:
        model = StudentIV
        fields = "__all__"

class UploadFileForm(forms.Form):
    csv_file = forms.FileField(label='CSV File', validators=[FileExtensionValidator(allowed_extensions=['csv'])])

