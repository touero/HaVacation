from enum import Enum


CONFIG_FILE = "custom_components/ha_vacation/ha_vacation.yaml"


class Options(Enum):
    TODAY: str = "today"
    YESTERDAY: str = "yesterday"
    TOMORROW: str = "tomorrow"

    @staticmethod
    def to_list() -> list:
        return [option.value for option in Options]


class HaVacationAttributes(Enum):
    TRUE: str = "true"
    FALSE: str = "false"


class CustomizeMenuItems(Enum):
    ADD_VACATION_DATE: str = "添加自定义假期"
    DELETE_VACATION_DATE: str = "删除自定义假期"
    ADD_WORKDAY_DATE: str = "添加自定义工作日"
    DELETE_WORKDAY_DATE: str = "删除自定义工作日"

    @staticmethod
    def to_dict():
        return {item.name.lower(): item.value for item in CustomizeMenuItems}


class CustomizeDateSet(Enum):
    VACATION: str = "vacation_dates"
    WORKDAY: str = "workday_dates"
