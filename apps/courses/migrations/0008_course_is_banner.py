# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-10-16 23:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20170925_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_banner',
            field=models.BooleanField(default=False, verbose_name='\u8f6e\u64ad\u4f4d'),
        ),
    ]