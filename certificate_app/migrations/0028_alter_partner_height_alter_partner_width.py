# Generated by Django 4.2.2 on 2024-05-07 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificate_app', '0027_remove_tronix_height_remove_tronix_width_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='height',
            field=models.FloatField(default=40),
        ),
        migrations.AlterField(
            model_name='partner',
            name='width',
            field=models.FloatField(default=80),
        ),
    ]
