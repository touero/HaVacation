import pytest
import datetime
from unittest.mock import MagicMock

from custom_components.ha_vacation import customize_date
from custom_components.ha_vacation.ha_vacation_date import HaVacationDate
from custom_components.ha_vacation.constants import Options, HaVacationAttributes, CustomizeDateSet

@pytest.fixture
def mock_customize_date():
    mock = MagicMock()
    today = datetime.date.today()
    mock.sync_load_customize_date.side_effect = lambda key: {
        CustomizeDateSet.VACATION.value: ['2099-01-04'],
        CustomizeDateSet.WORKDAY.value: ['2099-01-01', today.strftime("%Y-%m-%d")],
    }.get(key, [])
    return mock

@pytest.mark.parametrize("date_name,expected_date", [
    (Options.TODAY.value, datetime.date.today()),
    (Options.TOMORROW.value, datetime.date.today() + datetime.timedelta(days=1)),
    (Options.YESTERDAY.value, datetime.date.today() - datetime.timedelta(days=1)),
])
def test_update_date_options(date_name, expected_date, mock_customize_date):
    obj = HaVacationDate(name=date_name, customize_date=mock_customize_date)
    assert obj.date_datetime == expected_date
    assert str(obj) == expected_date.strftime("%Y-%m-%d")

def test_update_date_invalid(mock_customize_date):
    with pytest.raises(ValueError):
        HaVacationDate(name="invalid", customize_date=mock_customize_date)

def test_str_method(mock_customize_date):
    obj = HaVacationDate(name=Options.TODAY.value, customize_date=mock_customize_date)
    assert isinstance(str(obj), str)

def test_update_method(mock_customize_date):
    obj = HaVacationDate(name=Options.TODAY.value, customize_date=mock_customize_date)
    old_date = obj.date_datetime
    obj.update()
    assert obj.date_datetime == datetime.date.today()
    assert isinstance(obj.now, str)

def test_update_attributes(mock_customize_date):
    obj = HaVacationDate(name=Options.TODAY.value, customize_date=mock_customize_date)
    obj.update_attributes()
    attrs = obj.attributes
    assert "updated_at" in attrs
    assert obj.name in attrs
    assert "is_workday" in attrs
    assert "is_vacation" in attrs
    assert "is_customize_date" in attrs

def test_in_customize_date(mock_customize_date):
    obj1 = HaVacationDate(name=Options.TODAY.value, customize_date=mock_customize_date)
    obj1.date_datetime = datetime.date(2099, 1, 1)
    assert obj1.in_customize_date is True

    obj2 = HaVacationDate(name=Options.TODAY.value, customize_date=mock_customize_date)
    obj2.date_datetime = datetime.date(2099, 1, 5)
    assert obj2.in_customize_date is False

def test_is_customize_date(mock_customize_date):
    obj1 = HaVacationDate(name=Options.TODAY.value, customize_date=mock_customize_date)
    obj1.date_datetime = datetime.date(2099, 1, 5)
    assert obj1.is_customize_date == HaVacationAttributes.FALSE.value

    obj2 = HaVacationDate(name=Options.TODAY.value, customize_date=mock_customize_date)
    obj2.date_datetime = datetime.date(2099, 1, 1)
    assert obj2.is_customize_date == HaVacationAttributes.TRUE.value


def test_state(mock_customize_date):
    obj = HaVacationDate(name=Options.TODAY.value, customize_date=mock_customize_date)
    type(obj).is_workday = property(lambda self: HaVacationAttributes.TRUE.value)
    assert obj.state == "workday"
    type(obj).is_workday = property(lambda self: HaVacationAttributes.FALSE.value)
    assert obj.state == "vacation"

def test_in_customize_date_is_vacation(mock_customize_date):
    obj1 = HaVacationDate(name=Options.TODAY.value, customize_date=mock_customize_date)
    obj1.date_datetime = datetime.date(2099, 1, 1)
    assert obj1.is_vacation == HaVacationAttributes.FALSE.value

    obj1 = HaVacationDate(name=Options.TODAY.value, customize_date=mock_customize_date)
    obj1.date_datetime = datetime.date(2099, 1, 4)
    assert obj1.is_vacation == HaVacationAttributes.TRUE.value

def test_in_customize_date_is_workday(mock_customize_date):
    obj1 = HaVacationDate(name=Options.TODAY.value, customize_date=mock_customize_date)
    obj1.date_datetime = datetime.date(2099, 1, 1)
    assert obj1.is_workday == HaVacationAttributes.FALSE.value

