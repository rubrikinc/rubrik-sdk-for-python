import pytest
import logging
import rubrik_cdm


def test_unit_header(rubrik):
    header = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': "RubrikPythonSDK--{}--{}".format(rubrik.sdk_version, rubrik.python_version),
        'rk-integration': rubrik.function_name

    }

    assert rubrik._header() == header


def test_validate_release_version_matches_user_agent_version(rubrik):
    with open("setup.py") as fp:
        for line_number, line_content in enumerate(fp):
            if "version" in line_content:
                release_version = line_content.strip().replace('version="', "").replace('",', "")

    assert release_version == rubrik.sdk_version

def test_logging_output(mocker, caplog):

    def mock_get_v1_cluster_me_version():
        return {'version': '5.0.1-1280'}

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_cluster_me_version()

    # Manually import rubrik_cdm instead of using the fixture to get proper log
    # message count and to more easily set logging level
    rubrik = rubrik_cdm.Connect("10.0.1.1", "user", "password", enable_logging=True)

    rubrik.cluster_version()

    assert len(caplog.records) == 4

    log_entries = {
        0: "Node IP: 10.0.1.1",
        1: "Username: user",
        2: "Password: ******",
        3: "cluster_version: Getting the software version of the Rubrik cluster."
    }

    for index, log_message in log_entries.items():
        assert caplog.records[index].message == log_message
    
@pytest.mark.parametrize('logging_level', ["debug", "critical", "error", "warning", "info"])
def test_logging_level(mocker, caplog, logging_level):

    def mock_get_v1_cluster_me_version():
        return {'version': '5.0.1-1280'}

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_cluster_me_version()

    # Manually import rubrik_cdm instead of using the fixture to get proper log
    # message count and to more easily set logging level
    rubrik = rubrik_cdm.Connect("10.0.1.1", "user", "password", enable_logging=True, logging_level=logging_level)

    rubrik.cluster_version()
    
    # Validate the logging level
    set_logging = {
            "debug": logging.DEBUG,
            "critical": logging.CRITICAL,
            "error": logging.ERROR,
            "warning": logging.WARNING,
            "info": logging.INFO,
        }
        
    assert caplog.records[0].levelno == set_logging[logging_level]
