# Generated by Django 4.2.2 on 2024-05-06 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificate_app', '0025_tronix_height_tronix_width'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tronix',
            name='height',
            field=models.FloatField(default=50),
        ),
    ]
