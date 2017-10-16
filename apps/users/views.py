#_*_ encoding:utf-8 _*_
import json
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.views.generic.base import View
from django.http import HttpResponse,HttpResponsePermanentRedirect


from .models import UserProfile,EmailVerifyRecord
from .forms import LoginForm,RegisterForm,ForgetPwdForm,ModifyPwdForm
from .forms import UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse,UserCollect,UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course


#自定义user验证函数
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

# Create your views here.
def login_view(request):
    if request.method == "POST":
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            login(request, user)
            return render(request, "index.html")
        else:
            return render(request, "login.html",{"msg":"用户名或者密码错误！"})
    elif request.method == "GET":
        return render(request, "login.html", {})


class LogoutView(View):
    def get(self, request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponsePermanentRedirect(reverse("index"))


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html",{"msg":"用户名未激活！"})
            else:
                return render(request, "login.html",{"msg":"用户名或者密码错误！"})
        else:
            return render(request, "login.html",{"login_form":login_form})


class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, "register.html",{"register_form":register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(Q(username=user_name)|Q(email=user_name)):
                return render(request, "register.html",{"register_form":register_form,"msg":"账号已存在"})

            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.is_active = False
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.save()

            #welcome
            user_message = UserMessage()
            user_message.user_id = user_profile.id
            user_message.message = "欢迎注册EDU在线"
            user_message.save()

            send_register_email(user_name, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html",{"register_form":register_form})


class ActiveUserView(View):
    def get(self,request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                return render(request, "login.html")
        else:
            return render(request,"active_fail.html", {"active_result":"连接错误或已失效！"})


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request,"forgetpwd.html",{"forget_form":forget_form})

    def post(self,request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email","")
            send_register_email(email,"forget")
            return render(request,"send_result.html",{})
        else:
            return render(request,"forgetpwd.html",{"forget_form":forget_form})


class ResetView(View):
    def get(self,request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                return render(request,"password_reset.html",{"email":email})
        else:
            return render(request,"confirmation.html", {"confirm_result":"连接错误或已失效！"})


#TODO 添加验证码过期时间
class ModifyPwdView(View):
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        email = request.POST.get("email","")
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2","")
            if pwd1 != pwd2:
                return render(request,"password_reset.html",{"email":email,"msg":"两次输入不一致！"})

            user_profile = UserProfile.objects.get(email=email)
            user_profile.password = make_password(pwd1)
            user_profile.save()
            return render(request,"login.html")
        else:
            return render(request,"password_reset.html",{"email":email,"modify_form":modify_form})


class UserInofView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html',{})

    def post(self, request):
        #修改，需要指明要修改的实例,不指明实例，save会新增
        userinfo_form = UserInfoForm(request.POST, instance=request.user)
        if userinfo_form.is_valid():
            userinfo_form.save()
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse(json.dumps(userinfo_form.errors),content_type='application/json')



class UserUploadImageView(LoginRequiredMixin, View):
    #方法1 TODO 需要理解
    #def post(self,request):
    #    image_form = UploadImageForm(request.POST, request.FILES)
    #    if image_form.is_valid():
    #        image = image_form.cleaned_data['image']
    #        request.user.image = image
    #        request.user.save()

    #方法2 TODO 需要理解
    def post(self,request):
       image_form = UploadImageForm(request.POST, request.FILES,instance=request.user)
       if image_form.is_valid():
           image_form.save()
           return HttpResponse('{"status":"success"}',content_type='application/json')
       else:
           return HttpResponse('{"status":"fail"}',content_type='application/json')


class UserUpdatePwdView(View):
    """
    个人中心中修改密码，不需要邮箱验证
    """
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2","")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}',content_type='application/json')

            user_profile = request.user
            user_profile.password = make_password(pwd1)
            user_profile.save()
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors),content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email','')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}',content_type='application/json')
        send_register_email(email,'update_email')
        return HttpResponse('{"status":"success"}',content_type='application/json')


class UpdateEmailView(View):
    def post(self, request):
        email = request.POST.get('email','')
        code = request.POST.get('code','')

        if EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email'):
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码错误"}',content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html',{
            "user_courses":user_courses,
        })


class MyCollectOrgView(LoginRequiredMixin, View):
    def get(self, request):
        org_list = []
        collects = UserCollect.objects.filter(user=request.user, collect_type=2)
        for collect in collects:
            org = CourseOrg.objects.get(id=collect.collect_id)
            if org:
                org_list.append(org)

        return render(request, 'usercenter-fav-org.html', {
            "org_list":org_list,
        })


class MyCollectTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        teacher_list = []
        collects = UserCollect.objects.filter(user=request.user, collect_type=3)
        for collect in collects:
            teacher = Teacher.objects.get(id=collect.collect_id)
            if teacher:
                teacher_list.append(teacher)

        return render(request, 'usercenter-fav-teacher.html', {
            "teacher_list":teacher_list,
        })


class MyCollectCourseView(LoginRequiredMixin, View):
    def get(self, request):
        course_list = []
        collects = UserCollect.objects.filter(user=request.user, collect_type=1)
        for collect in collects:
            course = Course.objects.get(id=collect.collect_id)
            if course:
                course_list.append(course)

        return render(request, 'usercenter-fav-course.html', {
            "course_list":course_list,
        })


class MyMessageView(LoginRequiredMixin, View):
    def get(self, request):
        unread_msgs = UserMessage.objects.filter(user_id=request.user.id, has_read=False)
        for unread_msg in unread_msgs:
            unread_msg.has_read = True
            unread_msg.save()

        all_messages = UserMessage.objects.filter(user_id=request.user.id)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, 1, request=request)#每页显示条数
        page_messages = p.page(page)

        return render(request, 'usercenter-message.html',{
            "all_messages":page_messages,
        })