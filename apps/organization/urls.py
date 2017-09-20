# -*- coding: utf-8  -*-
__author__ = 'said'
__date__ = '2017/9/21 2:39'

from django.conf.urls import url,include
from .views import OrgView,AddUserAskView


urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
]