# -*- coding:utf8 -*-
from django.shortcuts import render,HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.base import View

from microgrids.models import WebMicrogrid,DevControl,EnvAddressC

# Create your views here.


# 电站总览
class OverviewView(View):
    def get(self, request):
        # 导航栏选择标志
        nav = 1

        #
        return render(request, 'overview.html', {
            'nav': nav
        })


# 电站设备管理
class DeviceManageView(View):
    def get(self, request):
        # 导航栏选择标志
        nav = 2
        # 区域信息(目录一级)
        message_all = [[0, '间隔区'],[1, '光伏区'],[2, '风力区'],[3,'燃机区'],[4, '电池储能区'],[5, '飞轮储能区'],[6, '控制区'],[7, '环境']]
        # 获取所有子区域(目录二级)
        for area_type_num in message_all:
            area_infos = WebMicrogrid.objects.filter(area_type=area_type_num[0],type=1).values_list('num','name')
            # 一级目录3位置加list存储二级以下信息
            message_all[area_type_num[0]].append([])
            # 获取所有组区域(目录三级)
            for area_info in area_infos:
                # 二级信息元组变数组
                area_info = list(area_info)
                group_infos = WebMicrogrid.objects.filter(parent_area=area_info[0]).values_list('num', 'name')
                # 二级目录3位置加list存储三级以下信息
                area_info.append([])
                # 获取所有设备(目录四级)
                for group_info in group_infos:
                    group_info = list(group_info)
                    dev_infos = WebMicrogrid.objects.filter(parent_area=group_info[0]).values_list('num', 'name')
                    # 三级添加对应四级信息
                    group_info.append(dev_infos)
                    # 二级添加对应三级信息
                    area_info[2].append(group_info)
                # 一级添加对应二级信息
                message_all[area_type_num[0]][2].append(area_info)

        return render(request, 'device_manage.html', {
            'nav':nav,
            'message_all': message_all,
        })


