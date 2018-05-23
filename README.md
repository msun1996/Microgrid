# Microgrid（微电网能量管理系统）
## 一、开发环境
- **web管理系统** HTML+CSS+JS+Bootstrap（*前端*）+ Python3.6+Django1.11（*后端*）+ mysql5.6(*数据库*)
- **iec104主站客户端** Java1.8 + mysql5.6
## 二、项目简介
#### 微电网管理系统总框架图
![](https://github.com/msun1996/Microgrid/blob/master/projectInstruction/picture/%E5%BE%AE%E7%94%B5%E7%BD%91%E7%AE%A1%E7%90%86%E7%B3%BB%E7%BB%9F%E6%80%BB%E6%A1%86%E6%9E%B6%E5%9B%BE.png)
本项目为微电网能量系统管理系统，实现通过Web界面对微电网系统进行实时管控。 
* [**Microgird工程**](https://github.com/msun1996/Microgrid)完成Web管控部分功能，主要包括设备逻辑管理与视图化展示、设备数据实时显示功能、设备远程命令控制与参数下发功能； 
* [**IEC104_microgrid工程**](https://github.com/msun1996/IEC104_microgrid)完成104主站部分功能，主要包括IEC104主站通讯功能（遥信、遥测、遥控、遥调）与数据库数据存储与提取功能。 
#### 数据库逻辑设计图
![](https://github.com/msun1996/Microgrid/blob/master/projectInstruction/picture/%E6%95%B0%E6%8D%AE%E5%BA%93%E9%80%BB%E8%BE%91%E8%AE%BE%E8%AE%A1.png)
#### Web设备管理控制逻辑框架
![](https://github.com/msun1996/Microgrid/blob/master/projectInstruction/picture/Web%E8%AE%BE%E5%A4%87%E7%AE%A1%E7%90%86%E9%80%BB%E8%BE%91%E6%A1%86%E6%9E%B6.png)
- 设备区：
> 设备区为四层树结构。
> 设备区下包括光伏区、蓄电池区、风电区等等大区域。（逻辑分区）
>> 光伏区(大区以光伏为例)下包括光伏子区，光伏子区控制部分。（逻辑分区）
>> 光伏子区下包括逆变器设备相关控制部分。（物理存在，逻辑管理）
>> 逆变器下包括光伏阵列设备及其相关控制部分。（物理存在，逻辑管理）
- 间隔区：
> 间隔区主要是对PCC等（区域并网）的控制部分区域保存。（物理存在，逻辑管理）
- 控制区：
> 控制区贯穿整个设备区和间隔区，主要将两个区域的控制部分映射到此区域，再将开关等具体控制单元添加到映射区，方便对所有控制部分直接管理。
#### Web设备管理界面
![](https://github.com/msun1996/Microgrid/blob/master/projectInstruction/picture/Web%E8%AE%BE%E5%A4%87%E7%AE%A1%E7%90%86%E7%95%8C%E9%9D%A2.png)
- **电站管理左侧栏:** 
> 可以对子区，逆变器设备、光伏设备等等进行添加、删除操作。（添加设备，开关元件时，该设备必须真实存在，设备号已存在到数据库，才可搜索到，进行添加）
- **管理模型:** 
> 会在管理栏对设备进行修改后，自动生成对应模型，方便视图化管理。点击具体设备或控制单元，会自动跳转到对应设备或单元的控制管理部分界面。
- **控制管理：** 
> 此区域会在管理模型点击对应设备后自动展示其对应控制相关的部分，可在此修改设备状态或参数（会修改数据库，下发命令给具体设备）。也可点击设备信息具体查看设备相关信息。
