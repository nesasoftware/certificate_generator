# Generated by Django 4.2.2 on 2024-03-06 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificate_app', '0002_student_college_name_student_mentor_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='course',
            field=models.CharField(choices=[('robotic operating system', 'Robotic Operating System'), ('python', 'Python'), ('java', 'Java')], max_length=100),
        ),
    ]
