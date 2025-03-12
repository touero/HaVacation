import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .constants import Options

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
                _LOGGER.info("创建配置条目: %s", date)
                return self.async_create_entry(title=date, data=user_input)

        data_schema = vol.Schema(
            {
                vol.Required("date", default="today"): vol.In(OPTIONS),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(entry):
        return HaVacationOptionsFlow(entry)


class HaVacationOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, entry):
        self.entry = entry

    async def async_step_init(self, user_input=None):
        errors = {}
        if user_input is not None:
            date = user_input.get("date", "today")
            if date not in OPTIONS:
                errors["date"] = "invalid_date"
                _LOGGER.error("无效的日期选项: %s", date)
            else:
                _LOGGER.info("更新配置: %s", date)
                return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Required("date", default=self.entry.data.get("date", "today")): vol.In(OPTIONS),
            }
        )

        return self.async_show_form(step_id="init", data_schema=data_schema, errors=errors)
