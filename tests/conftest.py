"""Fixtures for testing."""

import pytest
import homeassistant.core as hass_core


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations."""
    return

_original_set_time_zone = hass_core.Config.set_time_zone

def _patched_set_time_zone(self, tz_str):
    if tz_str == "US/Pacific":
        tz_str = "America/Los_Angeles"
    _original_set_time_zone(self, tz_str)

hass_core.Config.set_time_zone = _patched_set_time_zone

@pytest.fixture
async def hass(loop, request):
    """Home Assistant instance with valid timezone."""
    from pytest_homeassistant_custom_component.common import async_test_home_assistant
    hass = await async_test_home_assistant(loop, load_registries=True)
    yield hass
    await hass.async_stop()
