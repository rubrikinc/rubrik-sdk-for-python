import pytest


def test_valid_url(rubrik_init):

    rubrik = rubrik_init

    test_header = {'Content-Type': 'application/json', 'Accept': 'application/json',
                   'Authorization': 'Basic cHl0aG9uc2RrQHJhbmdlcnMubGFiOkR1bW15UGFzc3dvcmQh'}

    assert rubrik._authorization_header() == test_header


def test_valid_url(rubrik_init):

    rubrik = rubrik_init

    assert rubrik._api_validation('v1', '/cluster/me') == None
    assert rubrik._api_validation('internal', '/cluster/me') == None


def test_invalid_api_version(rubrik_init):

    rubrik = rubrik_init

    with pytest.raises(SystemExit, match="Error: Enter a valid API version."):
        rubrik._api_validation('1', '/cluster/me')


def test_invalid_url_type(rubrik_init):

    rubrik = rubrik_init

    with pytest.raises(SystemExit, match="Error: The API Endpoint must be a string."):
        rubrik._api_validation('v1', 1)


def test_invalid_url_start(rubrik_init):

    rubrik = rubrik_init

    with pytest.raises(SystemExit, match="Error: The API Endpoint should begin with '/'"):
        rubrik._api_validation('v1', "cluster/me")


def test_invalid_url_end(rubrik_init):

    rubrik = rubrik_init

    with pytest.raises(SystemExit, match="Error: The API Endpoint should not end with '/'."):
        rubrik._api_validation('v1', "/cluster/me/")
