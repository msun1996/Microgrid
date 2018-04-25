# -*- coding: utf8 -*-

import xadmin

from microgrids.models import DevControl,EnvAddressC,PVAnalogQuantityData,PVDigitalQuantityData,EnvironmentData,WebMicrogrid

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


class PVAnalogQuantityDataAdmin(object):
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


xadmin.site.register(DevControl, DevControlAdmin)
xadmin.site.register(EnvAddressC, EnvAddressCAdmin)
xadmin.site.register(PVAnalogQuantityData, PVAnalogQuantityDataAdmin)
xadmin.site.register(PVDigitalQuantityData, PVDigitalQuantityDataAdmin)
xadmin.site.register(EnvironmentData, EnvAdressDataAdmin)
xadmin.site.register(WebMicrogrid, WebMicrogridAdmin)

# # 本地主要管理数据
# from microgrids.models import HighVoltageLoadSwitchC,IsolationSwitchC,BreakerSwitchC,PVC,PVAnalogQuantityData,PVDigitalQuantityData,EnvironmentData
# # Web管理数据库
# from microgrids.models import Area,PV,HighVoltageLoadSwitch,BreakerSwitch,IsolationSwitch,EnvAdress
#
#
# # 本地
# class HighVoltageLoadSwitchCAdmin(object):
#     list_display = ['switch_num']
#     search_fields = ['switch_num']
#     list_filter = ['switch_num']
#
#
# class IsolationSwitchCAdmin(object):
#     list_display = ['switch_num']
#     search_fields = ['switch_num']
#     list_filter = ['switch_num']
#
#
# class BreakerSwitchCAdmin(object):
#     list_display = ['switch_num']
#     search_fields = ['switch_num']
#     list_filter = ['switch_num']
#
#
# class PVCAdmin(object):
#     list_display = ['pv_num']
#     search_fields = ['pv_num']
#     list_filter = ['pv_num']
#
#
# class PVDigitalQuantityDataAdmin(object):
#     list_display = ['pv_num']
#     search_fields = ['pv_num']
#     list_filter = ['pv_num']
#
#
# class PVAnalogQuantityDataAdmin(object):
#     list_display = ['pv_num']
#     search_fields = ['pv_num']
#     list_filter = ['pv_num']
#
#
# class EnvAdressDataAdmin(object):
#     list_display = ['env_num']
#     search_fields = ['env_num']
#     list_filter = ['env_num']
#
#
# # Web 管理库
# class AreaAdmin(object):
#     list_display = ['num']
#     search_fields = ['num']
#     list_filter = ['num']
#
#
# class PVAdmin(object):
#     list_display = ['pv_num']
#     search_fields = ['pv_num']
#     list_filter = ['pv_num']
#
#
# class EnvAdressAdmin(object):
#     list_display = ['env_num']
#     search_fields = ['env_num']
#     list_filter = ['env_num']
#
#
# class HighVoltageLoadSwitchAdmin(object):
#     list_display = ['switch_num']
#     search_fields = ['switch_num']
#     list_filter = ['switch_num']
#
#
# class BreakerSwitchAdmin(object):
#     list_display = ['switch_num']
#     search_fields = ['switch_num']
#     list_filter = ['switch_num']
#
#
# class IsolationSwitchAdmin(object):
#     list_display = ['switch_num']
#     search_fields = ['switch_num']
#     list_filter = ['switch_num']
#
#
# # xadmin注册
# xadmin.site.register(HighVoltageLoadSwitchC, HighVoltageLoadSwitchCAdmin)
# xadmin.site.register(IsolationSwitchC, IsolationSwitchCAdmin)
# xadmin.site.register(BreakerSwitchC, BreakerSwitchCAdmin)
# xadmin.site.register(PVC, PVCAdmin)
# xadmin.site.register(PVAnalogQuantityData, PVAnalogQuantityDataAdmin)
# xadmin.site.register(PVDigitalQuantityData, PVDigitalQuantityDataAdmin)
# xadmin.site.register(EnvironmentData, EnvAdressDataAdmin)
#
# xadmin.site.register(Area, AreaAdmin)
# xadmin.site.register(PV, PVAdmin)
# xadmin.site.register(EnvAdress, EnvAdressAdmin)
# xadmin.site.register(HighVoltageLoadSwitch, HighVoltageLoadSwitchAdmin)
# xadmin.site.register(BreakerSwitch, BreakerSwitchAdmin)
# xadmin.site.register(IsolationSwitch, IsolationSwitchAdmin)
