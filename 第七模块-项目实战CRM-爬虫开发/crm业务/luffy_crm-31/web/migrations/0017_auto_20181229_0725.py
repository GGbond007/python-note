# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-12-29 07:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0016_studyrecord'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studyrecord',
            name='course_record',
        ),
        migrations.RemoveField(
            model_name='studyrecord',
            name='student',
        ),
        migrations.DeleteModel(
            name='StudyRecord',
        ),
    ]
