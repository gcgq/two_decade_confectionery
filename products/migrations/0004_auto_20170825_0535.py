# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 05:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_productimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Truffle', 'Truffle'), ('Cookie', 'Cookie'), ('Cupcake', 'Cupcake')], default='Truffle', max_length=10),
        ),
    ]
