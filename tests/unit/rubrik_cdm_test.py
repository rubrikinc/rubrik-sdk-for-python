import pytest


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
