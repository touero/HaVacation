import pytest
from unittest.mock import MagicMock, patch, call

from custom_components.ha_vacation.sensor import VacationSensor, async_setup_entry

@pytest.fixture
def mock_hass():
    hass = MagicMock()
    hass.bus.fire = MagicMock()
    return hass

@pytest.fixture
def mock_customize_date(monkeypatch):
    # Patch CustomizeDate to return a MagicMock
    mock = MagicMock()
    monkeypatch.setattr("custom_components.ha_vacation.sensor.CustomizeDate", lambda hass, config: mock)
    return mock

@pytest.fixture
def mock_ha_vacation_date(monkeypatch):
    mock = MagicMock()
    mock.attributes = {"foo": "bar"}
    mock.state = "workday"
    monkeypatch.setattr("custom_components.ha_vacation.sensor.HaVacationDate", lambda date, customize: mock)
    return mock

def test_vacation_sensor_properties(mock_hass, mock_customize_date, mock_ha_vacation_date):
    sensor = VacationSensor(mock_hass, "today")
    # test all properties
    assert sensor.state == "workday"
    assert sensor.should_poll is False
    assert sensor.icon == "mdi:calendar"
    assert sensor.unique_id == "vacation_sensor_today"
    assert sensor.name == "ha_vacation_today"
    assert sensor.extra_state_attributes == {"foo": "bar"}

def test_update_attributes_fires_events_and_updates_state(mock_hass, mock_customize_date, mock_ha_vacation_date):
    sensor = VacationSensor(mock_hass, "today")
    sensor.hass = mock_hass
    # Patch async_write_ha_state
    sensor.async_write_ha_state = MagicMock()
    # Patch underlying ha_vacation_date
    sensor.ha_vacation_date.update = MagicMock()
    sensor.ha_vacation_date.attributes = {"new": "attr"}
    sensor.ha_vacation_date.state = "vacation"
    # test update_attributes
    sensor.update_attributes()
    # test event fired before and after update
    assert mock_hass.bus.fire.call_args_list[0][0][0] == "ha_vacation_updating"
    assert mock_hass.bus.fire.call_args_list[1][0][0] == "ha_vacation_updated"
    # attributes updated
    assert sensor._attributes == {"new": "attr"}
    # state updated
    assert sensor.state == "vacation"
    # async_write_ha_state called
    sensor.async_write_ha_state.assert_called_once()

@pytest.mark.asyncio
async def test_async_setup_entry(monkeypatch, mock_hass, mock_customize_date, mock_ha_vacation_date):
    entry = MagicMock()
    entry.data = {"date": "today"}
    add_entities = MagicMock()
    
    # Patch async_track_time_change to capture the callback
    captured_callback = {}
    def fake_async_track_time_change(hass, callback, hour, minute, second):
        captured_callback["cb"] = callback
    monkeypatch.setattr("custom_components.ha_vacation.sensor.async_track_time_change", fake_async_track_time_change)
    
    await async_setup_entry(mock_hass, entry, add_entities)

    add_entities.assert_called_once()
    entity = add_entities.call_args[0][0][0]
    assert isinstance(entity, VacationSensor)

    # Patch sensor.update_attributes to verify it gets called
    entity.update_attributes = MagicMock()
    
    # Trigger the midnight callback manually
    await captured_callback["cb"](None)

    entity.update_attributes.assert_called_once()
