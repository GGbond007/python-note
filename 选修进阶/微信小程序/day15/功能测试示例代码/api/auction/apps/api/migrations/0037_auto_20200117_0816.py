# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-01-17 08:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_auctionitem_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionitem',
            name='price',
        ),
        migrations.AddField(
            model_name='auctionitem',
            name='start_price',
            field=models.PositiveIntegerField(default=1000, verbose_name='起拍价'),
            preserve_default=False,
        ),
    ]
