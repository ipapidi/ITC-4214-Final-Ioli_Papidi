# Generated by Django 5.2.3 on 2025-07-01 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_performance_rating_productrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productrating',
            name='rating',
            field=models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]),
        ),
    ]
