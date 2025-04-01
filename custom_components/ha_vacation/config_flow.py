import logging
import os

import voluptuous as vol
import yaml
from homeassistant import config_entries
from homeassistant.core import callback, HomeAssistant

from .constants import Options

_LOGGER = logging.getLogger(__name__)

DOMAIN = "ha_vacation"
CONFIG_FILE = "custom_components/ha_vacation/ha_vacation.yaml"
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
            date = user_input.get("date", "")
            if not date:
                errors["date"] = "invalid_date"
                _LOGGER.error("日期不能为空")
            else:
                await self._save_to_yaml(self.hass, date)
                _LOGGER.info("日期已保存到 %s: %s", CONFIG_FILE, date)

                return self.async_abort(reason="成功添加日期")

        data_schema = vol.Schema(
            {
                vol.Required("date"): vol.All(str, vol.Length(min=1)),  # 允许自由输入
            }
        )

        return self.async_show_form(step_id="init", data_schema=data_schema, errors=errors)

    async def _save_to_yaml(self, hass: HomeAssistant, date: str):
        """将日期保存到 YAML 文件（追加写入，使用列表格式）"""
        file_path = hass.config.path(CONFIG_FILE)

        # 确保文件夹存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # 读取已有数据
        data = {"dates": []}  # 初始化默认结构
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = yaml.safe_load(file) or {}
                    if not isinstance(data, dict) or "dates" not in data:
                        _LOGGER.warning(f"YAML 数据格式错误，重置为列表: {file_path}")
                        data = {"dates": []}
            except yaml.YAMLError as e:
                _LOGGER.error(f"读取 YAML 失败: {e}")

        # 追加新日期
        data["dates"].append(date)

        # 写回文件
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                yaml.safe_dump(data, file, allow_unicode=True, default_flow_style=False)
            _LOGGER.info(f"日期已保存到 {file_path}: {date}")
        except OSError as e:
            _LOGGER.error(f"写入 YAML 文件失败: {e}")