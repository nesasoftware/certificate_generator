# Generated by Django 4.2.2 on 2024-03-30 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('certificate_app', '0030_alter_certificatetype_authorities'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CertificateType',
            new_name='CertificateTypes',
        ),
    ]
