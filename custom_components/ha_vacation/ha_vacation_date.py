import datetime
from typing import Optional
from dataclasses import dataclass, field

from chinese_calendar import is_holiday, is_workday
from .constants import Options, HaVacationAttributes

@dataclass
class HaVacationDate:
    name: str
    now: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today: datetime.date = field(default_factory=datetime.date.today)
    attributes: dict = field(default_factory=dict, init=False)
    date_datetime: Optional[datetime.date] = field(default=None, init=False)

    def __post_init__(self):
        self.update_date()
        self.update_attributes()

    def __str__(self) -> str:
        return self.date_datetime.strftime("%Y-%m-%d")

    @property
    def is_vacation(self) -> str:
        if is_holiday(self.date_datetime):
            return HaVacationAttributes.TRUE.value
        else:
            return HaVacationAttributes.FALSE.value

    @property
    def is_workday(self) -> str:
        if is_workday(self.date_datetime):
            return HaVacationAttributes.TRUE.value
        else:
            return HaVacationAttributes.FALSE.value

    @property
    def state(self) -> str:
        return 'workday' if self.is_workday == HaVacationAttributes.TRUE.value else 'vacation'

    def update(self):
        self.today = datetime.date.today()
        self.now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.update_date()
        self.update_attributes()

    def update_date(self):
        if self.name == Options.TODAY.value:
            self.date_datetime = self.today
        elif self.name == Options.TOMORROW.value:
            self.date_datetime = self.today + datetime.timedelta(days=1)
        elif self.name == Options.YESTERDAY.value:
            self.date_datetime = self.today - datetime.timedelta(days=1)
        else:
            raise ValueError("Invalid date option")

    def update_attributes(self):
        self.attributes = {
            self.name: str(self),
            "is_workday": self.is_workday,
            "is_vacation": self.is_vacation,
            "updated_at": self.now
        }
