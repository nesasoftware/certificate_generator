# Generated by Django 4.2.2 on 2024-03-28 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('certificate_app', '0023_certificatetype_student_certificate_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='course',
        ),
    ]
