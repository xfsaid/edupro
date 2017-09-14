# -*- coding: utf-8  -*-
__author__ = 'said'
__date__ = '2017/9/14 1:05'

import xadmin
from xadmin import views

from .models import EmailVerifyRecord,Banner


class BaseSetting(object):
    """
    需要修改xadmin的源码：
    1.install requests and import
    2.修改函数xadmin/plugins/themes.py：block_top_navmenu请求方法
    """
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = "218 EDU后台管理系统"
    site_footer = "218 EDU在线"
    menu_style = "accordion" #app收起model


####################
class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']
    search_fields = ['code','email','send_type']
    list_filter = ['code','email','send_type','send_time']


class BannerAdmin(object):
    list_display = ['title','image','url','index','add_time']
    search_fields = ['title','image','url','index']
    list_filter = ['title','image','url','index','add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
