# Generated by Django 4.2.2 on 2024-04-02 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('certificate_app', '0045_studentrelatedauthority_remove_student_authorities_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificatetypes',
            name='authorities',
        ),
    ]
