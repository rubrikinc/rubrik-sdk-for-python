import pytest
import rubrik_cdm


@pytest.fixture(scope='module')
def rubrik():

    return rubrik_cdm.Connect("10.0.1.1", "user", "password", enable_logging=True)
