# -*- coding: utf-8  -*-
from django.shortcuts import render,HttpResponse
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course,Video
from operation.models import UserCollect,CourseComments,UserCourse
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.


class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_num")[:3]

        #搜索功能
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords))

        sort = request.GET.get("sort","")
        if sort:
            if sort == "student_num":
                all_courses = all_courses.order_by("-student_num")
            elif sort == "click_num":
                all_courses = all_courses.order_by("-click_num")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)#每页显示条数
        page_orgs = p.page(page)
        return render(request,'course-list.html',{
            "all_courses":page_orgs,
            "sort":sort,
            "hot_courses":hot_courses,
        })


class CourseDetailView(View):
    def get(self,request,course_id):
        current_course = Course.objects.get(id=int(course_id))

        current_course.click_num += 1
        current_course.save()

        relate_courses = None
        tag = current_course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag).exclude(id=current_course.id)[:2]

        has_cl_course = False
        has_cl_org = False
        if request.user.is_authenticated():
            if UserCollect.objects.filter(user=request.user, collect_id=current_course.id,collect_type=1):
                has_cl_course = True
            if UserCollect.objects.filter(user=request.user, collect_id=current_course.course_org.id,collect_type=2):
                has_cl_org = True

        return render(request, "course-detail.html",{
            "current_course":current_course,
            "relate_courses":relate_courses,
            "has_cl_course":has_cl_course,
            "has_cl_org":has_cl_org,
        })


#view要求登录权限的两种方法
class CourseInfoView(LoginRequiredMixin, View):#方法2
    def get(self,request,course_id):
        #方法1：
        # if not request.user.is_authenticated():
        #     return render(request,"login.html",{})

        current_course = Course.objects.get(id=int(course_id))
        current_course.student_num += 1
        current_course.save()

        user_courses = UserCourse.objects.filter(user=request.user, course=current_course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=current_course)
            user_courses.save()

        return render(request,"course-video.html",{
            "current_course":current_course,
        })


class CommentsView(LoginRequiredMixin, View):
    def get(self,request,course_id):
        current_course = Course.objects.get(id=int(course_id))
        all_comments = current_course.get_course_comments()#可以再html中获取
        return render(request,"course-comment.html",{
            "current_course":current_course,
            "all_comments":all_comments,
        })


class AddCommentView(View):
    def post(self,request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type='application/json')

        course_id = request.POST.get("course_id",0)
        comment = request.POST.get("comment","")
        if course_id > 0 and comment :
            course = Course.objects.get(id=int(course_id))
            course_comment = CourseComments()
            course_comment.course = course
            course_comment.comments = comment
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse('{"status":"success","msg":"评论成功"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"评论失败"}',content_type='application/json')


class VideoPlayView(View):
    def get(self,request,video_id):
        video =Video.objects.get(id=video_id)
        current_course = video.lesson.course

        user_courses = UserCourse.objects.filter(user=request.user, course=current_course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=current_course)
            user_courses.save()

        return render(request,"course-play.html",{
            "current_course":current_course,
            "video":video,
        })