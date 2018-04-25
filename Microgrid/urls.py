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

from users.views import LoginView, LogoutView
from microgrids.views import OverviewView,DeviceManageView,DeviceAddView,DeviceDelView

urlpatterns = [
    url(r'^$', LoginView.as_view()),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^overview/$', OverviewView.as_view(), name='overview'),
    url(r'^device_manage/$', DeviceManageView.as_view(), name='device'),
    url(r'^dev_add/$', DeviceAddView.as_view(), name='dev_add'),
    url(r'^dev_del/$', DeviceDelView.as_view(), name='dev_del'),
    url(r'^xadmin/', xadmin.site.urls)
]
