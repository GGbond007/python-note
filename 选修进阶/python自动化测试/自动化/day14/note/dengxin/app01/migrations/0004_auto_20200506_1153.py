# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-05-06 03:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_api'),
    ]

    operations = [
        migrations.AlterField(
            model_name='api',
            name='api_run_time',
            field=models.DateTimeField(null=True, verbose_name='执行时间'),
        ),
    ]
