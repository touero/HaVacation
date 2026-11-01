from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_point_in_time
from homeassistant.helpers.typing import ConfigType
from homeassistant.util import dt as dt_util

import asyncio
import datetime as dt
import importlib
import logging
import subprocess
import sys

from packaging.version import InvalidVersion, Version

_LOGGER = logging.getLogger(__name__)

DOMAIN = "ha_vacation"

PACKAGE = "chinesecalendar"
MODULE = "chinese_calendar"
VERSION_URLS = (
    "https://pypi.org/pypi/{}/json".format(PACKAGE),
    "https://pypi.tuna.tsinghua.edu.cn/pypi/{}/json".format(PACKAGE),
)

CHECK_MONTH_DAY = (12, 15)
CHECK_HOUR = 3


def _installed_version():
    from importlib.metadata import PackageNotFoundError, version

    try:
        return version(PACKAGE)
    except PackageNotFoundError:
        return None


def _upgrade_chinese_calendar():
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--upgrade", "--no-deps", PACKAGE],
        capture_output=True,
        check=True,
        timeout=300,
    )


def _reload_chinese_calendar():
    """Swap the freshly installed package into the running process."""
    for name in [n for n in sys.modules if n == MODULE or n.startswith("{}.".format(MODULE))]:
        del sys.modules[name]
    importlib.invalidate_caches()

    import chinese_calendar

    from . import ha_vacation_date

    ha_vacation_date._calendar = chinese_calendar


async def _async_latest_version(hass: HomeAssistant):
    session = async_get_clientsession(hass)
    for url in VERSION_URLS:
        try:
            async with asyncio.timeout(15):
                response = await session.get(url)
                if response.status != 200:
                    continue
                return (await response.json(content_type=None))["info"]["version"]
        except Exception:  # noqa: BLE001
            continue
    return None


def _is_newer(latest, current) -> bool:
    if not current:
        return True
    try:
        return Version(latest) > Version(current)
    except InvalidVersion:
        return latest != current


def _data_max_year():
    """已加载的数据覆盖到哪一年。"""
    try:
        constants = importlib.import_module("{}.constants".format(MODULE))
        return max(day.year for day in constants.holidays)
    except Exception:  # noqa: BLE001
        return None


def _check_window_open() -> bool:
    """数据缺了才检查：12 月 15 日之后缺明年的，或已经跨年却缺当年数据。"""
    today = dt.date.today()
    covered = _data_max_year()
    if covered is None:
        return True
    if (today.month, today.day) >= CHECK_MONTH_DAY:
        return covered < today.year + 1
    return covered < today.year


def _next_check_time() -> dt.datetime:
    """下一次（今年的或明年的）12 月 15 日。"""
    now = dt_util.now()
    target = now.replace(
        month=CHECK_MONTH_DAY[0],
        day=CHECK_MONTH_DAY[1],
        hour=CHECK_HOUR,
        minute=0,
        second=0,
        microsecond=0,
    )
    if target <= now:
        target = target.replace(year=target.year + 1)
    return target


async def _async_update_calendar(hass: HomeAssistant) -> None:
    latest = await _async_latest_version(hass)
    current = _installed_version()
    if latest is None or not _is_newer(latest, current):
        return

    _LOGGER.info("Updating %s %s -> %s", PACKAGE, current or "unknown", latest)
    try:
        await hass.async_add_executor_job(_upgrade_chinese_calendar)
        await hass.async_add_executor_job(_reload_chinese_calendar)
    except Exception:  # noqa: BLE001
        _LOGGER.warning("Failed to update %s, using installed version", PACKAGE)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True


async def async_setup_entry(hass, entry):
    unsub = None

    def _schedule() -> None:
        nonlocal unsub
        unsub = async_track_point_in_time(hass, _async_check, _next_check_time())

    async def _async_check(_now) -> None:
        nonlocal unsub
        unsub = None
        await _async_update_calendar(hass)
        _schedule()

    if not getattr(hass.config, "skip_pip", False) and _check_window_open():
        hass.async_create_background_task(
            _async_update_calendar(hass), "ha_vacation_calendar_update"
        )

    _schedule()
    entry.async_on_unload(lambda: unsub and unsub())

    await hass.config_entries.async_forward_entry_setups(
        entry,
        ["sensor"],
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")
