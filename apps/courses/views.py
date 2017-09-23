# -*- coding: utf-8  -*-
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course
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

        return render(request, "course-detail.html",{
            "current_course":current_course,
        })
