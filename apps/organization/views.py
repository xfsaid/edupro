#_*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from .forms import UserAskForm

#https://github.com/jamespacileo/django-pure-pagination
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg,CityDict
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
