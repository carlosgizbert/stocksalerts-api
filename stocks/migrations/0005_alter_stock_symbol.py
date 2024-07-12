# Generated by Django 5.0.6 on 2024-07-12 03:40

import stocks.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0004_alter_stock_symbol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='symbol',
            field=models.CharField(max_length=10, validators=[stocks.models.validate_unique_symbol]),
        ),
    ]
