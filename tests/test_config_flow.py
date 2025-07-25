import pytest
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.ha_vacation.config_flow import (
    HaVacationConfigFlow, HaVacationOptionsFlow
)
from custom_components.ha_vacation.constants import Options, CustomizeMenuItems, CustomizeDateSet

@pytest.mark.asyncio
async def test_async_step_user_form(hass):
    flow = HaVacationConfigFlow()
    flow.hass = hass
    result = await flow.async_step_user()
    assert result["type"] == "form"
    assert result["step_id"] == "user"

@pytest.mark.asyncio
async def test_async_step_user_valid(hass):
    flow = HaVacationConfigFlow()
    flow.hass = hass
    user_input = {"date": Options.TODAY.value}
    result = await flow.async_step_user(user_input)
    assert result["type"] == "create_entry"
    assert result["title"] == Options.TODAY.value

@pytest.mark.asyncio
async def test_async_step_user_invalid(hass):
    flow = HaVacationConfigFlow()
    flow.hass = hass
    user_input = {"date": "notfound"}
    result = await flow.async_step_user(user_input)
    assert result["type"] == "form"
    assert "date" in result["errors"]

def test_async_get_options_flow():
    entry = MagicMock()
    flow = HaVacationConfigFlow()
    options_flow = flow.async_get_options_flow(entry)
    assert isinstance(options_flow, HaVacationOptionsFlow)

@pytest.fixture
def mock_customize_date():
    mock = MagicMock()
    mock.save_customize_date = AsyncMock()
    mock.read_customize_date_from_yaml = AsyncMock(return_value=["2025-01-01", "2025-01-02"])
    mock.delete_customize_date_from_yaml = AsyncMock()
    return mock

@pytest.mark.asyncio
async def test_optionflow_init_menu(hass, mock_customize_date):
    entry = MagicMock()
    flow = HaVacationOptionsFlow(entry)
    flow.hass = hass
    flow.customize_date = mock_customize_date
    result = await flow.async_step_init()
    assert result["type"] == "menu"
    assert "menu_options" in result

@pytest.mark.asyncio
async def test_optionflow_menu_add_vacation(hass, mock_customize_date):
    entry = MagicMock()
    flow = HaVacationOptionsFlow(entry)
    flow.hass = hass
    flow.customize_date = mock_customize_date
    result = await flow.async_step_menu(CustomizeMenuItems.ADD_VACATION_DATE.name)
    assert result["type"] == "form"
    assert result["step_id"] == "add_vacation_date"

@pytest.mark.asyncio
async def test_optionflow_menu_delete_vacation(hass, mock_customize_date):
    entry = MagicMock()
    flow = HaVacationOptionsFlow(entry)
    flow.hass = hass
    flow.customize_date = mock_customize_date
    result = await flow.async_step_menu(CustomizeMenuItems.DELETE_VACATION_DATE.name)
    assert result["type"] == "form"
    assert result["step_id"] == "delete_vacation_date"

@pytest.mark.asyncio
async def test_optionflow_menu_add_workday(hass, mock_customize_date):
    entry = MagicMock()
    flow = HaVacationOptionsFlow(entry)
    flow.hass = hass
    flow.customize_date = mock_customize_date
    result = await flow.async_step_menu(CustomizeMenuItems.ADD_WORKDAY_DATE.name)
    assert result["type"] == "form"
    assert result["step_id"] == "add_workday_date"

@pytest.mark.asyncio
async def test_optionflow_menu_delete_workday(hass, mock_customize_date):
    entry = MagicMock()
    flow = HaVacationOptionsFlow(entry)
    flow.hass = hass
    flow.customize_date = mock_customize_date
    result = await flow.async_step_menu(CustomizeMenuItems.DELETE_WORKDAY_DATE.name)
    assert result["type"] == "form"
    assert result["step_id"] == "delete_vacation_date"

@pytest.mark.asyncio
async def test_optionflow_menu_default(hass, mock_customize_date):
    entry = MagicMock()
    flow = HaVacationOptionsFlow(entry)
    flow.hass = hass
    flow.customize_date = mock_customize_date
    result = await flow.async_step_menu("invalid")
    assert result["type"] == "menu"

@pytest.mark.asyncio
async def test_optionflow_add_vacation_date_success(hass, mock_customize_date):
    entry = MagicMock()
    flow = HaVacationOptionsFlow(entry)
    flow.hass = hass
    flow.customize_date = mock_customize_date
    result = await flow.async_step_add_vacation_date({"date": "2025-01-01"})
    assert result["type"] == "abort"
    assert result["reason"] == "添加自定义假期日期成功"

@pytest.mark.asyncio
async def test_optionflow_add_vacation_date_invalid(hass, mock_customize_date):
    entry = MagicMock()
    flow = HaVacationOptionsFlow(entry)
    flow.hass = hass
    flow.customize_date = mock_customize_date
    result = await flow.async_step_add_vacation_date({"date": ""})
    assert result["type"] == "form"
    assert "date" in result["errors"]

