# Generated by Django 4.2.2 on 2024-04-04 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificate_app', '0002_student_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authority',
            name='authority_id',
            field=models.TextField(max_length=5, null=True),
        ),
    ]
