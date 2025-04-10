import datetime
from chinese_calendar import is_holiday, is_workday
from dataclasses import dataclass, field
from typing import Optional

from .constants import Options, HaVacationAttributes, CustomizeDateSet
from .customize_date import CustomizeDate


@dataclass
class HaVacationDate:
    name: str
    customize_date: CustomizeDate
    now: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today: datetime.date = field(default_factory=datetime.date.today)
    attributes: dict = field(default_factory=dict, init=False)
    date_datetime: Optional[datetime.date] = field(default=None, init=False)
    customize_vacation_dates: list = field(default_factory=list, init=False)
    customize_workday_dates: list = field(default_factory=list, init=False)

    def __post_init__(self):
        self.customize_vacation_dates = self.customize_date.sync_load_customize_date(CustomizeDateSet.VACATION.value)
        self.customize_workday_dates = self.customize_date.sync_load_customize_date(CustomizeDateSet.WORKDAY.value)
        self.update_date()
        self.update_attributes()

    def __str__(self) -> str:
        return self.date_datetime.strftime("%Y-%m-%d")

    @property
    def is_vacation(self) -> str:
        if self.in_customize_date:
            if str(self) in self.customize_vacation_dates:
                return HaVacationAttributes.TRUE.value
            else:
                return HaVacationAttributes.FALSE.value

        elif is_holiday(self.date_datetime):
            return HaVacationAttributes.TRUE.value
        else:
            return HaVacationAttributes.FALSE.value

    @property
    def is_workday(self) -> str:
        if self.in_customize_date:
            if str(self) in self.customize_workday_dates:
                return HaVacationAttributes.TRUE.value
            else:
                return HaVacationAttributes.FALSE.value

        elif is_workday(self.date_datetime):
            return HaVacationAttributes.TRUE.value
        else:
            return HaVacationAttributes.FALSE.value

    @property
    def in_customize_date(self) -> bool:
        if str(self) in self.customize_vacation_dates or str(self) in self.customize_workday_dates:
            return True
        return False

    @property
    def is_customize_date(self) -> str:
        if self.in_customize_date:
            return HaVacationAttributes.TRUE.value
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
            "updated_at": self.now,
            self.name: str(self),
            "is_workday": self.is_workday,
            "is_vacation": self.is_vacation,
            "is_customize_date": self.is_customize_date
        }
