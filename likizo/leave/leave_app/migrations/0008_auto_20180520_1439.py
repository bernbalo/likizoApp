# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-20 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave_app', '0007_user_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='duration',
            field=models.IntegerField(),
        ),
    ]
