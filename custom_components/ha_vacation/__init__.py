from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType

import logging
import subprocess

_LOGGER = logging.getLogger(__name__)

DOMAIN = "ha_vacation"


def _upgrade_chinese_calendar():
    subprocess.check_call(
        ["pip", "install", "--upgrade", "chinesecalendar"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True


async def async_setup_entry(hass, entry):
    try:
        await hass.async_add_executor_job(_upgrade_chinese_calendar)
    except Exception:
        _LOGGER.warning("Failed to upgrade chinesecalendar, using installed version")

    await hass.config_entries.async_forward_entry_setups(
        entry,
        ["sensor"],
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")
