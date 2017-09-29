# -*- coding: utf-8  -*-
__author__ = 'said'
__date__ = '2017/9/23 10:52'


from django.conf.urls import url,include
from .views import CourseListView,CourseDetailView,CourseInfoView,CommentsView,AddCommentView,VideoPlayView


urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),
    url(r'^comments/(?P<course_id>\d+)/$', CommentsView.as_view(), name="course_comments"),
    url(r'^add_comment/$', AddCommentView.as_view(), name="add_comment"),
    url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name="video_play"),
]