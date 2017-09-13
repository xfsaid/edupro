#_*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from users.models import UserProfile
from courses.models import Course

# Create your models here.


class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name="姓名")
    mobile = models.CharField(max_length=11, verbose_name="手机号")
    course_name = models.CharField(max_length=50, verbose_name="课程名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile, default="用户")
    course = models.ForeignKey(Course, verbose_name="课程")
    comments = models.CharField(max_length=200, verbose_name="评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.comments


class UserCollect(models.Model):
    #course = models.ForeignKey(Course, verbose_name="课程")
    #teacher = models.ForeignKey(***, verbose_name="讲师")
    #org = models.ForeignKey(***, verbose_name="机构")
    user = models.ForeignKey(UserProfile, default="用户")
    collect_id = models.IntegerField(default=0, verbose_name="ID")
    collect_type = models.IntegerField(choices=((1,"课程"),(2,"机构"),(3,"讲师")),default=1,verbose_name="收藏类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user_id = models.IntegerField(default=0,verbose_name="接收用户")
    message = models.CharField(max_length=500, verbose_name="消息内容")
    has_read = models.BooleanField(default=False, verbose_name="是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, default="用户")
    course = models.ForeignKey(Course, verbose_name="课程")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="学习时间")

    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural = verbose_name










