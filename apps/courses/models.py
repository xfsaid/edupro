#_*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from organization.models import CourseOrg

# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg,verbose_name="所属机构",null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name="课程名")
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    detail = models.TextField(verbose_name="课程详情")#后面可以改为富文本
    degree = models.CharField(choices=(("cj","初级"),("zj","中级"),("gj","高级")),max_length=2,verbose_name="难度")
    learn_times = models.IntegerField(default=0,verbose_name="学习时长")
    student_num = models.IntegerField(default=0,verbose_name="学习人数")
    collect_num = models.IntegerField(default=0,verbose_name="收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m",verbose_name="缩略图",max_length=100)
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    category = models.CharField(default="web后端开发",max_length=20, verbose_name="课程类别")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    #TODO
    def get_zj_nums(self):
        #获取课程章节数
        return self.lesson_set.count()

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def __unicode__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '[{0}] {1}'.format(self.course.name, self.name)


class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name="章节")
    name = models.CharField(max_length=100, verbose_name="视频名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '[{0}] {1}'.format(self.lesson.name, self.name)


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="名称")
    download = models.FileField(upload_to="course/resource/%Y/%m",verbose_name="资源文件",max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '[{0}] {1}'.format(self.course.name, self.name)
