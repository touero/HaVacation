# HaVacation

<p align="center">
    <img src=preview/logo.png height="200" width="200" alt="">
</p>

A Chinese workday/vacation integration for Home-Assistant, support customize date of workday and vacation.

## Installation

### Hacs Install

#### If you have installed [hacs](https://github.com/hacs/integration), please click:  
[![ByHacs](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=touero&repository=HaVacation&category=integration)  
#### After restart Home-Assistant, you can find it in the integration menu or click:  
[![add_integration](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=ha_vacation)

### Manual Install
Go to [Releases](https://github.com/touero/HaVacation/releases/) download the ha_vacation.tar.gz and move it to `HomeAssistant/custom_components` and execute:

```shell
tar -zxvf ha_vacation.tar.gz
```
And then restart your home-assistant.

In add integration search HaVacation configure it.

> [!IMPORTANT] 
> Reloading is required after configuring a custom date

## Details

After you will get 1-3 sensor:

![preview](https://github.com/touero/HaVacation/blob/main/preview/sensor.png)

And then have attribute:

![preview](https://github.com/touero/HaVacation/blob/main/preview/sensor_details.png)

You can customize the date of workday and vacation in the integration configuration.

![preview](https://github.com/touero/HaVacation/blob/main/preview/config.png)

> [!TIP]
> The following are the types and descriptions of each attribute.  

| attribute | type | description |
| --------- | ---- | ----------- |
| Updated at | str | The sensor update datetime, it will update at every day 00:00. |
| Is workday | str |  Indicates whether it is a working day. |
| Is vacation | str | Indicates whether it is a holiday. |
| Is customize date | str | This day a custom date entered manually.|

The value of `Is workday`, `Is vacation` and `Is customize date` there will be only two changes: `true` and `false`.  

> [!IMPORTANT] 
> Reloading is required after configuring a custom date

Start your automation!

## Base on
[chinese-calendar](https://github.com/LKI/chinese-calendar)

## LICENSE
[MIT](https://github.com/touero/HaVacation/blob/main/LICENSE) [@touero](https://github.com/touero)

