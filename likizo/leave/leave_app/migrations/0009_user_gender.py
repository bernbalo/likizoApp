# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-20 14:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave_app', '0008_auto_20180520_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(max_length=6, null=True),
        ),
    ]
