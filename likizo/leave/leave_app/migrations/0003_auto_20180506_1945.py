# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-06 19:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leave_app', '0002_auto_20180506_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='leave',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leaves', to='leave_app.Leave'),
        ),
    ]