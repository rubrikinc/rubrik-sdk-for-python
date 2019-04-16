import pytest
import rubrik_cdm


@pytest.fixture(scope='module')
def rubrik():

    return rubrik_cdm.Connect()
