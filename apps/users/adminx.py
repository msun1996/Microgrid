# -*- coding: utf8 -*-

import xadmin

from xadmin import views


# 允许用新主题样式
class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


# 管理系统页头页脚设置
class GlobalSettings(object):
    site_title = '微电网能量管理系统后台'
    site_footer = '微电网能量管理系统'
    menu_style = 'accordion'


# xadmin注册
xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)