# 设备添加
class DeviceAddView(View):
    def get(self, request):
        area_a = request.GET.get('area_a','') # 所属区域
        type = request.GET.get('type', '') # 所属级别
        pnum = request.GET.get('num', '') #设备上级num
        # 将要创建编号限定
        num = []
        # 创建编号的汉字标注
        num_h = ''
        # 如果创建子项的为总区域，即创建子区域
        if pnum == '':
            num_h = [[0, '间隔子区'], [1, '光伏子区'], [2, '风力子区'], [3, '燃机子区'], [4, '电池储能子区'], [5, '飞轮储能子区'], [6, '控制子区'], [7, '环境子区']][int(area_a)][1]
            # 控制区所创建子区会对应产生层或间隔层区域进行控制
            if area_a == '6':
                nums = []
                # 控制区所包含的num,即已被控制
                nums1 = WebMicrogrid.objects.filter(area_type=6).values_list('control_belong_id')
                for num1 in nums1:
                    nums.append(num1[0])
                # 取出产生层、间隔层所有num
                devs = WebMicrogrid.objects.exclude(area_type__in=[6,7]).values_list('num')
                for dev in devs:
                    if dev[0] not in nums:
                        num.append(dev[0])
        else:
            # 获取所有Web使用的num
            nums = []
            nums1 = WebMicrogrid.objects.values_list('num')
            for num1 in nums1:
                nums.append(num1[0])

            # 如果是光伏区设备组级(光伏逆变器)
            if area_a == '1' and type == '2':
                num_h = '光伏逆变器'
                devs = DevControl.objects.filter(dev_type=1).values_list('num')
                for dev in devs:
                    if dev[0] not in nums:
                        num.append(dev[0])
            # 如果是光伏区设备(光伏板)
            if area_a == '1' and type == '3':
                num_h = '光伏板'
                devs = DevControl.objects.filter(dev_type=2).values_list('num')
                for dev in devs:
                    if dev[0] not in nums:
                        num.append(dev[0])

            # 如果是风力区组级(风力逆变器)
            if area_a == '2' and type == '2':
                num_h = '风力逆变器'
                devs = DevControl.objects.filter().values_list('num')
                for dev in devs:
                    if dev[0] not in nums:
                        num.append(dev[0])
            # 如果是风力设备(风机)
            if area_a == '2' and type == '3':
                num_h = '风机'
                devs = DevControl.objects.filter().values_list('num')
                for dev in devs:
                    if dev[0] not in nums:
                        num.append(dev[0])

            # 如果是燃机区组级(燃机逆变器)
            if area_a == '3' and type == '2':
                num_h = '燃机逆变器'
                devs = DevControl.objects.filter().values_list('num')
                for dev in devs:
                    if dev[0] not in nums:
                        num.append(dev[0])
            # 如果是燃机设备(燃料电池)
            if area_a == '3' and type == '3':
                num_h = '燃料电池'
                devs = DevControl.objects.filter().values_list('num')
                for dev in devs:
                    if dev[0] not in nums:
                        num.append(dev[0])

            # 如果是蓄电池区组级(蓄电池逆变器)
            if area_a == '4' and type == '2':
                num_h = '蓄电池逆变器'
                devs = DevControl.objects.filter(dev_type=3).values_list('num')
                for dev in devs:
                    if dev[0] not in nums:
                        num.append(dev[0])
            # 如果是蓄电池设备(蓄电池)
            if area_a == '4' and type == '3':
                devs = DevControl.objects.filter(dev_type=4).values_list('num')
                for dev in devs:
                    if dev[0] not in nums:
                        num.append(dev[0])
            # 如果是飞轮区组级(飞轮逆变器)
            if area_a == '5' and type == '2':
                num_h = '飞轮逆变器'
                devs = DevControl.objects.filter().values_list('num')
                for dev in devs:
                    if dev[0] not in nums:
                        num.append(dev[0])

            # 如果是飞轮设备(飞轮)
            if area_a == '5' and type == '3':
                num_h = '飞轮'
                devs = DevControl.objects.filter().values_list('num')
                for dev in devs:
                    if dev[0] not in nums:
                        num.append(dev[0])

            # 如果是控制区组级
            if area_a == '6' and type == '2':
                num_h = '控制区'
                devs = DevControl.objects.filter(dev_type__in=[5,6,7]).values_list('num')
                for dev in devs:
                    if dev[0] not in nums:
                        num.append(dev[0])

            # 如果是环境区组
            if area_a == '7' and type == '2':
                num_h = "环境地址"
                addrs = EnvAddressC.objects.values_list('env_num')
                for addr in addrs:
                    if addr[0] not in nums:
                        num.append(addr[0])

        return render(request, 'dev_add.html', {
            'area_a': area_a,
            'num': num,
            'pnum': pnum,
            'num_h': num_h,
            'type': type
        })

    def post(self, reqeust):
        dev_num = reqeust.POST.get('dev_num', '')
        parent_area = reqeust.POST.get('parent_area', '')
        dev_name = reqeust.POST.get('dev_name', '')
        remark = reqeust.POST.get('remark', '')
        area_a = reqeust.POST.get('area_a', '')
        type = reqeust.POST.get('type','')
        control_belong = reqeust.POST.get('control_belong', '')
        dev = WebMicrogrid()
        dev.num = dev_num
        dev.name = dev_name
        dev.remark = remark
        dev.area_type = int(area_a)
        dev.type = int(type)
        if parent_area != '':
            dev.parent_area_id = parent_area
        if control_belong != '':
            dev.control_belong_id = control_belong
        dev.save()
        return HttpResponseRedirect(reverse('device'))


# 设备删除
class DeviceDelView(View):
    def get(self, request):
        num = request.GET.get('num', '')
        num = WebMicrogrid.objects.get(num=num)
        num.delete()
        return HttpResponseRedirect(reverse('device'))

