# -*- coding:utf8 -*-
from datetime import datetime

from django.db import models

# Create your models here.


# # 本地上传数据库数据（Web改变其中数据库时，认为执行命令） ###############
# 本地控制信息
# 设备状态控制
class DevControl(models.Model):
    # 设备类别
    DEV_TYPE = (
        (1, '光伏组逆变器'),
        (2, '光伏板'),
        (3, '风力逆变器'),
        (4, '风机'),
        (5, '燃料电池逆变器'),
        (6, '燃料电池'),


        (11, '蓄电池组逆变器'),
        (12, '蓄电池'),
        (13, '飞轮逆变器'),
        (14, '飞轮'),

        (20, '高压负荷开关'),
        (21, '隔离开关'),
        (22, '断路器'),

        (30, '负载')
    )
    STATUS = (
        (0, '断开'),
        (1, '闭合'),
    )
    num = models.CharField(max_length=20, unique=True, verbose_name='编号')
    dev_type = models.IntegerField(choices=DEV_TYPE, verbose_name=u'设备类型')
    # 光伏、高压负荷开关、断路器、隔离开关
    switch_status = models.IntegerField(choices=(STATUS), default=0, blank=True, null=True, verbose_name='开关状态控制')
    # 逆变器设置使用
    active_power = models.FloatField(blank=True, null=True, verbose_name='有功功率设置')
    reactive_power = models.FloatField(blank=True, null=True, verbose_name='无功功率设置')
    powerfactor = models.FloatField(blank=True, null=True, verbose_name='功率因素设置')

    class Meta:
        verbose_name = '设备控制信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.num


# 环境地址
class EnvAddressC(models.Model):
    env_num = models.CharField(max_length=20, unique=True, verbose_name='环境地址编号')

    class Meta:
        verbose_name = u'环境地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.env_num


# 数据类存储不进行外键关联，为在设备被移除时可以继续保存(保存时注意保持编号一致)因数据实时性要求不同，分类保存
# 光伏逆变器模拟量数据1（实时性高数据，数据量大，需定时清除）
class PVAnalogQuantityData1(models.Model):
    timestamp = models.DateTimeField(default=datetime.now, verbose_name='时间戳')
    pv_num = models.CharField(max_length=20, verbose_name='光伏逆变器编号')
    matrix_cur = models.FloatField(blank=True, null=True, verbose_name='阵列电流')
    matrix_volt = models.FloatField(blank=True, null=True, verbose_name='阵列电压')
    matrix_power_in = models.FloatField(blank=True, null=True, verbose_name='阵列输入功率')
    grid_volt_ab = models.FloatField(blank=True, null=True, verbose_name='电网AB线电压')
    grid_volt_bc = models.FloatField(blank=True, null=True, verbose_name='电网BC线电压')
    grid_volt_ca = models.FloatField(blank=True, null=True, verbose_name='电网CA线电压')
    on_grid_cur_a = models.FloatField(blank=True, null=True, verbose_name='A相并网电流')
    on_grid_cur_b = models.FloatField(blank=True, null=True, verbose_name='B相并网电流')
    on_grid_cur_c = models.FloatField(blank=True, null=True, verbose_name='C相并网电流')
    power_factor_a = models.FloatField(blank=True, null=True, verbose_name='A相功率因素')
    power_factor_b = models.FloatField(blank=True, null=True, verbose_name='B相功率因素')
    power_factor_c = models.FloatField(blank=True, null=True, verbose_name='C相功率因素')
    grid_freq = models.FloatField(blank=True, null=True, verbose_name='电网频率')
    class Meta:
        verbose_name = u'光伏逆变器模拟量数据1'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.timestamp


# 光伏逆变器模拟量数据2（常年数据，）
class PVAnalogQuantityData2(models.Model):
    timestamp = models.DateTimeField(default=datetime.now, verbose_name='时间戳')
    pv_num = models.CharField(max_length=20, verbose_name='光伏逆变器编号')
    on_grid_p = models.FloatField(blank=True, null=True, verbose_name='并网有功功率')
    on_grid_q = models.FloatField(blank=True, null=True, verbose_name='并网无功功率')
    on_grid_s = models.FloatField(blank=True, null=True, verbose_name='并网视在功率')
    inv_cabin_temp = models.FloatField(blank=True, null=True, verbose_name='机柜温度')
    day_gen_power = models.FloatField(blank=True, null=True, verbose_name='日累计发电量')
    day_runtime = models.FloatField(blank=True, null=True, verbose_name='日运行时间')
    total_gen_power = models.FloatField(blank=True, null=True, verbose_name='总累计发电量')
    total_runtime = models.FloatField(blank=True, null=True, verbose_name='总运行时间')
    co2_reduce = models.FloatField(blank=True, null=True, verbose_name='CO2减排量')

    class Meta:
        verbose_name = u'光伏逆变器模拟量数据2'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.timestamp


