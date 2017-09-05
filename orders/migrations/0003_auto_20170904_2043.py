# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-04 20:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20170829_1523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_id',
        ),
        migrations.RemoveField(
            model_name='usercheckout',
            name='braintree_id',
        ),
        migrations.AddField(
            model_name='order',
            name='order_total_in_cents',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('created', 'Created'), ('completed', 'Completed')], default='created', max_length=120),
        ),
    ]
