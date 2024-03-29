# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-11 14:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beans', '0003_transaction'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Expense categories', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterField(
            model_name='transaction',
            name='description',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='description',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
