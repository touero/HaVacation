import pytest
import yaml
from unittest.mock import MagicMock, patch
from custom_components.ha_vacation.customize_date import CustomizeDate
from custom_components.ha_vacation.constants import CustomizeDateSet

# Helper for context-managed mock open
from io import StringIO
def mock_open(read_data=""):
    file_obj = StringIO(read_data)
    file_obj.__enter__ = lambda s: s
    file_obj.__exit__ = lambda s, exc_type, exc_val, exc_tb: None
    return MagicMock(return_value=file_obj)

@pytest.fixture
def hass():
    hass = MagicMock()
    hass.config.path = MagicMock(return_value="/tmp/customize_date.yaml")
    return hass

@pytest.fixture
def customize_date(hass):
    with patch("os.makedirs"):
        return CustomizeDate(hass, "customize_date.yaml")

def test_load_local_data_file_not_exist(customize_date):
    with patch("os.path.exists", return_value=False):
        data = customize_date._load_local_data()
    assert CustomizeDateSet.VACATION.value in data and CustomizeDateSet.WORKDAY.value in data

def test_load_local_data_file_exist_and_valid(customize_date):
    mock_data = {
        CustomizeDateSet.VACATION.value: ["2024-01-01"],
        CustomizeDateSet.WORKDAY.value: ["2024-01-02"]
    }
    with patch("os.path.exists", return_value=True), \
         patch("builtins.open", mock_open(read_data=yaml.safe_dump(mock_data))):
        data = customize_date._load_local_data()
    assert data == mock_data

def test_load_local_data_file_exist_and_invalid_format(customize_date, caplog):
    with patch("os.path.exists", return_value=True), \
         patch("builtins.open", mock_open(read_data="[1]")), \
         patch("yaml.safe_load", return_value=[1]):
        data = customize_date._load_local_data()
    assert data == {CustomizeDateSet.VACATION.value: [], CustomizeDateSet.WORKDAY.value: []}

def test_load_local_data_yaml_error(customize_date):
    with patch("os.path.exists", return_value=True), \
         patch("builtins.open", mock_open(read_data=": invalid yaml")), \
         patch("yaml.safe_load", side_effect=yaml.YAMLError("bad yaml")):
        data = customize_date._load_local_data()
    assert CustomizeDateSet.VACATION.value in data and CustomizeDateSet.WORKDAY.value in data

@pytest.mark.asyncio
async def test_load_original_data(customize_date):
    with patch.object(customize_date, "_load_local_data", return_value={
        CustomizeDateSet.VACATION.value: [],
        CustomizeDateSet.WORKDAY.value: []
    }):
        data = await customize_date._load_original_data()
    assert data == {
        CustomizeDateSet.VACATION.value: [],
        CustomizeDateSet.WORKDAY.value: []
    }

@pytest.mark.asyncio
async def test_write_customize_date_to_yaml_success(customize_date):
    with patch("builtins.open", mock_open()) as mfile, \
         patch("yaml.safe_dump"):
        await customize_date.write_customize_date_to_yaml({
            CustomizeDateSet.VACATION.value: [],
            CustomizeDateSet.WORKDAY.value: []
        })
        mfile.assert_called_once()

@pytest.mark.asyncio
async def test_write_customize_date_to_yaml_oserror(customize_date):
    with patch("builtins.open", side_effect=OSError("fail")):
        await customize_date.write_customize_date_to_yaml({
            CustomizeDateSet.VACATION.value: [],
            CustomizeDateSet.WORKDAY.value: []
        })

@pytest.mark.asyncio
async def test_save_customize_date(customize_date):
    initial = {
        CustomizeDateSet.VACATION.value: [],
        CustomizeDateSet.WORKDAY.value: []
    }
    with patch.object(customize_date, "_load_original_data", return_value=initial.copy()), \
         patch.object(customize_date, "write_customize_date_to_yaml") as mock_write:
        await customize_date.save_customize_date(CustomizeDateSet.VACATION.value, "2024-01-01")
        # Should have added one date
        args, kwargs = mock_write.call_args
        assert "2024-01-01" in args[0][CustomizeDateSet.VACATION.value]

@pytest.mark.asyncio
async def test_read_customize_date_from_yaml(customize_date):
    data = {
        CustomizeDateSet.VACATION.value: ["2024-01-01"],
        CustomizeDateSet.WORKDAY.value: []
    }
    with patch.object(customize_date, "_load_original_data", return_value=data):
        result = await customize_date.read_customize_date_from_yaml(CustomizeDateSet.VACATION.value)
    assert result == ["2024-01-01"]

@pytest.mark.asyncio
async def test_delete_customize_date_from_yaml_success(customize_date):
    data = {
        CustomizeDateSet.VACATION.value: ["2024-01-01"],
        CustomizeDateSet.WORKDAY.value: []
    }
    with patch.object(customize_date, "_load_original_data", return_value=data.copy()), \
         patch("builtins.open", mock_open()) as mfile, \
         patch("yaml.safe_dump"):
        await customize_date.delete_customize_date_from_yaml(CustomizeDateSet.VACATION.value, "2024-01-01")
        mfile.assert_called_once()

@pytest.mark.asyncio
async def test_delete_customize_date_from_yaml_valueerror(customize_date):
    data = {
        CustomizeDateSet.VACATION.value: [],
        CustomizeDateSet.WORKDAY.value: []
    }
    with patch.object(customize_date, "_load_original_data", return_value=data.copy()), \
         patch("builtins.open", mock_open()):
        await customize_date.delete_customize_date_from_yaml(CustomizeDateSet.VACATION.value, "2024-01-01")
        # Should not raise

@pytest.mark.asyncio
async def test_delete_customize_date_from_yaml_oserror(customize_date):
    data = {
        CustomizeDateSet.VACATION.value: ["2024-01-01"],
        CustomizeDateSet.WORKDAY.value: []
    }
    with patch.object(customize_date, "_load_original_data", return_value=data.copy()), \
         patch("builtins.open", side_effect=OSError("fail")):
        await customize_date.delete_customize_date_from_yaml(CustomizeDateSet.VACATION.value, "2024-01-01")
        # Should not raise

def test_sync_load_customize_date(customize_date):
    data = {
        CustomizeDateSet.VACATION.value: ["2024-01-01"],
        CustomizeDateSet.WORKDAY.value: []
    }
    with patch.object(customize_date, "_load_local_data", return_value=data):
        result = customize_date.sync_load_customize_date(CustomizeDateSet.VACATION.value)
    assert result == ["2024-01-01"]
