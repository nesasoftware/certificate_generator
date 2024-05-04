# Generated by Django 4.2.2 on 2024-05-02 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('certificate_app', '0014_tronix'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tronix_events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('events', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='tronix',
            name='events',
        ),
        migrations.CreateModel(
            name='StudentTronix',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('school', models.CharField(max_length=255, null=True)),
                ('tronix_details', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='certificate_app.tronix')),
            ],
        ),
        migrations.AddField(
            model_name='tronix',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='certificate_app.tronix_events'),
        ),
    ]