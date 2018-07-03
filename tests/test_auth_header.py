import pytest


def test_valid_url(rubrik_init):

    rubrik = rubrik_init

    test_header = {'Content-Type': 'application/json', 'Accept': 'application/json',
                   'Authorization': 'Basic cHl0aG9uc2RrQHJhbmdlcnMubGFiOkR1bW15UGFzc3dvcmQh'}

    assert rubrik._authorization_header() == test_header
