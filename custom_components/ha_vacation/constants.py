from enum import Enum

class Options(Enum):
    TODAY = "today"
    YESTERDAY = "yesterday"
    TOMORROW = "tomorrow"

    @staticmethod
    def to_list():
        return [option.value for option in Options]


class HaVacationAttributes(Enum):
    TRUE = "true"
    FALSE = "false"
