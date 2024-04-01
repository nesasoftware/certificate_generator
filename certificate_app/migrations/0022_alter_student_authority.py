# Generated by Django 4.2.2 on 2024-03-27 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('certificate_app', '0021_alter_authority_name_alter_authority_organization_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='authority',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='certificate_app.authority'),
        ),
    ]
