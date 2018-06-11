"""Microgrid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
import xadmin
from Microgrid.settings import MEDIA_ROOT
from django.views.static import serve
from django.contrib.auth.decorators import login_required

from users.views import LoginView, LogoutView
from microgrids.views import OverviewView,DeviceManageView,DeviceAddView,DeviceDelView,DeviceAskView,DeviceInfoView,PsoView

urlpatterns = [
    url(r'^$', LoginView.as_view()),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    # 总览
    url(r'^overview/$', login_required(OverviewView.as_view()), name='overview'),
    # 设备管理
    url(r'^device_manage/$', login_required(DeviceManageView.as_view()), name='device'),
    # 左侧栏设备添加删除管理
    url(r'^dev_add/$', login_required(DeviceAddView.as_view()), name='dev_add'),
    url(r'^dev_del/$', login_required(DeviceDelView.as_view()), name='dev_del'),
    # 设备请求(区域设备控制)
    url(r'^dev_ask/$', login_required(DeviceAskView.as_view()), name='dev_ask'),
    # 设备详情(波形和报警信息)
    url(r'^dev_info/$', login_required(DeviceInfoView.as_view()), name='dev_info'),

    # PSO优化管理界面
    url(r'^pso/$', login_required(PsoView.as_view()), name='pso'),

    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^xadmin/', xadmin.site.urls)
]
