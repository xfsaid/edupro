# -*- coding: utf-8  -*-
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course
from operation.models import UserCollect

# Create your views here.


class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_num")[:3]

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


class CourseInfoView(View):
    def get(self,request,course_id):
        current_course = Course.objects.get(id=int(course_id))
        return render(request,"course-video.html",{
            "current_course":current_course,
        })

