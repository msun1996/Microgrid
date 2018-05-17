# -*- coding: utf8 -*-

import xadmin

from microgrids.models import DevControl,EnvAddressC,PVAnalogQuantityData1,PVAnalogQuantityData2,PVDigitalQuantityData,EnvironmentData,WebMicrogrid,Img


# 本地主要管理上传数据
class DevControlAdmin(object):
    list_display = ['num']
    search_fields = ['num']
    list_filter = ['num']


class EnvAddressCAdmin(object):
    list_display = ['env_num']
    search_fields = ['env_num']
    list_filter = ['env_num']


class PVDigitalQuantityDataAdmin(object):
    list_display = ['pv_num']
    search_fields = ['pv_num']
    list_filter = ['pv_num']


class PVAnalogQuantityData1Admin(object):
    list_display = ['pv_num']
    search_fields = ['pv_num']
    list_filter = ['pv_num']


class PVAnalogQuantityData2Admin(object):
    list_display = ['pv_num']
    search_fields = ['pv_num']
    list_filter = ['pv_num']


class EnvAdressDataAdmin(object):
    list_display = ['env_num']
    search_fields = ['env_num']
    list_filter = ['env_num']


# Web 管理库
class WebMicrogridAdmin(object):
    list_display = ['num']
    search_fields = ['num']
    list_filter = ['num']


class ImgAdmin(object):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']


xadmin.site.register(DevControl, DevControlAdmin)
xadmin.site.register(EnvAddressC, EnvAddressCAdmin)
xadmin.site.register(PVAnalogQuantityData1, PVAnalogQuantityData1Admin)
xadmin.site.register(PVAnalogQuantityData2, PVAnalogQuantityData2Admin)
xadmin.site.register(PVDigitalQuantityData, PVDigitalQuantityDataAdmin)
xadmin.site.register(EnvironmentData, EnvAdressDataAdmin)
xadmin.site.register(WebMicrogrid, WebMicrogridAdmin)
xadmin.site.register(Img, ImgAdmin)
