# serializers.py
from rest_framework import serializers
from .models import Student,StudentIV,StudentTronix,CertificateTypes,Course, Tronix, TronixItems


class CertificateTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateTypes
        # fields = '__all__'
        exclude = ['courses']  # Exclude the 'courses' field


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    certificate_type = CertificateTypesSerializer()  # Use CertificateTypesSerializer for the certificate_type field
    course = CourseSerializer() # Use CourseSerializer for the course field
    class Meta:
        model = Student
        fields = '__all__'


class TronixItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TronixItems
        fields = '__all__'


class TronixSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tronix
        fields = '__all__'

class StudentTronixSerializer(serializers.HyperlinkedModelSerializer):
    certificate_type = CertificateTypesSerializer()
    class Meta:
        model = StudentTronix
        fields = '__all__'
        
class StudentIVSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StudentIV
        fields = '__all__'



