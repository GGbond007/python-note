# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-02-16 02:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0061_coupon_deleted'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='收货人姓名')),
                ('phone', models.CharField(max_length=11, verbose_name='联系电话')),
                ('city', models.CharField(max_length=64, verbose_name='收货地址')),
                ('detail', models.CharField(max_length=64, verbose_name='详细地址')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.UserInfo', verbose_name='用户')),
            ],
        ),
    ]
