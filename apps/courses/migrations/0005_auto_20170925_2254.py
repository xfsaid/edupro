# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-09-25 22:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_video_video_times'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseresource',
            name='download',
            field=models.FileField(upload_to='courses/resource/%Y/%m', verbose_name='\u8d44\u6e90\u6587\u4ef6'),
        ),
    ]