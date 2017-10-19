#_*_ encoding:utf-8 _*_
"""edupro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
import xadmin

#from users.views import login_view
from users.views import LoginView,RegisterView,ActiveUserView, ForgetPwdView,ResetView
from users.views import IndexView, ModifyPwdView,LogoutView
from organization.views import OrgView
from edupro.settings import MEDIA_ROOT
#release
#from edupro.settings import STATIC_ROOT


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^ueditor/',include('DjangoUeditor.urls')),
    url(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}),

    #release 生产环境配置
    #url(r'^static/(?P<path>.*)$', serve, {"document_root":STATIC_ROOT}),

    url('^$',IndexView.as_view(),name="index"),
    #url('^login/$',login_view, name="login"),
    url('^login/$',LoginView.as_view(), name="login"),
    url('^logout/$',LogoutView.as_view(), name="logout"),
    url('^register/$',RegisterView.as_view(), name="register"),

    url(r'^captcha/', include('captcha.urls')),


    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'^modifypwd/$', ModifyPwdView.as_view(), name="modify_pwd"),


    url(r'^org/', include('organization.urls', namespace="org")),
    url(r'^course/', include('courses.urls', namespace="course")),
    url(r'^users/', include('users.urls', namespace="users")),
]

#全局4004页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'