@pytest.mark.asyncio
async def test_optionflow_add_vacation_date_format(hass, mock_customize_date):
    entry = MagicMock()
    flow = HaVacationOptionsFlow(entry)
    flow.hass = hass
    flow.customize_date = mock_customize_date
    result = await flow.async_step_add_vacation_date({"date": "invalid-format"})
    assert result["type"] == "form"
    assert "date" in result["errors"]

@pytest.mark.asyncio
async def test_optionflow_add_vacation_date_form(hass, mock_customize_date):
    entry = MagicMock()
    flow = HaVacationOptionsFlow(entry)
    flow.hass = hass
    flow.customize_date = mock_customize_date
    result = await flow.async_step_add_vacation_date()
    assert result["type"] == "form"
    assert result["step_id"] == "add_vacation_date"

@pytest.mark.asyncio
async def test_optionflow_delete_vacation_date_success(hass, mock_customize_date):
    entry = MagicMock()
    flow = HaVacationOptionsFlow(entry)
    flow.hass = hass
    flow.customize_date = mock_customize_date
    result = await flow.async_step_delete_vacation_date({"date": "2025-01-01"})
    assert result["type"] == "abort"
    assert result["reason"] == "删除自定义假期日期成功"

@pytest.mark.asyncio
async def test_optionflow_delete_vacation_date_invalid(hass, mock_customize_date):
    entry = MagicMock()
    flow = HaVacationOptionsFlow(entry)
    flow.hass = hass
    flow.customize_date = mock_customize_date
    result = await flow.async_step_delete_vacation_date({"date": ""})
    assert result["type"] == "form"
    assert "date" in result["errors"]

@pytest.mark.asyncio
async def test_optionflow_delete_vacation_date_form(hass, mock_customize_date):
    entry = MagicMock()
    flow = HaVacationOptionsFlow(entry)
    flow.hass = hass
    flow.customize_date = mock_customize_date
    result = await flow.async_step_delete_vacation_date()
    assert result["type"] == "form"
    assert result["step_id"] == "delete_vacation_date"

@pytest.mark.asyncio
async def test_optionflow_add_workday_date_success(hass, mock_customize_date):
    entry = MagicMock()
    flow = HaVacationOptionsFlow(entry)
    flow.hass = hass
    flow.customize_date = mock_customize_date
    result = await flow.async_step_add_workday_date({"date": "2025-01-02"})
    assert result["type"] == "abort"
    assert result["reason"] == "添加自定义工作日日期成功"

@pytest.mark.asyncio
async def test_optionflow_add_workday_date_invalid(hass, mock_customize_date):
    entry = MagicMock()
    flow = HaVacationOptionsFlow(entry)
    flow.hass = hass
    flow.customize_date = mock_customize_date
    result = await flow.async_step_add_workday_date({"date": ""})
    assert result["type"] == "form"
    assert "date" in result["errors"]

@pytest.mark.asyncio
async def test_optionflow_add_workday_date_format(hass, mock_customize_date):
    entry = MagicMock()
    flow = HaVacationOptionsFlow(entry)
    flow.hass = hass
    flow.customize_date = mock_customize_date
    result = await flow.async_step_add_workday_date({"date": "invalid-format"})
    assert result["type"] == "form"
    assert "date" in result["errors"]

@pytest.mark.asyncio
async def test_optionflow_add_workday_date_form(hass, mock_customize_date):
    entry = MagicMock()
    flow = HaVacationOptionsFlow(entry)
    flow.hass = hass
    flow.customize_date = mock_customize_date
    result = await flow.async_step_add_workday_date()
    assert result["type"] == "form"
    assert result["step_id"] == "add_workday_date"

@pytest.mark.asyncio
async def test_optionflow_delete_workday_date_success(hass, mock_customize_date):
    entry = MagicMock()
    flow = HaVacationOptionsFlow(entry)
    flow.hass = hass
    flow.customize_date = mock_customize_date
    result = await flow.async_step_delete_workday_date({"date": "2025-01-02"})
    assert result["type"] == "abort"
    assert result["reason"] == "删除自定义工作日期成功"

@pytest.mark.asyncio
async def test_optionflow_delete_workday_date_invalid(hass, mock_customize_date):
    entry = MagicMock()
    flow = HaVacationOptionsFlow(entry)
    flow.hass = hass
    flow.customize_date = mock_customize_date
    result = await flow.async_step_delete_workday_date({"date": ""})
    assert result["type"] == "form"
    assert "date" in result["errors"]

@pytest.mark.asyncio
async def test_optionflow_delete_workday_date_form(hass, mock_customize_date):
    entry = MagicMock()
    flow = HaVacationOptionsFlow(entry)
    flow.hass = hass
    flow.customize_date = mock_customize_date
    result = await flow.async_step_delete_workday_date()
    assert result["type"] == "form"

@pytest.mark.asyncio
async def test_optionflow_init_menu_full(hass):
    entry = MagicMock()
    flow = HaVacationOptionsFlow(entry)
    flow.hass = hass

    hass.config = MagicMock()
    hass.config.path = MagicMock(return_value="/tmp/fake.yaml")

    with patch("custom_components.ha_vacation.config_flow.CustomizeDate", MagicMock()):
        result = await flow.async_step_init()
    assert result["type"] == "menu"
    assert "menu_options" in result
