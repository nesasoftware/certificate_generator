# Generated by Django 4.2.2 on 2024-04-02 06:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('certificate_app', '0039_remove_certificatetypes_signed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificatetypes',
            name='signed',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='certificate_app.authority'),
        ),
    ]
