# Microgrid（微电网能量管理系统）
## 一、开发环境
Python3.6+Django1.11+mysql5.6(web)
Java1.8 + mysql5.6 (iec104)
## 二、项目简介
#### 微电网管理系统总框架图
![](https://github.com/msun1996/Microgrid/blob/master/projectInstruction/picture/%E5%BE%AE%E7%94%B5%E7%BD%91%E7%AE%A1%E7%90%86%E7%B3%BB%E7%BB%9F%E6%80%BB%E6%A1%86%E6%9E%B6%E5%9B%BE.png)
本项目为微电网能量系统管理系统，实现通过Web界面对微电网系统进行实时管控。 
* [**Microgird工程**](https://github.com/msun1996/Microgrid)完成Web管控部分功能，主要包括设备逻辑管理与视图化展示、设备数据实时显示功能、设备远程命令控制与参数下发功能； 
* [**IEC104_microgrid工程**](https://github.com/msun1996/IEC104_microgrid)完成104主站部分功能，主要包括IEC104主站通讯功能（遥信、遥测、遥控、遥调）与数据库数据存储与提取功能。 
## 三 Web
