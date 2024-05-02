from django.contrib import admin
from . models import Authority, Student, CertificateTypes, Course, StudentIV, StudentRelatedAuthority

# Register your models here.
admin.site.register(Authority)
admin.site.register(Student)
admin.site.register(StudentIV)
admin.site.register(CertificateTypes)
admin.site.register(Course)