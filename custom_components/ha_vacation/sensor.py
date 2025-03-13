import logging
from datetime import datetime
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_time_change

from .ha_vacation_date import HaVacationDate

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
        minute=0,
        second=1,
    )


class VacationSensor(Entity):

    def __init__(self, hass, date):
        self._hass = hass
        self._name = f"ha_vacation_{date}"
        self._unique_id = f"vacation_sensor_{date}"

        self.ha_vacation_date = HaVacationDate(date)
        self._attributes: dict = {
            self.ha_vacation_date.name: str(self.ha_vacation_date),
            "IsWorkday": self.ha_vacation_date.is_workday,
            "IsVacation": self.ha_vacation_date.is_vacation,
            "UpdateAt": 'initialization'
        }

    @property
    def state(self):
        return 'workday' if self._attributes["IsWorkday"] else 'vacation'

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
        self.ha_vacation_date.update()
        self._attributes[self.ha_vacation_date.name] = self.ha_vacation_date
        self._attributes["IsWorkday"] = self.ha_vacation_date.is_workday
        self._attributes["IsVacation"] = self.ha_vacation_date.is_vacation
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._attributes["UpdateAt"] = now

        self.schedule_update_ha_state()
