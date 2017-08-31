# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-29 15:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_cart_subtotal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=50),
        ),
        migrations.AlterField(
            model_name='cart',
            name='tax_percentage',
            field=models.DecimalField(decimal_places=2, default=0.085, max_digits=50),
        ),
        migrations.AlterField(
            model_name='cart',
            name='tax_total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=50),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=50),
        ),
    ]