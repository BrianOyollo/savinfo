# Generated by Django 5.1.1 on 2024-09-25 09:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_order_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(blank=True, max_length=13, null=True, validators=[django.core.validators.MinValueValidator(10)]),
        ),
    ]
