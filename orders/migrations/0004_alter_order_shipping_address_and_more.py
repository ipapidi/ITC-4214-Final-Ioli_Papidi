# Generated by Django 5.2.3 on 2025-07-20 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_product_snapshot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.TextField(help_text='Shipping address (max 1000 characters)'),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_city',
            field=models.CharField(help_text='Shipping city (max 100 characters)', max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_country',
            field=models.CharField(help_text='Shipping country (max 100 characters)', max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_phone',
            field=models.CharField(help_text='Shipping phone number (max 20 characters)', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_postal_code',
            field=models.CharField(help_text='Shipping postal code (max 20 characters)', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_state',
            field=models.CharField(help_text='Shipping state/province (max 100 characters)', max_length=100),
        ),
    ]
