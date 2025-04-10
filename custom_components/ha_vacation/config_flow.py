import re
import logging
from typing import Optional

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.config_entries import OptionsFlow
from .constants import Options, CustomizeMenuItems, CustomizeDateSet, CONFIG_FILE
from .customize_date import CustomizeDate

_LOGGER = logging.getLogger(__name__)

DOMAIN = "ha_vacation"
OPTIONS = Options.to_list()


class HaVacationConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            date = user_input.get("date", "today")
            if date not in OPTIONS:
                errors["date"] = "invalid_date"
                _LOGGER.error("无效的日期选项: %s", date)
            else:
                _LOGGER.info("创建配置条目: %s" ,date)
                return self.async_create_entry(title=date, data=user_input)

        data_schema = vol.Schema({vol.Required("date", default="today"): vol.In(OPTIONS)})

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(entry):
        return HaVacationOptionsFlow(entry)


class HaVacationOptionsFlow(OptionsFlow):
    def __init__(self, entry):
        self.entry = entry
        self.customize_date: Optional[CustomizeDate | None] = None

    async def async_step_init(self, user_input=None):
        if self.customize_date is None:
            self.customize_date = CustomizeDate(self.hass, CONFIG_FILE)
        return self.async_show_menu(step_id="menu", menu_options=CustomizeMenuItems.to_dict())

    async def async_step_menu(self, user_input=None):
        if user_input == CustomizeMenuItems.ADD_VACATION_DATE.name:
            step = await self.async_step_add_vacation_date()
        elif user_input == CustomizeMenuItems.DELETE_VACATION_DATE.name:
            step = await self.async_step_delete_vacation_date()
        elif user_input == CustomizeMenuItems.ADD_WORKDAY_DATE.name:
            step = await self.async_step_add_workday_date()
        elif user_input == CustomizeMenuItems.DELETE_WORKDAY_DATE.name:
            step = await self.async_step_delete_workday_date()
        else:
            step = self.async_show_menu(step_id="menu", menu_options=CustomizeMenuItems.to_dict())
        return step

    async def async_step_add_vacation_date(self, user_input=None):
        errors = {}
        if user_input is not None:
            date = user_input.get("date", "")
            if not date or not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
                errors["date"] = "请输入有效的日期格式（YYYY-MM-DD）"
            else:
                await self.customize_date.save_customize_date(CustomizeDateSet.VACATION.value, date)
                _LOGGER.info("日期已保存到 %s: %s", CONFIG_FILE, date)
                return self.async_abort(reason="添加自定义假期日期成功")
        data_schema = vol.Schema({vol.Required("date"): vol.All(str, vol.Length(min=1))})
        return self.async_show_form(step_id="add_vacation_date", data_schema=data_schema, errors=errors)

    async def async_step_delete_vacation_date(self, user_input=None):
        errors = {}
        if user_input is not None:
            date = user_input.get("date", "")
            if not date:
                errors["date"] = "invalid_date"
                _LOGGER.error("无效的日期选项: %s",date)
            else:
                _LOGGER.info("创建配置条目: %s", date)
                await self.customize_date.delete_customize_date_from_yaml(CustomizeDateSet.VACATION.value, date)
                return self.async_abort(reason="删除自定义假期日期成功")
        default_data = await self.customize_date.read_customize_date_from_yaml(CustomizeDateSet.VACATION.value)
        data_schema = vol.Schema({vol.Required("date"): vol.In(default_data)})
        return self.async_show_form(step_id="delete_vacation_date", data_schema=data_schema, errors=errors)

    async def async_step_add_workday_date(self, user_input=None):
        errors = {}
        if user_input is not None:
            date = user_input.get("date", "")
            if not date or not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
                errors["date"] = "请输入有效的日期格式（YYYY-MM-DD）"
            else:
                await self.customize_date.save_customize_date(CustomizeDateSet.WORKDAY.value, date)
                _LOGGER.info("日期已保存到 %s: %s", CONFIG_FILE, date)
                return self.async_abort(reason="添加自定义工作日日期成功")
        data_schema = vol.Schema({vol.Required("date"): vol.All(str, vol.Length(min=1))})
        return self.async_show_form(step_id="add_workday_date", data_schema=data_schema, errors=errors)

    async def async_step_delete_workday_date(self, user_input=None):
        errors = {}
        if user_input is not None:
            date = user_input.get("date", "")
            if not date:
                errors["date"] = "invalid_date"
                _LOGGER.error("无效的日期选项: %s",date)
            else:
                _LOGGER.info("创建配置条目: %s", date)
                await self.customize_date.delete_customize_date_from_yaml(CustomizeDateSet.WORKDAY.value, date)
                return self.async_abort(reason="删除自定义工作日期成功")
        default_data = await self.customize_date.read_customize_date_from_yaml(CustomizeDateSet.WORKDAY.value)
        data_schema = vol.Schema({vol.Required("date"): vol.In(default_data)})
        return self.async_show_form(step_id="delete_vacation_date", data_schema=data_schema, errors=errors)
