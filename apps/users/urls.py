# -*- coding: utf-8  -*-
__author__ = 'said'
__date__ = '2017/10/14 12:27'

from django.conf.urls import url,include
from .views import UserInofView,UserUploadImageView,UserUpdatePwdView,SendEmailCodeView,UpdateEmailView
from .views import MyCourseView
urlpatterns = [
    url(r'^info/$', UserInofView.as_view(), name="users_info"),
    url(r'^mycourse/$', MyCourseView.as_view(), name="mycourse"),


    url(r'^image/upload/$', UserUploadImageView.as_view(), name="image_upload"),
    url(r'^update/pwd/$', UserUpdatePwdView.as_view(), name="update_pwd"),
    #发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="sendemail_code"),
    #修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),
]