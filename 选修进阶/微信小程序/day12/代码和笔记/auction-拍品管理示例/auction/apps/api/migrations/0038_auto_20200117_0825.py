# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-01-17 08:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_auto_20200117_0816'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='blance',
            field=models.PositiveIntegerField(default=1000, verbose_name='账户余额'),
        ),
        migrations.AlterField(
            model_name='depositrecord',
            name='auction',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.Auction', verbose_name='拍卖'),
            preserve_default=False,
        ),
    ]
