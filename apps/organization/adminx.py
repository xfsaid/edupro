# -*- coding: utf-8  -*-
__author__ = 'said'
__date__ = '2017/9/14 2:16'

import xadmin

from .models import CityDict, CourseOrg, Teacher

#define--admins
class CityDictAdmin(object):
    list_display = ['name','desc','add_time']
    search_fields = ['name','desc']
    list_filter = ['name','desc','add_time']


class CourseOrgAdmin(object):
    list_display = ['name','desc','click_num','collect_num','image','address','city','add_time']
    search_fields = ['name','desc','click_num','collect_num','image','address','city']
    list_filter = ['name','desc','click_num','collect_num','image','address','city','add_time']


class TeacherAdmin(object):
    list_display = ['org','name','work_years','work_company','work_position','points','click_num','collect_num','add_time']
    search_fields = ['org','name','work_years','work_company','work_position','points','click_num','collect_num']
    list_filter = ['org__name','name','work_years','work_company','work_position','points','click_num','collect_num','add_time']





#register
xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)