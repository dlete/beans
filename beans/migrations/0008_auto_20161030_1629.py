# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 16:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beans', '0007_transaction_client'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='client',
            new_name='user',
        ),
    ]