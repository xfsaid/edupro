# -*- coding: utf-8  -*-
__author__ = 'said'
__date__ = '2017/10/14 12:27'


from django.conf.urls import url,include
from .views import UserInofView,UserUploadImageView,UserUpdatePwdView,SendEmailCodeView,UpdateEmailView
from .views import MyCourseView,MyCollectOrgView, MyCollectTeacherView, MyCollectCourseView, MyMessageView


urlpatterns = [
    url(r'^info/$', UserInofView.as_view(), name="users_info"),
    url(r'^image/upload/$', UserUploadImageView.as_view(), name="image_upload"),
    url(r'^update/pwd/$', UserUpdatePwdView.as_view(), name="update_pwd"),
    #发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="sendemail_code"),
    #修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),

    #我的课程
    url(r'^mycourse/$', MyCourseView.as_view(), name="mycourse"),

    #我的收藏
    url(r'^mycollect/org$', MyCollectOrgView.as_view(), name="mycollect_org"),
    url(r'^mycollect/teacher$', MyCollectTeacherView.as_view(), name="mycollect_teacher"),
    url(r'^mycollect/course$', MyCollectCourseView.as_view(), name="mycollect_course"),

    url(r'^mymessage/$', MyMessageView.as_view(), name="mymessage"),

]