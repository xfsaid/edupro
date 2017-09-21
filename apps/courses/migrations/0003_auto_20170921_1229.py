# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-09-21 12:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_course_org'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(upload_to='courses/%Y/%m', verbose_name='\u7f29\u7565\u56fe'),
        ),
        migrations.AlterField(
            model_name='courseresource',
            name='download',
            field=models.FileField(upload_to='course/resource/%Y/%m', verbose_name='\u8d44\u6e90\u6587\u4ef6'),
        ),
    ]
