# Generated by Django 5.2.3 on 2025-07-12 01:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile_is_vendor_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='car_color',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='primary_car_make',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='primary_car_model',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='primary_car_year',
        ),
    ]
