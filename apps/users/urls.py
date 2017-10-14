# -*- coding: utf-8  -*-
__author__ = 'said'
__date__ = '2017/10/14 12:27'

from django.conf.urls import url,include
from .views import UserInofView,UserUploadImageView,UserUpdatePwdView

urlpatterns = [
    url(r'^info/$', UserInofView.as_view(), name="users_info"),
    url(r'^image/upload/$', UserUploadImageView.as_view(), name="image_upload"),
    url(r'^update/pwd/$', UserUpdatePwdView.as_view(), name="update_pwd"),
]