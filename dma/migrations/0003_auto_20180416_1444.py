# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-16 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dma', '0002_auto_20180416_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stations',
            name='installed',
            field=models.DateField(blank=True, null=True, verbose_name='\u5b89\u88c5\u65e5\u671f'),
        ),
    ]