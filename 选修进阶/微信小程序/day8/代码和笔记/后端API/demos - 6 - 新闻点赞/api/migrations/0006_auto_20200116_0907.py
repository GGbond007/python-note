# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-01-16 01:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20200115_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.CharField(default=1, max_length=64, verbose_name='头像'),
            preserve_default=False,
        ),
    ]
