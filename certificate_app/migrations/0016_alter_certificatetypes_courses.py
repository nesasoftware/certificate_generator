# Generated by Django 4.2.2 on 2024-05-02 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificate_app', '0015_tronix_events_remove_tronix_events_studenttronix_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificatetypes',
            name='courses',
            field=models.ManyToManyField(null=True, related_name='certificate_types', to='certificate_app.course'),
        ),
    ]