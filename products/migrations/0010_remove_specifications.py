# Generated by Django 5.2.3 on 2025-07-12 01:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_remove_product_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='specifications',
        ),
        migrations.DeleteModel(
            name='ProductSpecification',
        ),
    ]
