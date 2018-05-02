# -*- coding:utf8 -*-
from django.shortcuts import render,HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.base import View

from microgrids.models import WebMicrogrid,DevControl,EnvAddressC,Img

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
        # 获取右侧栏需要显示的对应控制区内容的编号
        control_num = request.GET.get('control_num', '')
        # 导航栏选择标志
        nav = 2

        # 左侧微电网设备管理栏
        # 区域信息(目录一级)
        message = [[0, '间隔区'],[1, '光伏区'],[2, '风力区'],[3,'燃机区'],[4, '电池储能区'],[5, '飞轮储能区'],[6, '控制区'],[7, '环境']]
        # 左侧栏所有信息存储(先存储一级目录信息)
        message_left = message
        # 获取所有子区域(目录二级)
        for area_type_num in message_left:
            area_infos = WebMicrogrid.objects.filter(area_type=area_type_num[0],type=1).order_by('name').values_list('num','name')
            # 一级目录3位置加list存储二级以下信息
            message_left[area_type_num[0]].append([])
            # 获取所有组区域(目录三级)
            for area_info in area_infos:
                # 二级信息元组变数组
                area_info = list(area_info)
                group_infos = WebMicrogrid.objects.filter(parent_area=area_info[0]).order_by('name').values_list('num', 'name')
                # 二级目录3位置加list存储三级以下信息
                area_info.append([])
                # 获取所有设备(目录四级)
                for group_info in group_infos:
                    group_info = list(group_info)
                    dev_infos = WebMicrogrid.objects.filter(parent_area=group_info[0]).order_by('name').values_list('num', 'name')
                    # 三级添加对应四级信息
                    group_info.append(dev_infos)
                    # 二级添加对应三级信息
                    area_info[2].append(group_info)
                # 一级添加对应二级信息
                message_left[area_type_num[0]][2].append(area_info)
        print(message_left)

        # 中间模型展示栏
        # 中间栏所需图片
        big_power_grid_picture = Img.objects.get(name_h='大电网')
        pvI_picture = Img.objects.get(name_h='光伏逆变器')
        pv_picture = Img.objects.get(name_h='光伏阵列')
        BI_picture = Img.objects.get(name_h='蓄电池逆变器')
        battery_picture = Img.objects.get(name_h='蓄电池组')
        CA_Close_picture = Img.objects.get(name_h='控制区_闭合')
        CA_Open_picture = Img.objects.get(name_h='控制区_断开')
        # 光伏模型区
        pv_model = []
        # 获取光伏下的所有控制子区
        pas = WebMicrogrid.objects.order_by('num').filter(area_type=message[1][0],type=1).values_list('num')
        for pa in pas:
            # 创建2级即子区保存数组
            pv_2 = []
            try:
                # 获取对应控制区
                pac = WebMicrogrid.objects.order_by('num').filter(control_belong__num=pa[0]).values_list('num')[0][0]
                # 获取控制区状态
                pac_sws = WebMicrogrid.objects.filter(parent_area=pac)
                # 默认闭合
                pac_status = 2
                for pac_sw in pac_sws:
                    pac_sw_status = DevControl.objects.get(num=pac_sw).switch_status
                    if pac_sw_status == 1:
                        # 控制区有一个断开，则显示控制区断开
                        pac_status = 1
            except:
                pac = ''
                pac_status = ''
            # 追加子区编号和对应控制区编号和三级总容器
            pv_2.append(pa[0])
            pv_2.append(pac)
            pv_2.append(pac_status)
            pv_2.append([])
            # 获取子区下的所有逆变器
            pvIs = WebMicrogrid.objects.order_by('num').filter(parent_area=pa[0]).values_list('num')
            for pvI in pvIs:
                # 创建保存3级即逆变器数组
                pv_3 = []
                try:
                    # 获取逆变器对应控制区(如果逆变器对应无控制区为'')
                    pvIc = WebMicrogrid.objects.order_by('num').filter(control_belong__num=pvI[0]).values_list('num')[0][0]
                    # 获取控制区状态
                    pvIc_sws = WebMicrogrid.objects.filter(parent_area=pvIc)
                    # 默认闭合
                    pvIc_status = 2
                    for pvIc_sw in pvIc_sws:
                        pvIc_sw_status = DevControl.objects.get(num=pvIc_sw).switch_status
                        if pvIc_sw_status == 1:
                            # 控制区有一个断开，则显示控制区断开
                            pvIc_status = 1
                except:
                    pvIc = ''
                    pvIc_status = ''
                # 获取逆变器控制编号和逆变器编号及四级总容器
                pv_3.append(pvIc)
                pv_3.append(pvI[0])
                pv_3.append(pvIc_status)
                pv_3.append([])
                # 获取逆变器下所有的光伏阵列
                pvs = WebMicrogrid.objects.order_by('num').filter(parent_area=pvI[0]).values_list('num')
                for pv in pvs:
                    # 创建保存4级即光伏阵列的数组
                    pv_4 = []
                    try:
                        # 获取光伏阵列对应控制区(如果光伏阵列对应无控制区为'')
                        pvc = WebMicrogrid.objects.order_by('num').filter(control_belong__num=pv[0]).values_list('num')[0][0]
                        # 获取控制区状态
                        pvc_sws = WebMicrogrid.objects.filter(parent_area=pvc)
                        # 默认闭合
                        pvc_status = 2
                        for pvc_sw in pvc_sws:
                            pvc_sw_status = DevControl.objects.get(num=pvc_sw).switch_status
                            if pvc_sw_status == 1:
                                # 控制区有一个断开，则显示控制区断开
                                pvc_status = 1
                    except:
                        pvc = ''
                        pvc_status = ''
                    # 获取逆变器下所有光伏阵列控制编号和光伏阵列编号及五级容器(备用)
                    pv_4.append(pvc)
                    pv_4.append(pv[0])
                    pv_4.append([])
                    pv_3[3].append(pv_4)
                pv_2[3].append(pv_3)
            pv_model.append(pv_2)
        print(pv_model)

        # 右侧栏设备控制管理栏
        swcs = []
        if control_num != '':
            # 首位为控制编号
            swcs.append(control_num)
            swcs.append([])
            # 获取对应编号的对象
            control_obj = WebMicrogrid.objects.get(num=control_num)
            # 如果对象为子区
            if control_obj.type == 1:
                # 获取子区对象下所有的控制开关
                sws = WebMicrogrid.objects.filter(parent_area=control_obj.num).values_list('num')
                for sw in sws:
                    swc = DevControl.objects.filter(num=sw[0]).values_list('num','switch_status')
                    swcs[1].append(swc)
            elif control_obj.type == 2:
                swc = DevControl.objects.filter(num=control_obj.num).values_list('num', 'switch_status')
                swcs[1].append(swc)
        print(swcs)
        return render(request, 'device_manage.html', {
            'nav':nav,
            'message_left': message_left,
            'pv_model':pv_model,
            'big_power_grid_picture': big_power_grid_picture,
            'pvI_picture': pvI_picture,
            'pv_picture': pv_picture,
            'BI_picture': BI_picture,
            'battery_picture': battery_picture,
            'CA_Close_picture':CA_Close_picture,
            'CA_Open_picture':CA_Open_picture,
            'swcs': swcs
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
                devs = WebMicrogrid.objects.exclude(area_type__in=[6,7]).order_by('num').values_list('num')
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


# 设备请求控制或查看详情处理
class DeviceAskView(View):
    def get(self, request):
        ask_dev = request.GET.get('ask_dev','')
        # 获取设备信息
        dev = WebMicrogrid.objects.get(num=ask_dev)

        # 控制区处理(返回请求所需的控制开关编号及状态)
        if dev.area_type == 6:
            # 如果是控制区,交给manage处理
            control_num = dev.num
            return HttpResponseRedirect('/device_manage/?control_num={0}'.format(control_num))

    def post(self, request):
        control_num = request.POST.get('control_num','')
        print(control_num)
        sw_num = request.POST.get('sw_num', '')
        sw_status = request.POST.get('sw_status', '')
        # 获取对应开关并设置状态
        sw = DevControl.objects.get(num=sw_num)
        sw.switch_status = sw_status
        sw.save()

        return HttpResponseRedirect('/device_manage/?control_num={0}'.format(control_num))