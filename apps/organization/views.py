#_*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q

#https://github.com/jamespacileo/django-pure-pagination
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .forms import UserAskForm
from .models import CourseOrg,CityDict,Teacher
from courses.models import Course
from operation.models import UserCollect

# Create your views here.


class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_num")[:3]
        all_citys = CityDict.objects.all()

        city_id = request.GET.get("city","")
        if city_id == "":
            city_id = 0
        city_id = int(city_id)

        if city_id:
            all_orgs = all_orgs.filter(city_id=city_id)

        #搜索功能
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords))

        category = request.GET.get("ct","")
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get("sort","")
        if sort:
            if sort == "student_num":
                all_orgs = all_orgs.order_by("-student_num")
            elif sort == "course_num":
                all_orgs = all_orgs.order_by("-course_num")


        org_num = all_orgs.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 1, request=request)#每页显示条数
        page_orgs = p.page(page)

        return render(request, "org-list.html",{
            "all_orgs":page_orgs,
            "org_num":org_num,
            "all_citys":all_citys,
            "city_id":city_id,
            "category":category,
            "hot_orgs":hot_orgs,
            "sort":sort,
        })


class AddUserAskView(View):
    def post(self,request):
        user_ask_form = UserAskForm(request.POST)
        if user_ask_form.is_valid():
            user_ask = user_ask_form.save(commit=True)
            #return HttpResponse("{'status':'success'}",content_type='application/json')
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            #return HttpResponse("{'status':'fail','msg':'添加出错'}",content_type='application/json')
            return HttpResponse('{"status":"fail","msg":"添加出错"}',content_type='application/json')


class OrgHomeView(View):
    def get(self,request, org_id):
        has_collect = False
        current_page = "home"

        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_num += 1
        course_org.save()

        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:2]

        if request.user.is_authenticated():
            if UserCollect.objects.filter(user=request.user,collect_id=course_org.id, collect_type=2):
                has_collect = True

        return render(request,'org-detail-homepage.html',{
            "all_courses":all_courses,
            "all_teachers":all_teachers,
            "course_org":course_org,
            "current_page":current_page,
            "has_collect":has_collect,
        })


class OrgCourseView(View):
    def get(self,request, org_id):
        has_collect = False
        current_page = "course"

        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()

        if request.user.is_authenticated():
            if UserCollect.objects.filter(user=request.user,collect_id=course_org.id, collect_type=2):
                has_collect = True

        return render(request,'org-detail-course.html',{
            "all_courses":all_courses,
            "course_org":course_org,
            "current_page":current_page,
            "has_collect":has_collect,
        })


class OrgDescView(View):
    def get(self,request, org_id):
        has_collect = False
        current_page = "desc"

        course_org = CourseOrg.objects.get(id=int(org_id))
        #all_courses = course_org.course_set.all()

        if request.user.is_authenticated():
            if UserCollect.objects.filter(user=request.user,collect_id=course_org.id, collect_type=2):
                has_collect = True

        return render(request,'org-detail-desc.html',{
            "course_org":course_org,
            "current_page":current_page,
            "has_collect":has_collect,
        })


class OrgTeacherView(View):
    def get(self,request, org_id):
        has_collect = False
        current_page = "teacher"

        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()

        if request.user.is_authenticated():
            if UserCollect.objects.filter(user=request.user,collect_id=course_org.id, collect_type=2):
                has_collect = True

        return render(request,'org-detail-teachers.html',{
            "all_teachers":all_teachers,
            "course_org":course_org,
            "current_page":current_page,
            "has_collect":has_collect,
        })


class AddCollectView(View):
    def post(self,request):
        collect_id = request.POST.get("collect_id",0)
        collect_type = request.POST.get("collect_type",0)
        collect_id = int(collect_id)
        collect_type = int(collect_type)

        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type='application/json')

        exist_records = UserCollect.objects.filter(user=request.user,collect_id=collect_id, collect_type=collect_type)
        if exist_records:
            exist_records.delete()

            coll_obj = None
            if collect_type == 1:#kecheng
                coll_obj = Course.objects.get(id=collect_id)
            elif collect_type == 2:#jigou
                coll_obj = CourseOrg.objects.get(id=collect_id)
            elif collect_type == 3:#jiangshi
                coll_obj = Teacher.objects.get(id=collect_id)

            if coll_obj:
                coll_obj.collect_num -= 1
                if coll_obj.collect_num < 0:
                    coll_obj.collect_num = 0
                coll_obj.save()

            return HttpResponse('{"status":"success","msg":"收藏"}',content_type='application/json')
        else:
            user_collect = UserCollect()
            if collect_id > 0 and collect_type > 0:
                user_collect.user = request.user
                user_collect.collect_id = collect_id
                user_collect.collect_type = collect_type
                user_collect.save()

                coll_obj = None
                if collect_type == 1:#kecheng
                    coll_obj = Course.objects.get(id=collect_id)
                elif collect_type == 2:#jigou
                    coll_obj = CourseOrg.objects.get(id=collect_id)
                elif collect_type == 3:#jiangshi
                    coll_obj = Teacher.objects.get(id=collect_id)

                if coll_obj:
                    coll_obj.collect_num += 1
                    coll_obj.save()

                return HttpResponse('{"status":"success","msg":"已收藏"}',content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}',content_type='application/json')


class TeacherListView(View):
    def get(self,request):
        all_teachers = Teacher.objects.all()

        #搜索功能
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_teachers = all_teachers.filter(name__icontains=search_keywords)

        sort = request.GET.get("sort","")
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_num")

        sorted_teachers = Teacher.objects.all().order_by("-click_num")[:3]

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 1, request=request)#每页显示条数
        page_teachers = p.page(page)
        return render(request,"teachers-list.html",{
            "all_teachers":page_teachers,
            "sorted_teachers":sorted_teachers,
            "sort":sort,
        })


class TeacherDetailView(View):
    def get(self,request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_num += 1
        teacher.save()

        all_courses = Course.objects.filter(teacher=teacher)
        sorted_teachers = Teacher.objects.all().order_by("-click_num")[:3]

        has_teacher_coll = False
        has_org_coll = False

        if UserCollect.objects.filter(user=request.user, collect_id=teacher.id,collect_type=3):
            has_teacher_coll = True

        if UserCollect.objects.filter(user=request.user, collect_id=teacher.org.id,collect_type=2):
            has_org_coll = True

        return render(request, "teacher-detail.html", {
            "teacher":teacher,
            "all_courses":all_courses,
            "sorted_teachers":sorted_teachers,
            "has_teacher_coll":has_teacher_coll,
            "has_org_coll":has_org_coll,
        })