# 光伏逆变器数字量数据（异常状态）
class PVDigitalQuantityData(models.Model):
    IS_STATUS =(
        (0, '是'),
        (1, '否'),
    )
    BUTTON_STATUS = (
        (0, '启动'),
        (1, '未启动'),
    )
    TESTING_STATUS = (
        (0, '正常'),
        (1, '异常'),
    )
    pv_num = models.CharField(max_length=20, unique=True, verbose_name='光伏逆变器编号')
    status_down = models.IntegerField(choices=(IS_STATUS), blank=True, null=True, verbose_name='设备状态_停机')
    status_standby = models.IntegerField(choices=(IS_STATUS), blank=True, null=True, verbose_name='设备状态_待机')
    status_selftest = models.IntegerField(choices=(IS_STATUS), blank=True, null=True, verbose_name='设备状态_自检')
    status_ongrid = models.IntegerField(choices=(IS_STATUS), blank=True, null=True, verbose_name='设备状态_并网')
    locking_self = models.IntegerField(choices=(IS_STATUS), blank=True, null=True, verbose_name='闭锁未自锁')
    emergency_stop = models.IntegerField(choices=(BUTTON_STATUS), blank=True, null=True, verbose_name='急停')
    remote_local = models.IntegerField(choices=(IS_STATUS), blank=True, null=True, verbose_name='远程本地')
    PV_reverse_connection = models.IntegerField(choices=(IS_STATUS), blank=True, null=True, verbose_name='PV反接')
    PV_insulation_resistance = models.IntegerField(choices=(TESTING_STATUS), blank=True, null=True, verbose_name='PV对地绝缘阻抗')
    DC_overvoltage = models.IntegerField(choices=(TESTING_STATUS), blank=True, null=True, verbose_name='直流过压')
    power_voltage = models.IntegerField(choices=(TESTING_STATUS), blank=True, null=True, verbose_name='电网电压')
    grid_frequency = models.IntegerField(choices=(TESTING_STATUS), blank=True, null=True, verbose_name='电网频率')
    grid_reverse_order = models.IntegerField(choices=(IS_STATUS), blank=True, null=True, verbose_name='电网反序')
    inverter_overload = models.IntegerField(choices=(TESTING_STATUS), blank=True, null=True, verbose_name='逆变器过载')
    inverter_overheating = models.IntegerField(choices=(TESTING_STATUS), blank=True, null=True, verbose_name='逆变器过热')
    inverter_short_circuit = models.IntegerField(choices=(TESTING_STATUS), blank=True, null=True, verbose_name='逆变器短路')
    smoke_alarm = models.IntegerField(choices=(TESTING_STATUS), blank=True, null=True, verbose_name='烟感报警')
    ambient_temperature_overheating = models.IntegerField(choices=(TESTING_STATUS), blank=True, null=True, verbose_name='环境温度过热')
    reactive_power_compensation = models.IntegerField(choices=(IS_STATUS), blank=True, null=True, verbose_name='夜间无功补偿')
    DC_lightning_protection = models.IntegerField(choices=(TESTING_STATUS), blank=True, null=True, verbose_name='直流防雷故障')
    AC_lightning_protection = models.IntegerField(choices=(TESTING_STATUS), blank=True, null=True, verbose_name='交流防雷故障')
    island_protection = models.IntegerField(choices=(BUTTON_STATUS), blank=True, null=True, verbose_name='孤岛保护')

    class Meta:
        verbose_name = u'光伏逆变器数字量数据'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.pv_num


