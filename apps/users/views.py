from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import View
from django.contrib.auth import authenticate,login,logout

from users.forms import LoginForm

# Create your views here.


#登录
class LoginView(View):
    def get(self, request):
        # 用户登录状态直接跳转（cookie）
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('overview'))
        login_form = LoginForm()
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        # form验证是否正确
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            # 用户是否存在
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('overview'))
            else:
                return render(request, 'login.html', {'msg': u'密码错误或用户不存在', 'login_form': login_form})
        else:
            return render(request, 'login.html', {'login_form': login_form})


# 登出
class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'login.html', {})