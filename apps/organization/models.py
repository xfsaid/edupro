#_*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime


from django.db import models

# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name="城市")
    desc = models.CharField(max_length=200,verbose_name="城市描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseOrg(models.Model):
    categorys = (
        ("pxjg","培训机构"),
        ("gr","个人"),
        ("gx","高校")
    )

    name = models.CharField(max_length=50, verbose_name="机构名称")
    desc = models.TextField(verbose_name="机构描述")
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    collect_num = models.IntegerField(default=0,verbose_name="收藏人数")
    student_num = models.IntegerField(default=0,verbose_name="学习人数")
    course_num = models.IntegerField(default=0,verbose_name="课程数")
    image = models.ImageField(upload_to="org/%Y/%m",verbose_name="Logo",max_length=100)
    address = models.CharField(max_length=100, default="",verbose_name="机构地址")
    category = models.CharField(default="pxjg",choices=categorys,max_length=20,verbose_name="机构类别")
    city = models.ForeignKey(CityDict,verbose_name="所在城市")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg,verbose_name="所属机构")
    name = models.CharField(max_length=50, verbose_name="教师名")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=50, verbose_name="就职公司")
    work_position = models.CharField(max_length=50, verbose_name="公司职位")
    points = models.CharField(max_length=100,verbose_name="教学特点")
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    collect_num = models.IntegerField(default=0,verbose_name="收藏数")
    add_time = models.DateField(default=datetime.now)

    class Meta:
        verbose_name = "教师信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '[{0}] {1}'.format(self.org.name, self.name)


