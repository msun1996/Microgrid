# -*- coding:utf8 -*-
import datetime
import json
# 粒子群算法使用数学库
import numpy as np
import random

from django.shortcuts import render,HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.base import View

from microgrids.models import WebMicrogrid,DevControl,EnvAddressC,Img,PVDigitalQuantityData,PVAnalogQuantityData1,PVAnalogQuantityData2,BattatyProperty

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
        ask_dev = request.GET.get('ask_dev', '')
        # 导航栏选择标志
        nav = 2

        # 左侧微电网设备管理栏
        # 区域信息(目录一级)
        message = [[0, '间隔区'],[1, '光伏区'],[2, '风力区'],[3,'燃机区'],[4, '电池储能区'],[5, '飞轮储能区'],[6, '负载区'],[7, '控制区'],[8, '环境']]
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
        load_picture = Img.objects.get(name_h='负荷')


        # 间隔区
        pcc_model = []
        pccs = WebMicrogrid.objects.order_by('num').filter(area_type=message[0][0], type=1).values_list('num')
        for pcc in pccs:
            # 获取对应控制区区号
            pcc_2 = []
            try:
                # 获取对应控制区
                pccc = WebMicrogrid.objects.order_by('num').filter(control_belong__num=pcc[0]).values_list('num')[0][0]
                # 获取对应控制区状态
                pcc_sws = WebMicrogrid.objects.filter(parent_area=pccc)
                # 默认闭合
                pcc_status = 1
                for pcc_sw in pcc_sws:  # 控制区可能有多个开关时判断
                    pcc_sw_status = DevControl.objects.get(num=pcc_sw).switch_status
                    if pcc_sw_status == 1:
                        # 控制区有一个断开，则显示控制区断开
                        pcc_status = 0
            except:
                pccc = ''
                pcc_status = ''
            pcc_2.append(pcc[0])
            pcc_2.append(pccc)
            pcc_2.append(pcc_status)
            pcc_model.append(pcc_2)
        print(pcc_model)

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
                pac_status = 1
                for pac_sw in pac_sws:
                    pac_sw_status = DevControl.objects.get(num=pac_sw).switch_status
                    if pac_sw_status == 1:
                        # 控制区有一个断开，则显示控制区断开
                        pac_status = 0
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
                    pvIc_status = 1
                    for pvIc_sw in pvIc_sws:
                        pvIc_sw_status = DevControl.objects.get(num=pvIc_sw).switch_status
                        if pvIc_sw_status == 1:
                            # 控制区有一个断开，则显示控制区断开
                            pvIc_status = 0
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
                        pvc_status = 1
                        for pvc_sw in pvc_sws:
                            pvc_sw_status = DevControl.objects.get(num=pvc_sw).switch_status
                            if pvc_sw_status == 1:
                                # 控制区有一个断开，则显示控制区断开
                                pvc_status = 0
                    except:
                        pvc = ''
                        pvc_status = ''
                    # 获取逆变器下所有光伏阵列或蓄电池控制编号和光伏阵列或蓄电池编号及五级容器(备用)
                    pv_4.append(pvc)
                    pv_4.append(pv[0])
                    pv_4.append([])
                    pv_3[3].append(pv_4)
                pv_2[3].append(pv_3)
            pv_model.append(pv_2)
        print(pv_model)

        # 负载区
        load_model = []
        # 获取负载的所有控制子区
        las =  WebMicrogrid.objects.order_by('num').filter(area_type=message[6][0],type=1).values_list('num')
        for la in las:
            # 创建2级即子区保存数组
            l_2 = []
            try:
                # 获取对应控制区
                lac = WebMicrogrid.objects.order_by('num').filter(control_belong__num=la[0]).values_list('num')[0][0]
                # 获取控制区状态
                lac_sws = WebMicrogrid.objects.filter(parent_area=lac)
                # 默认闭合
                lac_status = 1
                for lac_sw in lac_sws:
                    lac_sw_status = DevControl.objects.get(num=lac_sw).switch_status
                    if lac_sw_status == 1:
                        # 控制区有一个断开，则显示控制区断开
                        lac_status = 0
            except:
                lac = ''
                lac_status = ''
            # 追加子区编号和对应控制区编号和三级总容器
            l_2.append(la[0])
            l_2.append(lac)
            l_2.append(lac_status)
            l_2.append([])
            # 获取子区下的所有负载
            ls = WebMicrogrid.objects.order_by('num').filter(parent_area=la[0]).values_list('num')
            for load in ls:
                # 创建保存3级即负载数组
                l_3 = []
                try:
                    # 获取逆变器对应控制区(如果逆变器对应无控制区为'')
                    lc = WebMicrogrid.objects.order_by('num').filter(control_belong__num=load[0]).values_list('num')[0][0]
                    # 获取控制区状态
                    lc_sws = WebMicrogrid.objects.filter(parent_area=lc)
                    # 默认闭合
                    lc_status = 1
                    for lc_sw in lc_sws:
                        lc_sw_status = DevControl.objects.get(num=lc_sw).switch_status
                        if lc_sw_status == 1:
                            # 控制区有一个断开，则显示控制区断开
                            l_status = 0
                except:
                    lc = ''
                    lc_status = ''
                # 获取逆变器控制编号和逆变器编号及四级总容器
                l_3.append(lc)
                l_3.append(load[0])
                l_3.append(lc_status)
                l_3.append([])
                l_2[3].append(l_3)
            load_model.append(l_2)
        print(load_model)

        # #################################### 右侧栏设备控制管理栏  #########################
        try:
            dev = WebMicrogrid.objects.get(num=ask_dev)
        except:
            dev = ''
        # 处于控制区的开关部分处理
        swcs = []
        if ask_dev != ''and dev.area_type == 7:
            # 首位为控制编号
            swcs.append(ask_dev)
            swcs.append([])
            # 获取对应编号的对象
            control_obj = WebMicrogrid.objects.get(num=ask_dev)
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
        # 设备上的参数设定等管理
        dev_c = ''
        if ask_dev != '' and dev.area_type in [1,2,3,4,5,6]:
            dev_c = DevControl.objects.get(num=ask_dev)

        return render(request, 'device_manage.html', {
            'nav':nav,
            # 左侧
            'message_left': message_left,

            # 中间信息
            'pcc_model':pcc_model,
            'pv_model':pv_model,
            'load_model':load_model,
            'big_power_grid_picture': big_power_grid_picture,
            'pvI_picture': pvI_picture,
            'pv_picture': pv_picture,
            'BI_picture': BI_picture,
            'battery_picture': battery_picture,
            'CA_Close_picture':CA_Close_picture,
            'CA_Open_picture':CA_Open_picture,
            'load_picture':load_picture,

            # 右侧栏
            'swcs': swcs,
            'dev_c': dev_c,
        })


