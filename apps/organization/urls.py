# -*- coding: utf-8  -*-
__author__ = 'said'
__date__ = '2017/9/21 2:39'

from django.conf.urls import url,include
from .views import OrgView,AddUserAskView,OrgHomeView,OrgCourseView,OrgDescView,OrgTeacherView,AddCollectView
from .views import TeacherListView, TeacherDetailView

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),

    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),
    url(r'^org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),

    url(r'^add_collect/$', AddCollectView.as_view(), name="add_collect"),
    url(r'^teacher/list/$', TeacherListView.as_view(), name="teacher_list"),
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),
]