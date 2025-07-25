import datetime
import pytest
from unittest.mock import Mock, patch

from custom_components.ha_vacation.ha_vacation_date import HaVacationDate
from custom_components.ha_vacation.constants import Options

@pytest.fixture
def mock_customize():
    mock = Mock()
    return mock

@patch("custom_components.ha_vacation.ha_vacation_date.is_holiday", return_value=True)
@patch("custom_components.ha_vacation.ha_vacation_date.is_workday", return_value=False)
def test_customize_vacation_day(mock_is_workday, mock_is_holiday, mock_customize):
    mock_customize.sync_load_customize_date.side_effect = [
        ["2025-07-22"],
        []
    ]
    date = HaVacationDate(
        name=Options.TODAY.value,
        customize_date=mock_customize,
        today=datetime.date(2025, 7, 22),
        now="2025-07-22 10:00:00"
    )

    assert str(date) == "2025-07-22"
    assert date.is_vacation == "true"
    assert date.is_workday == "false"
    assert date.in_customize_date is True
    assert date.is_customize_date == "true"
    assert date.state == "vacation"
    assert date.attributes == {
        "updated_at": "2025-07-22 10:00:00",
        "today": "2025-07-22",
        "is_workday": "false",
        "is_vacation": "true",
        "is_customize_date": "true",
    }

@patch("custom_components.ha_vacation.ha_vacation_date.is_holiday", return_value=False)
@patch("custom_components.ha_vacation.ha_vacation_date.is_workday", return_value=True)
def test_customize_workday_day(mock_is_workday, mock_is_holiday, mock_customize):
    mock_customize.sync_load_customize_date.side_effect = [
        [],
        ["2025-07-22"]
    ]
    date = HaVacationDate(
        name=Options.TODAY.value,
        customize_date=mock_customize,
        today=datetime.date(2025, 7, 22),
        now="2025-07-22 12:00:00"
    )

    assert date.is_vacation == "false"
    assert date.is_workday == "true"
    assert date.in_customize_date is True
    assert date.is_customize_date == "true"
    assert date.state == "workday"

@patch("custom_components.ha_vacation.ha_vacation_date.is_holiday", return_value=True)
@patch("custom_components.ha_vacation.ha_vacation_date.is_workday", return_value=False)
def test_not_in_customize_and_holiday(mock_is_workday, mock_is_holiday, mock_customize):
    mock_customize.sync_load_customize_date.side_effect = [
        [],
        []
    ]
    date = HaVacationDate(
        name=Options.TOMORROW.value,
        customize_date=mock_customize,
        today=datetime.date(2025, 7, 21),
        now="2025-07-21 23:00:00"
    )

    assert date.is_vacation == "true"
    assert date.is_workday == "false"
    assert date.in_customize_date is False
    assert date.is_customize_date == "false"
    assert date.state == "vacation"

def test_yesterday_logic(mock_customize):
    mock_customize.sync_load_customize_date.side_effect = [[], []]
    date = HaVacationDate(
        name=Options.YESTERDAY.value,
        customize_date=mock_customize,
        today=datetime.date(2025, 7, 22),
        now="2025-07-22 09:00:00"
    )
    assert date.date_datetime == datetime.date(2025, 7, 21)

def test_invalid_date_option(mock_customize):
    mock_customize.sync_load_customize_date.side_effect = [[], []]
    with pytest.raises(ValueError, match="Invalid date option"):
        HaVacationDate(
            name="invalid",
            customize_date=mock_customize,
            today=datetime.date(2025, 7, 22),
            now="2025-07-22 09:00:00"
        )

def test_update_method(mock_customize):
    mock_customize.sync_load_customize_date.side_effect = [[], []]
    date = HaVacationDate(
        name=Options.TODAY.value,
        customize_date=mock_customize,
        today=datetime.date(2025, 7, 22),
        now="2025-07-22 08:00:00"
    )

    with patch("custom_components.ha_vacation.ha_vacation_date.datetime") as mock_datetime:
        mock_datetime.date.today.return_value = datetime.date(2025, 7, 23)
        mock_now = datetime.datetime(2025, 7, 23, 9, 0, 0)
        mock_datetime.datetime.now.return_value = mock_now
        date.update()

        assert date.today == datetime.date(2025, 7, 23)
        assert date.now == "2025-07-23 09:00:00"
