# Generated by Django 4.2.2 on 2024-04-03 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('certificate_app', '0046_remove_certificatetypes_authorities'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificatetypes',
            name='courses',
        ),
        migrations.AddField(
            model_name='certificatetypes',
            name='courses',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='certificate_types', to='certificate_app.course'),
        ),
    ]
