# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-24 11:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '6_24_1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='BookNo',
            field=models.CharField(max_length=11),
        ),
    ]