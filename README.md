# HaVacation

A Chinese workday/vacation integration for Home-Assistant.

## Installation

### Hacs Install

If you have installed [hacs](https://github.com/hacs/integration), please click:  
[![ByHacs](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=touero&repository=HaVacation&category=integration)  
After restart Home-Assistant, you can find it in the integration menu or click:  
[![add_integration](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=ha_vacation)

### Manual Install
Go to [Releases](https://github.com/touero/HaVacation/releases/) download the HaVacation.tar.gz, and move it to `HomeAssistant/custom_components` and execute:

```shell
tar -zxvf ha_vacation.tar.gz
```
And then restart your home-assistant.

In add integration search HaVacation configure it.

## Details

After you will get 1-3 sensor:

![preview](https://github.com/touero/HaVacation/blob/main/preview/sensor.png)

And then have attribute:

![preview](https://github.com/touero/HaVacation/blob/main/preview/sensor_details.png)

> [!TIP]
> `IsWorkday` indicates whether it is a working day.  
> `IsVacation` indicates whether it is a holiday.  
> The value of `IsWorkday` and `IsVacation` there will be only two changes: `true` and `false`.  
> UpdatedAt is the sensor update datetime, it will update at every day 00:00.  

Start your automation!

## Maintainers
[@touero](https://github.com/touero)

## Base on

[chinese-calendar](https://github.com/LKI/chinese-calendar)
