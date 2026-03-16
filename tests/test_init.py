import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.ha_vacation.const import DOMAIN

async def test_async_setup(hass):
    from custom_components.ha_vacation import async_setup

    assert await async_setup(hass, {}) is True

@pytest.fixture
def mock_entry(hass):
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Test Entry",
        data={},
        entry_id="1234",
    )
    entry.add_to_hass(hass)
    return entry

async def test_async_setup_entry(hass, mock_entry, monkeypatch):
    called = {}

    async def fake_forward_entry_setups(entry, platforms):
        called["entry"] = entry
        called["platforms"] = platforms
        return True

    monkeypatch.setattr(
        hass.config_entries,
        "async_forward_entry_setups",
        fake_forward_entry_setups,
    )

    from custom_components.ha_vacation import async_setup_entry

    result = await async_setup_entry(hass, mock_entry)

    assert result is True
    assert called["entry"] == mock_entry
    assert called["platforms"] == ["sensor"]

async def test_async_unload_entry(hass, mock_entry, monkeypatch):
    called = {}

    async def fake_forward_entry_unload(entry, component):
        called["entry"] = entry
        called["component"] = component
        return True

    monkeypatch.setattr(hass.config_entries, "async_forward_entry_unload", fake_forward_entry_unload)

    from custom_components.ha_vacation import async_unload_entry
    result = await async_unload_entry(hass, mock_entry)
    assert result is True
    assert called["entry"] == mock_entry
    assert called["component"] == "sensor"
