import os
import logging
import yaml
from homeassistant.core import HomeAssistant


from .constants import CustomizeDateSet

_LOGGER = logging.getLogger(__name__)


class CustomizeDate:
    def __init__(self, hass: HomeAssistant, config_file: str):
        self.hass = hass
        self.file_path = self.hass.config.path(config_file)
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def _load_local_data(self) -> dict:
        default_data = {CustomizeDateSet.VACATION.value: [], CustomizeDateSet.WORKDAY.value: []}
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as file:
                    default_data = yaml.safe_load(file) or {}
                    if not isinstance(default_data, dict):
                        _LOGGER.warning("Read %s format error, reset to list: %s", self.file_path, self.file_path)
                        default_data = {CustomizeDateSet.VACATION.value: [], CustomizeDateSet.WORKDAY.value: []}
            except yaml.YAMLError as e:
                _LOGGER.error("Read %s failed: %s", self.file_path, e)
        return default_data

    async def _load_original_data(self) -> dict:
        return self._load_local_data()

    async def write_customize_date_to_yaml(self, data_written):
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                yaml.safe_dump(data_written, file, allow_unicode=True, default_flow_style=False)
            _LOGGER.info("Date saved to %s: %s", self.file_path, data_written)
        except OSError as e:
            _LOGGER.error("Write %s failed: %s", self.file_path, e)

    async def save_customize_date(self, date_type: str, date: str):
        default_data = await self._load_original_data()
        default_data[date_type].append(date)
        await self.write_customize_date_to_yaml(default_data)

    async def read_customize_date_from_yaml(self, date_type: str):
        default_data = await self._load_original_data()
        return default_data[date_type]

    async def delete_customize_date_from_yaml(self, date_type: str, date: str):
        default_data = await self._load_original_data()
        try:
            default_data[date_type].remove(date)
            with open(self.file_path, "w", encoding="utf-8") as file:
                yaml.safe_dump(default_data, file, allow_unicode=True, default_flow_style=False)
        except ValueError:
            _LOGGER.warning("Date %s not found in %s", date, self.file_path)
        except OSError as e:
            _LOGGER.error("Delete write %s failed: %s", self.file_path, e)

    def sync_load_customize_date(self, date_type: str):
        default_data = self._load_local_data()
        return default_data[date_type]
