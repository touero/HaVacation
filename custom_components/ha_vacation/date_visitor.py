import datetime
from chinese_calendar import is_holiday, is_workday


class DateVisitor:
    def __init__(self):
        self.today = datetime.date.today()
        self.tomorrow = self.today + datetime.timedelta(days=1)
        self.yesterday = self.today - datetime.timedelta(days=1)

    @property
    def today_is_holiday(self) -> bool:
        return is_holiday(self.today)

    @property
    def today_is_workday(self) -> bool:
        return is_workday(self.today)

    @property
    def tomorrow_is_holiday(self) -> bool:
        return is_holiday(self.tomorrow)

    @property
    def tomorrow_is_workday(self) -> bool:
        return is_workday(self.tomorrow)

    @property
    def yesterday_is_holiday(self) -> bool:
        return is_holiday(self.yesterday)

    @property
    def yesterday_is_workday(self) -> bool:
        return is_workday(self.yesterday)
