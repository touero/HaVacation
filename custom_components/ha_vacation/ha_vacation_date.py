import datetime
from typing import Optional
from dataclasses import dataclass, field

from chinese_calendar import is_holiday, is_workday
from .constants import Options

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
    def is_vacation(self) -> bool:
        return is_holiday(self.date_datetime)

    @property
    def is_workday(self) -> bool:
        return is_workday(self.date_datetime)

    @property
    def state(self) -> str:
        return 'workday' if self.is_workday else 'vacation'

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
            "IsWorkday": self.is_workday,
            "IsVacation": self.is_vacation,
            "UpdatedAt": self.now
        }
