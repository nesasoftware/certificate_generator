# Generated by Django 4.2.2 on 2024-04-04 10:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('certificate_app', '0005_alter_authority_authority_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='authority',
            name='authority_id',
            field=models.IntegerField(null=True),
        ),
    ]
