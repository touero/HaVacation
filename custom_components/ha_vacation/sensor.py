import logging
from datetime import datetime, timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_time_change

from .constants import Options
from .date_visitor import DateVisitor


_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    date = entry.data.get("date", "today")
    vacation_sensor = VacationSensor(hass, date)
    async_add_entities([vacation_sensor])

    async def update_at_midnight(now):
        vacation_sensor.update_attributes()

    async_track_time_change(
        hass,
        update_at_midnight,
        hour=0,
        minute=1,
        second=0,
    )

def change_attributes(date):
    date_visitor = DateVisitor()
    if Options.TODAY.value in date:
        return date_visitor.today_is_workday, date_visitor.today_is_holiday
    elif Options.TOMORROW.value in date:
        return date_visitor.tomorrow_is_workday, date_visitor.tomorrow_is_holiday
    elif Options.YESTERDAY.value in date:
        return date_visitor.yesterday_is_workday, date_visitor.yesterday_is_holiday
    else:
        _LOGGER.error(f"VacationSensor 未知日期: {date}")
        raise ValueError(f"VacationSensor 未知日期: {date}")

class VacationSensor(SensorEntity):

    def __init__(self, hass, date):
        self._hass = hass
        self._name = f"HaVacation {date}"
        self._unique_id = f"vacation_sensor_{date}"
        self.date = date
        workday, vacation = change_attributes(date)
        self._attributes: dict = {
            "Workday": workday,
            "Vacation": vacation,
            "UpdatedAt": 'init'
        }

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def name(self):
        return self._name

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update_attributes(self):
        old_workday = self._attributes["Workday"]
        old_vacation = self._attributes["Vacation"]

        workday, vacation = change_attributes(self.date)
        self._attributes["Workday"] = workday
        self._attributes["Vacation"] = vacation


        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._attributes["UpdatedAt"] = now

        _LOGGER.debug(
            "VacationSensor 属性已更新: Workday %s -> %s, Vacation %s -> %s",
            old_workday, self._attributes["Workday"],
            old_vacation, self._attributes["Vacation"]
        )

        self.schedule_update_ha_state()
