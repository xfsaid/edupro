# -*- coding: utf-8  -*-
__author__ = 'said'
__date__ = '2017/9/14 2:40'

import xadmin

from .models import UserAsk, UserCourse, UserMessage, CourseComments, UserCollect

#define--admins
class UserAskAdmin(object):
    list_display = ['name','mobile', 'course_name', 'add_time']
    search_fields = ['name','mobile', 'course_name']
    list_filter = ['name','mobile', 'course_name', 'add_time']


class UserCourseAdmin(object):
    list_display = ['user','course','add_time']
    search_fields = ['user','course','add_time']
    list_filter = ['user','course__name','add_time']


class UserMessageAdmin(object):
    list_display = ['user_id','message','has_read','add_time']
    search_fields = ['user_id','message','has_read']
    list_filter = ['user_id','message','has_read','add_time']


class CourseCommentsAdmin(object):
    list_display = ['user','course','comments','add_time']
    search_fields = ['user','course','comments']
    list_filter = ['user','course','comments','add_time']


class UserCollectAdmin(object):
    list_display = ['user','collect_id','collect_type','add_time']
    search_fields = ['user','collect_id','collect_type']
    list_filter = ['user','collect_id','collect_type','add_time']





#register
xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserCollect, UserCollectAdmin)