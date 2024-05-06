from django.contrib import admin
from . models import Authority, Student, CertificateTypes, Course, StudentIV, StudentTronix, Tronix, TronixItems, StudentRelatedAuthority, Partner

# Register your models here.
admin.site.register(Authority)
admin.site.register(Student)
admin.site.register(StudentIV)
admin.site.register(StudentTronix)
admin.site.register(Tronix)
admin.site.register(TronixItems)
admin.site.register(CertificateTypes)
admin.site.register(Course)
admin.site.register(Partner)