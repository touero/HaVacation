import logging
from datetime import datetime
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_time_change

from .constants import Options
from .date_visitor import DateVisitor

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    date = entry.data.get("date", "today")
    vacation_sensor = VacationSensor(hass, date)
    async_add_entities([vacation_sensor])

    async def update_at_midnight():
        vacation_sensor.update_attributes()

    async_track_time_change(
        hass,
        update_at_midnight,
        hour=0,
        minute=0,
        second=1,
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
        raise ValueError(f"VacationSensor 未知日期: {date}")


class VacationSensor(Entity):

    def __init__(self, hass, date):
        self._hass = hass
        self._name = f"ha_vacation_{date}"
        self._unique_id = f"vacation_sensor_{date}"
        self.date = date
        workday, vacation = change_attributes(date)
        self._attributes: dict = {
            "workday": workday,
            "vacation": vacation,
            "update": 'initialization'
        }

    @property
    def state(self):
        return 'workday' if self._attributes["workday"] else 'vacation'

    @property
    def should_poll(self):
        return False

    @property
    def icon(self):
        return "mdi:calendar"

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
        workday, vacation = change_attributes(self.date)
        self._attributes["workday"] = workday
        self._attributes["vacation"] = vacation

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._attributes["update"] = now

        self.schedule_update_ha_state()
