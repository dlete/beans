# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-11 14:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beans', '0012_auto_20161205_2149'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beans.Category')),
            ],
        ),
    ]