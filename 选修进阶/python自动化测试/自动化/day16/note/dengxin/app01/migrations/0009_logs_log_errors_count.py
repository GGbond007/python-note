# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-05-07 07:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0008_logs'),
    ]

    operations = [
        migrations.AddField(
            model_name='logs',
            name='log_errors_count',
            field=models.IntegerField(default=0, verbose_name='报错数量'),
            preserve_default=False,
        ),
    ]
