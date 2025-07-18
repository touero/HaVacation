import pytest
from homeassistant.config_entries import ConfigEntry
from custom_components.ha_vacation.const import DOMAIN

async def test_async_setup(hass):
    from homeassistant.setup import async_setup_component
    assert await async_setup_component(hass, DOMAIN, {}) is True

@pytest.fixture
def mock_entry(hass):
    entry = ConfigEntry(
        version=1,
        domain=DOMAIN,
        title="Test Entry",
        data={},
        source="user",
        entry_id="1234",
    )
    hass.config_entries._entries[entry.entry_id] = entry
    return entry

async def test_async_setup_entry(hass, mock_entry):
    from custom_components.ha_vacation import async_setup_entry
    result = await async_setup_entry(hass, mock_entry)
    assert result is True

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
