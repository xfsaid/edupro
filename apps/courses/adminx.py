# -*- coding: utf-8  -*-
__author__ = 'said'
__date__ = '2017/9/14 1:43'

import xadmin

from .models import Course, Lesson, Video, CourseResource,BannerCourse


class LessonInLine(object):
    model = Lesson
    extra = 0

class CourseResourceInLine(object):
    model = CourseResource
    extra = 0


#define--admins
class CourseAdmin(object):
    list_display = ['name','desc','detail','degree','learn_times','student_num','collect_num','image','click_num','get_zj_nums','go_to','add_time']
    search_fields = ['name','desc','detail','degree','learn_times','student_num','collect_num','image','click_num']
    list_filter = ['name','desc','detail','degree','learn_times','student_num','collect_num','image','click_num','add_time']
    ordering = ['-click_num']
    readonly_fields = ['click_num','student_num']
    exclude = ['collect_num']#编辑页面不显示，若字段在readonly_fields中，则不生效
    inlines = [LessonInLine, CourseResourceInLine]#添加课程界面，可以复数添加章节，但是不能同时添加章节的视频信息了
    list_editable = ['degree','desc']#字段可直接修改
    refresh_times = [3,6]#定时刷新选项
    style_fields = {"detail":"ueditor"}#xadmin/plugins/ueditor.py中,style == 'ueditor'

    def queryset(self):#自定义过滤逻辑
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):#自定义保存操作的相关逻辑
        obj = self.new_obj #Course实例
        obj.save()#新增课程，防止漏计算count
        if obj.course_org:
            course_org = obj.course_org
            course_org.course_num = Course.objects.filter(course_org=course_org).count()
            course_org.save()

class BannerCourseAdmin(object):
    list_display = ['name','desc','detail','degree','learn_times','student_num','collect_num','image','click_num','get_zj_nums','add_time']
    search_fields = ['name','desc','detail','degree','learn_times','student_num','collect_num','image','click_num']
    list_filter = ['name','desc','detail','degree','learn_times','student_num','collect_num','image','click_num','add_time']
    ordering = ['-click_num']
    readonly_fields = ['click_num','student_num']
    exclude = ['collect_num']#编辑页面不显示，若字段在readonly_fields中，则不生效
    inlines = [LessonInLine, CourseResourceInLine]#添加课程界面，可以复数添加章节，但是不能同时添加章节的视频信息了

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


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
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)