# 地址环境各项参数数据
class EnvironmentData(models.Model):
    timestamp = models.DateTimeField(default=datetime.now, verbose_name=u'时间戳')
    env_num = models.CharField(max_length=20, verbose_name='环境地址编号')
    wind_speed = models.FloatField(blank=True, null=True, verbose_name=u'风速(m/s)')
    wind_direct = models.FloatField(blank=True, null=True, verbose_name=u'风向(°)')
    env_temperature = models.FloatField(blank=True, null=True, verbose_name=u'环境温度(°C)')
    env_temperature2 = models.FloatField(blank=True, null=True, verbose_name=u'环境温度2(°C)')
    env_humidity = models.FloatField(blank=True, null=True, verbose_name=u'环境湿度')
    air_pressure = models.FloatField(blank=True, null=True, verbose_name=u'气压(hPa)')

    period_rainfall = models.FloatField(blank=True, null=True, verbose_name=u'雨量时间间隔累计量(mm)')
    period_sun = models.FloatField(blank=True, null=True, verbose_name=u'日照时间间隔累计量(mm)')

    instant_total_radiation = models.FloatField(blank=True, null=True, verbose_name=u'总辐射瞬时值')
    instant_scat_radiation = models.FloatField(blank=True, null=True, verbose_name=u'散辐射瞬时值')
    instant_direct_radiation = models.FloatField(blank=True, null=True, verbose_name=u'直辐射瞬时值')
    instant_net_radiation = models.FloatField(blank=True, null=True, verbose_name=u'净辐射瞬时值')
    instant_photosynthetic_radiation = models.FloatField(blank=True, null=True, verbose_name=u'光合辐射瞬时值')
    instant_ultraviolet_radiation = models.FloatField(blank=True, null=True, verbose_name=u'紫外辐射瞬时值')

    period_total_radiation = models.FloatField(blank=True, null=True, verbose_name=u'总辐射时间间隔累计值')
    period_scat_radiation = models.FloatField(blank=True, null=True, verbose_name=u'散辐射时间间隔累计值')
    period_direct_radiation = models.FloatField(blank=True, null=True, verbose_name=u'直辐射时间间隔累计量')
    period_net_radiation = models.FloatField(blank=True, null=True, verbose_name=u'净辐射时间间隔累计值')
    period_photosynthetic_radiation = models.FloatField(blank=True, null=True, verbose_name=u'光合辐射时间间隔累计量')
    period_ultraviolet_radiation = models.FloatField(blank=True, null=True, verbose_name=u'紫外辐射时间间隔累计值')

    class Meta:
        verbose_name = u'环境数据'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.timestamp


# 微电网设备web管理（区域/设备/元件管理）(重构)
class WebMicrogrid(models.Model):
    # 分级
    TYPE = (
        (1, '子区域'),
        (2, '设备组'),  # 逆变器
        (3, '具体发电设备')  # 光伏板、风力机、蓄电池
    )
    # 区域类别
    AREA_TYPE = (
        (0, '间隔区'),   # 里面主要为PCC
        (1, '光伏区'),
        (2, '风力区'),
        (3, '燃机区'),
        (4, '电池储能区'),
        (5, '飞轮储能区'),
        (6, '负载区'),
        (7, '控制区'), # 控制区域包含各类和控制相关设备和开关
        (8, '环境')
    )
    # 设备名称
    # 保存对应本地设备地址
    num = models.CharField(max_length=20, unique=True, verbose_name=u'编号')
    name = models.CharField(max_length=50, verbose_name=u'区域/设备/元件名')
    remark = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'备注')
    type = models.IntegerField(choices=TYPE, verbose_name=u'编号类型')
    # 创建区域时所属区域类别
    area_type = models.IntegerField(choices=AREA_TYPE, verbose_name=u'区域类别')

    # 创建设备所属指向上级num
    parent_area = models.ForeignKey('self',to_field='num',blank=True, null=True, related_name='sub',verbose_name=u'设备上级')

    # 控制区域归属区域或设备(控制区中子区域会关联到整个微网需要控制的区域或设备)
    control_belong = models.ForeignKey('self', to_field='num', null=True, blank=True, related_name='sub2', verbose_name=u'控制区域所属')

    class Meta:
        verbose_name = u'微电网设备web管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.num


# class PsoInfo(models.Model):
#     GridMaxImportPower =
#     GridMinImportPower =


# 图片存储
class Img(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'名称')
    name_h = models.CharField(max_length=30, verbose_name=u'汉语名称')  # 便于添加编辑
    img = models.ImageField(upload_to='img', verbose_name=u'图片')

    class Meta:
        verbose_name = u'图片管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