# 设备详情
class DeviceInfoView(View):
    def get(self, request):
        num = request.GET.get('num', '')
        type = request.GET.get('type','')
        # 光伏逆变器
        if type == '1':
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            day = request.GET.get('day', today)
            date = request.GET.get('date', 'day')
            day_l = day.split('-')
            # 监控信息获取
            pvI_monitor = PVDigitalQuantityData.objects.get(pv_num=num)
            # 数据信息(最新)
            pvI_data2 = PVAnalogQuantityData2.objects.filter(pv_num=num).order_by('-timestamp').first()
            # 波形显示
            # 功率数据
            pvI_on_grid_p_data_l = []
            # 时间集
            time_l = []
            if date == 'day':
                # 获取对应编号指定日期数据
                pvI_datas2 = PVAnalogQuantityData2.objects.filter(pv_num=num).filter(timestamp__year=day_l[0],timestamp__month=day_l[1],timestamp__day=day_l[2])
                pvI_on_grid_p_datas = pvI_datas2.values_list('on_grid_p')
                for pvI_on_grid_p_data in pvI_on_grid_p_datas:
                    pvI_on_grid_p_data_l.append(pvI_on_grid_p_data[0])
                times = pvI_datas2.values_list('timestamp')
                for time in times:
                    time_l.append(time[0].strftime('%H:%M:%S'))
            elif date == 'month':
                # 获取对应编号日期数据
                for date_day in range(1, 31):
                    pvI_on_grid_p_datas = PVAnalogQuantityData2.objects.filter(pv_num=num).filter(timestamp__year=day_l[0],timestamp__month=day_l[1],timestamp__day=date_day).values_list('on_grid_p')
                    pvI_on_grid_p_data_day = 0
                    for pvI_on_grid_p_data in pvI_on_grid_p_datas:
                            pvI_on_grid_p_data_day = pvI_on_grid_p_data_day + pvI_on_grid_p_data[0]
                    pvI_on_grid_p_data_l.append(pvI_on_grid_p_data_day)
                    time_l.append(date_day)
                    print(time_l)
            # 三相电压实时n个数据
            volt_ab_dates = []
            volt_bc_dates = []
            volt_ca_dates = []
            volt_time_dates = []
            volt_dates = PVAnalogQuantityData1.objects.filter(pv_num=num).order_by('-id')[:10000]
            for volt_ab_date in volt_dates.values_list('grid_volt_ab'):
                volt_ab_dates.insert(0,volt_ab_date[0])
            for volt_bc_date in volt_dates.values_list('grid_volt_bc'):
                volt_bc_dates.insert(0,volt_bc_date[0])
            for volt_ca_date in volt_dates.values_list('grid_volt_ca'):
                volt_ca_dates.insert(0,volt_ca_date[0])
            for volt_time_date in volt_dates.values_list('timestamp'):
                volt_time_dates.insert(0,str(volt_time_date[0]))

            return render(request, 'dev_info_pv.html', {
                'num': num,
                'type': type,
                'pvI_monitor': pvI_monitor,
                'pvI_data2': pvI_data2,
                'day': day,
                'date':date,
                # 光伏逆变器功率数据
                'pvI_on_grid_p_data_l': json.dumps(pvI_on_grid_p_data_l),
                'time_l':json.dumps(time_l),
                # 光伏三相电压
                'volt_ab_dates':json.dumps(volt_ab_dates),
                'volt_bc_dates':json.dumps(volt_bc_dates),
                'volt_ca_dates':json.dumps(volt_ca_dates),
                'volt_time_dates':json.dumps(volt_time_dates)
            })
        # 蓄电池
        if type == '12':
            # 属性信息
            try:
                battaryproperty = BattatyProperty.objects.get(battary_num=num)
            except:
                battaryproperty = BattatyProperty()
                battaryproperty.battary_num = num
                battaryproperty.save()

            # 电池状态信息

            return render(request, 'dev_info_battary.html', {
                'battaryproperty': battaryproperty
            })
        # 负载
        if type == '30':


            return render(request, 'dev_info_load.html', {

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
            num_h = [[0, '间隔子区'], [1, '光伏子区'], [2, '风力子区'], [3, '燃机子区'], [4, '电池储能子区'], [5, '飞轮储能子区'], [6, '负载子区'],[7, '控制子区'], [8, '环境子区']][int(area_a)][1]
            # 控制区所创建子区会对应产生层或间隔层区域进行控制
            if area_a == '7':
                nums = []
                # 控制区所包含的num,即已被控制
                nums1 = WebMicrogrid.objects.filter(area_type=7).values_list('control_belong_id')
                for num1 in nums1:
                    nums.append(num1[0])
                # 取出产生层、间隔层所有num
                devs = WebMicrogrid.objects.exclude(area_type__in=[7,8]).order_by('num').values_list('num')
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
            # 如果是光伏区设备(光伏板或蓄电池)
            if area_a == '1' and type == '3':
                num_h = '光伏板/蓄电池'
                devs = DevControl.objects.filter(dev_type__in=[2, 12]).values_list('num')
                for dev in devs:
                    if dev[0] not in nums:
                        num.append(dev[0])

            # 如果是风力区组级(风力逆变器)
            if area_a == '2' and type == '2':
                num_h = '风力逆变器'
                devs = DevControl.objects.filter(dev_type=3).values_list('num')
                for dev in devs:
                    if dev[0] not in nums:
                        num.append(dev[0])
            # 如果是风力设备(风机)
            if area_a == '2' and type == '3':
                num_h = '风机'
                devs = DevControl.objects.filter(dev_type=4).values_list('num')
                for dev in devs:
                    if dev[0] not in nums:
                        num.append(dev[0])

            # 如果是燃机区组级(燃机逆变器)
            if area_a == '3' and type == '2':
                num_h = '燃机逆变器'
                devs = DevControl.objects.filter(dev_type=5).values_list('num')
                for dev in devs:
                    if dev[0] not in nums:
                        num.append(dev[0])
            # 如果是燃机设备(燃料电池)
            if area_a == '3' and type == '3':
                num_h = '燃料电池'
                devs = DevControl.objects.filter(dev_type=6).values_list('num')
                for dev in devs:
                    if dev[0] not in nums:
                        num.append(dev[0])

            # 如果是蓄电池区组级(蓄电池逆变器)
            if area_a == '4' and type == '2':
                num_h = '蓄电池逆变器'
                devs = DevControl.objects.filter(dev_type=10).values_list('num')
                for dev in devs:
                    if dev[0] not in nums:
                        num.append(dev[0])
            # 如果是蓄电池设备(蓄电池)
            if area_a == '4' and type == '3':
                num_h = '蓄电池'
                devs = DevControl.objects.filter(dev_type=11).values_list('num')
                for dev in devs:
                    if dev[0] not in nums:
                        num.append(dev[0])
            # 如果是飞轮区组级(飞轮逆变器)
            if area_a == '5' and type == '2':
                num_h = '飞轮逆变器'
                devs = DevControl.objects.filter(dev_type=12).values_list('num')
                for dev in devs:
                    if dev[0] not in nums:
                        num.append(dev[0])

            # 如果是飞轮设备(飞轮)
            if area_a == '5' and type == '3':
                num_h = '飞轮'
                devs = DevControl.objects.filter(dev_type=13).values_list('num')
                for dev in devs:
                    if dev[0] not in nums:
                        num.append(dev[0])

            # 如果负载
            if area_a == '6' and type == '2':
                num_h = '负载'
                devs = DevControl.objects.filter(dev_type=30).values_list('num')
                for dev in devs:
                    if dev[0] not in nums:
                        num.append(dev[0])

            # 如果是控制区组级
            if area_a == '7' and type == '2':
                num_h = '控制区'
                devs = DevControl.objects.filter(dev_type__in=[20,21,22]).values_list('num')
                for dev in devs:
                    if dev[0] not in nums:
                        num.append(dev[0])

            # 如果是环境区组
            if area_a == '8' and type == '2':
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


# 控制区开关请求控制处理
class DeviceAskView(View):
    def post(self, request):
        ask_dev = request.POST.get('ask_dev','')
        print(ask_dev)
        num = request.POST.get('num', '')
        switch_status = request.POST.get('switch_status', '')
        active_power = request.POST.get('active_power', 0)
        reactive_power = request.POST.get('reactive_power', 0)
        powerfactor = request.POST.get('powerfactor', 0)

        # 获取对应开关并设置状态
        dev = DevControl.objects.get(num=num)
        dev.switch_status = switch_status
        dev.active_power = float(active_power)
        dev.reactive_power = float(reactive_power)
        dev.powerfactor = float(powerfactor)
        dev.save()

        return HttpResponseRedirect('/device_manage/?ask_dev={0}'.format(ask_dev))


# 电池属性
class BattaryPropertyView(View):
    def post(self, request):
        num = request.POST.get("num","")
        rated_capacity = request.POST.get("rated_capacity","")

        battaryproperty = BattatyProperty.objects.get(battary_num=num)
        battaryproperty.rated_capacity = rated_capacity
        battaryproperty.save()
        return HttpResponseRedirect('/dev_info/?num={0}&&type={1}'.format(num,12))

# PSO ；粒子群优化算法
class PsoView(View):
    def get(self, request):
        nav = 4

        microgrid_max = request.GET.get("microgrid_max",300)
        microgrid_min = request.GET.get("microgrid_min",-300)
        battary_output = request.GET.get("battary_output",400)
        battary_input = request.GET.get("battary_input",400)

        # 粒子群优化算法
        # 预测24小时光伏、负载，电价
        P_pv = np.array([0,0,0,0,0,0,10,20,40,150,250,200,180,150,150,100,40,20,0,0,0,0,0,0])
        P_load = np.array([10,12,10,12,14,23,30,60,80,100,120,100,100,140,180,120,60,100,120,120,120,120,80,40])
        G_price = np.array([0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.4,0.4,0.4])

        # 临时变量
        # 电池工作状态
        B = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0])
        P_bat = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0])
        fangdian = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0])
        chongdian = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0])

        # 结果集
        # 电网向微电网输入输出量
        pg1 = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0])
        # 电池存储输入输出量
        pg2 = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0])

        # 初始化
        # 允许调节负载范围
        P_tiao = P_load - P_pv
        # 电网输入微网最大功率
        GridMaxImportPower = microgrid_max
        # 微网输入电网最小功率
        GridMinImportPower = microgrid_min
        # 储能最大放电功率
        StorageMaxDischargingPower = battary_output
        # 储能最大充电功率
        StorageMaxChargingPower = battary_input
        # 最大迭代次数300,5000
        Max_Dt = 500
        D = 25  #搜索空间维数（未知数个数）24+1
        N = 600  #粒子个数600,100
        w_max = 0.9  #w权重上限
        w_min = 0.4  #w权重下限
        v_max = 2.0  #w速度变量上限
        s = 0  #记录最优值的迭代次数
        v = np.ones((N, D))
        x = np.ones((N, D))
        y = np.ones((N, D))
        p = np.ones(N)

        def fitness(x):
            C_GRID = 0  # 取电大电网成本
            for j in range(0, 24):
                P_bat[j] = P_load[j] - P_pv[j] - x[j]  # 电池24小时工作情况,P_bat>0(放电)，P_bat<0(充电)
            cost = 0  # 污染治理成本
            fa = 0  # 电池深浅冲放引起的寿命成本增加费用
            chushi = x[24] * 75 / 365  # 铅酸蓄电池日维护费用
            shouyi = 0  # 大电网卖电收获
            for j in range(0, 24):
                if x[j] > 0:  # 充电
                    C_GRID = C_GRID + G_price[j] * x[j]
                if x[j] < 0:  # 放电
                    shouyi = shouyi + 0.6 * x[j]
            for j in range(0, 24):
                if x[j] > 0:
                    cost = cost + (1.2 * (0.002875 + 0.00125) + 0.0024 * 1.25 + 0.002 * 0.875 + 0.00078 * 0.145) * x[j]
                # print(x)
            for j in range(0, 24):
                d = abs(P_bat[j] / x[24])
                y = d ** 1.7
                fa = fa + chushi * y
            result = C_GRID + fa + chushi + shouyi + cost
            return result

        for i in range(0, N):
            for j in range(0, D - 1):
                v[i, j] = random.random()  # 用于生成一个随机浮点数n,0 =< n < 1 #初始化粒子速度变量
                x[i, j] = GridMinImportPower + random.random() * (GridMaxImportPower - GridMinImportPower)  # 初始化粒子位置
                # x[i,D-1]=random.random()*1400 #限定初始化电池容量在0-1400
            x[i, D - 1] = 500  # 限定初始化电池容量在0-1400
            v[i, D - 1] = random.random()  # 限定初始化电池容量速度变量
            for j in range(0, D - 1):
                B[j] = P_load[j] - P_pv[j] - x[i, j]  # 通过功率平衡条件计算出电池工作状态
                # print(v)
            # 限定电池工作在上下限内-4
            for j in range(0, D - 1):
                if B[j] < -StorageMaxDischargingPower:
                    x[i, j] = x[i, j] + B[j] + StorageMaxDischargingPower
                if B[j] > StorageMaxChargingPower:
                    x[i, j] = x[i, j] + B[j] - StorageMaxChargingPower
            for j in range(0, D - 1):
                P_bat[j] = P_load[j] - P_pv[j] - x[i, j]  # 重新计算经过一次约束后的电池工作状态
            soc = 0  # 设电池初始容量为0，即本身不带前一天的电
            q = 0
            # 限定t=1时刻只允许充电，不允许放电
            if P_bat[0] > 0:
                x[i, 0] = x[i, 0] + P_bat[0]
                P_bat[0] = 0
            for j in range(0, 23):
                soc = soc - P_bat[j]
                # 限定不允许充电达到容量上限
                if soc > x[i, D - 1]:
                    q = soc - x[i, D - 1]
                    soc = x[i, D - 1]
                    P_bat[j] = P_bat[j] + q
                    x[i, j] = x[i, j] - q
                    # 限定不允许在容量不足时放电超过目前所拥有电量
                if P_bat[j + 1] > soc:
                    h = P_bat[j + 1] - soc
                    P_bat[j + 1] = soc
                    x[i, j + 1] = x[i, j + 1] + h
        # ***************计算各个粒子的适应度，并初始化Pi和Pg****************
        for i in range(0, N):
            p[i] = fitness(x[i, :])
            y[i, :] = x[i, :]  # 每个粒子的个体寻优值
        Pbest = p[0]
        # Pg为全局最优
        pg = x[1, :]
        for i in range(1, N):
            if fitness(x[i, :]) < fitness(pg):
                Pbest = fitness(x[i, :])
                pg = x[i, :]  # 全局最优更新
        # ****************************进入主循环*****************************************
        for t in range(0, Max_Dt):
            for i in range(0, N):
                w = w_max - (w_max - w_min) * t / Max_Dt  # 惯性权重更新 0.7
                c1 = (0.5 - 2.5) * t / Max_Dt + 2.5  # 认知 2.05
                c2 = (2.5 - 0.5) * t / Max_Dt + 0.5  # 社会认识 2.05
                v[i, :] = w * v[i, :] + c1 * random.random() * (y[i, :] - x[i, :]) + c2 * random.random() * (
                            pg - x[i, :])  # 更新后的速度变量
                for j in range(0, 25):  # 防止寻优速度超过速度上限，如果超过，则限定在速度上限峰值
                    if v[i, j] > v_max:
                        v[i, j] = v_max
                    if v[i, j] < -v_max:
                        v[i, j] = -v_max
                x[i, :] = x[i, :] + v[i, :]  # 更新后的粒子位置
                # ******对粒子边界处理*****************************
                for n in range(0, 24):
                    if x[i, n] < GridMinImportPower:  # 防止大电网充放电超过上下限
                        x[i, n] = GridMinImportPower
                        v[i, n] = -v[i, n]
                    if x[i, n] > GridMaxImportPower:
                        x[i, n] = GridMaxImportPower
                        v[i, n] = -v[i, n]
                if x[i, 24] > 2000:  # 限定容量的上限为2000KWH
                    x[i, 24] = 2000
                    v[i, 24] = -v[i, 24]
                if x[i, 24] < 0:  # 限定容量的下限为0KWH
                    x[i, 24] = 0
                    v[i, 24] = -v[i, 24]
                    # 同初始化一样，进行相关的条件约束
                for j in range(0, D - 1):
                    P_bat[j] = P_load[j] - P_pv[j] - x[i, j]
                soc = 0
                if P_bat[0] > 0:
                    x[i, 0] = x[i, 0] + P_bat[0]
                    P_bat[0] = 0
                for j in range(0, D - 2):
                    soc = soc - P_bat[j]
                    if soc > x[i, D - 1]:
                        q = soc - x[i, D - 1]
                        soc = x[i, D - 1]
                        P_bat[j] = P_bat[j] + q
                        x[i, j] = x[i, j] - q
                    if P_bat[j + 1] > soc:
                        h = P_bat[j + 1] - soc
                        P_bat[j + 1] = soc
                        x[i, j + 1] = x[i, j + 1] + h
                    # *********对粒子进行评价，寻找最优值******************
                PFp = fitness(x[i, :])
                if PFp < p[i]:
                    p[i] = PFp
                    y[i, :] = x[i, :]
                if p[i] < Pbest:
                    Pbest = p[i]
                    pg = y[i, :]
                    s = t  # 记录目前最优值出现在第几次迭代中
        C_GRID = 0
        for i in range(0, D - 1):  # 向大电网取电的费用
            if pg[i] > 0:
                C_GRID = C_GRID + G_price[i] * pg[i]
            if pg[i] < 0:
                C_GRID = C_GRID + 0.6 * pg[i]
        chengben = fitness(pg)  # 实际一日综合各种费用的成本
        for i in range(0, D - 1):
            pg1[i] = pg[i]
            pg2[i] = P_load[i] - P_pv[i] - pg[i]
        for i in range(0, D - 1):
            if pg2[i] > 0:
                fangdian[i] = pg2[i] / 220
            else:
                fangdian[i] = 0
        for i in range(0, D - 1):
            if pg2[i] < 0:
                chongdian[i] = 220 * 220 / -pg2[i]
            else:
                chongdian[i] = float("inf")
        # 电量差和，越小越好
        SUM = 0
        for i in range(0, D - 1):
            SUM = SUM - (P_load[i] - P_pv[i] - pg[i])
        microgrid = pg1.tolist()
        battray = pg2.tolist()
        return render(request, 'pso.html', {
            'nav':nav,
            'microgrid_max': microgrid_max,
            'microgrid_min': microgrid_min,
            'battary_output': battary_output,
            'battary_input': battary_input,

            'microgrid':microgrid,
            'battray':battray,

        })

