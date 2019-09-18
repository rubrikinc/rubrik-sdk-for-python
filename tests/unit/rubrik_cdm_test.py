import pytest


def test_unit_header(rubrik):
    header = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    assert rubrik._header() == header


def test_validate_release_version_matches_user_agent_version(rubrik):
    with open("setup.py") as fp:
        for line_number, line_content in enumerate(fp):
            if "version" in line_content:
                release_version = line_content.strip().replace('version="', "").replace('",', "")

    with open("./rubrik_cdm/rubrik_cdm.py") as fp:
        for line_number, line_content in enumerate(fp):
            if "User-Agent" in line_content:
                user_agent_version = line_content.strip().replace("'User-Agent': 'Rubrik Python SDK v", "").replace("'", "")

    assert release_version == user_agent_version


def test_validate_user_agent_version(rubrik):

    user_agents = []

    with open("./rubrik_cdm/rubrik_cdm.py") as fp:
        for line_number, line_content in enumerate(fp):
            if "User-Agent" in line_content:
                user_agents.append(
                    line_content.strip().replace(
                        "'User-Agent': 'Rubrik Python SDK v",
                        "").replace(
                        "'",
                        ""))

    assert user_agents[0] == user_agents[1]
