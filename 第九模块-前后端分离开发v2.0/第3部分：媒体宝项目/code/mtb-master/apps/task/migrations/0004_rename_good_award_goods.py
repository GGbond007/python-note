# Generated by Django 3.2 on 2022-04-01 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_alter_activity_protect_switch'),
    ]

    operations = [
        migrations.RenameField(
            model_name='award',
            old_name='good',
            new_name='goods',
        ),
    ]
