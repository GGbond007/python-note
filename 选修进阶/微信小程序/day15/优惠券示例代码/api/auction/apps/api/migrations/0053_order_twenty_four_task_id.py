# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-02-12 11:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0052_auto_20200212_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='twenty_four_task_id',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='24小时后定时任务'),
        ),
    ]
