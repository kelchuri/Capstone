# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-20 00:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Capstone', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machinetype',
            name='IdealTemperature',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]