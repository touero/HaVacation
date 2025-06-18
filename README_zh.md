# HaVacation

<p align="center">
    <a href="https://github.com/touero/HaVacation/blob/main/README.md">English</a>
    <a href="https://github.com/touero/HaVacation/blob/main/README_zh.md">中文</a>
</p>

<p align="center">
    <img src=preview/logo.png height="200" width="200" alt="">
</p>

一个关于中国节假日/工作日的Home-Assistant集成, 同时它支持自定义工作日和假期.

## 安装

### 通过Hacs安装

#### 如果你已经安装了[hacs](https://github.com/hacs/integration), 请点击:  
[![ByHacs](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=touero&repository=HaVacation&category=integration)  
#### 然后重启Home-assistant, 你就能在集成菜单找到它或者点击:  
[![add_integration](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=ha_vacation)

### 手动安装
导航到[Releases](https://github.com/touero/HaVacation/releases/)下载ha_vacation.tar.gz压缩包, 把它放到`HomeAssistant/custom_components`下执行命令解压:

```shell
tar -zxvf ha_vacation.tar.gz
```
然后重启Home-Assistant

之后在集成搜索配置它

> [!IMPORTANT] 
> 自定义节假日需要重新加载插件

## 细节

配置后你会得到3个实体

![preview](https://github.com/touero/HaVacation/blob/main/preview/sensor.png)

它们有着一些属性

![preview](https://github.com/touero/HaVacation/blob/main/preview/sensor_details.png)

你可以自定义节假日在实体的配置中

![preview](https://github.com/touero/HaVacation/blob/main/preview/config.png)

> [!TIP]
> 下面一些属性的类型和描述说明

| attribute | type | description |
| --------- | ---- | ----------- |
| Updated at | str | 实体更新日期的时间, 每天00:00更新 |
| Is workday | str |  这天是否为工作日 |
| Is vacation | str | 这天是否为假期|
| Is customize date | str | 这天是否是自定义的节假日 |

The value of `Is workday`, `Is vacation` and `Is customize date` there will be only two changes: `true` and `false`.  
属性 `Is workday`, `Is vacation` and `Is customize date` 它们有两个值: str类型的`true` and `false`.  

> [!IMPORTANT] 
> 自定义节假日需要重新加载插件

开始你的自动化吧!

## 基于
[chinese-calendar](https://github.com/LKI/chinese-calendar)

## 协议
[MIT](https://github.com/touero/HaVacation/blob/main/LICENSE) [@touero](https://github.com/touero)

