import pytest
import rubrik


@pytest.fixture(scope='module')
def rubrik_init():
    node_ip = "172.21.8.90"
    username = "pythonsdk@rangers.lab"
    password = "DummyPassword!"

    return rubrik.api(node_ip, username, password)
