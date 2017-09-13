# -*- coding: utf-8  -*-
__author__ = 'said'
__date__ = '2017/9/14 1:43'

import xadmin

from .models import Course, Lesson, Video, CourseResource


#define--admins
class CourseAdmin(object):
    list_display = ['name','desc','detail','degree','learn_times','student_num','collect_num','image','click_num','add_time']
    search_fields = ['name','desc','detail','degree','learn_times','student_num','collect_num','image','click_num']
    list_filter = ['name','desc','detail','degree','learn_times','student_num','collect_num','image','click_num','add_time']


class LessonAdmin(object):
    list_display = ['course','name','add_time']
    search_fields = ['course','name']
    list_filter = ['course__name','name','add_time']


class VideoAdmin(object):
    list_display = ['lesson','name','add_time']
    search_fields = ['lesson','name']
    list_filter = ['lesson__course__name','lesson__name','name','add_time']


class CourseResourceAdmin(object):
    list_display = ['course','name','download','add_time']
    search_fields = ['course','name','download']
    list_filter = ['course__name','name','download','add_time']



#register
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)