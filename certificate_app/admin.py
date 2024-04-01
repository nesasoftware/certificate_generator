from django.contrib import admin
from . models import Authority, Student, CertificateTypes, Course

# Register your models here.
admin.site.register(Authority)
admin.site.register(Student)
admin.site.register(CertificateTypes)
admin.site.register(Course)