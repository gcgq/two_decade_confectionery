# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-05 02:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20170904_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_total_in_cents',
            field=models.IntegerField(),
        ),
    ]