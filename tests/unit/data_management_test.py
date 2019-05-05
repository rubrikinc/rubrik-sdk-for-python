import pytest
from rubrik_cdm.exceptions import InvalidParameterException, CDMVersionException
from rubrik_cdm import Connect


def test_on_demand_snapshot_invalid_object_type(rubrik):
    with pytest.raises(InvalidParameterException) as error:
        rubrik.on_demand_snapshot("object_name", "not_a_valid_object_type")

    error_message = error.value.args[0]

    assert error_message == "The on_demand_snapshot() object_type argument must be one of the following: ['vmware', 'physical_host', 'ahv', 'mssql_db']."


def test_on_demand_snapshot_invalid_host_os_type(rubrik):
    with pytest.raises(InvalidParameterException) as error:
        rubrik.on_demand_snapshot("object_name", "physical_host", host_os="not_a_valid_host_os")

    error_message = error.value.args[0]

    assert error_message == "The on_demand_snapshot() host_os argument must be one of the following: ['Linux', 'Windows']."
