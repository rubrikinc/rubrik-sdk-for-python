import pytest


@pytest.mark.unit
def test_cluster_version(rubrik, monkeypatch):

    # Result of self.get('v1', '/cluster/me/version', timeout=timeout)
    def patch_get_v1_cluster_me_version(api_version, api_endpoint, timeout):
        return {'version': '5.0.1-1280'}

    # Monkey match rubrik.cluster_version to equal the patch_cluster_version() result
    monkeypatch.setattr(rubrik, "get", patch_get_v1_cluster_me_version)

    assert rubrik.cluster_version() == "5.0.1-1280"


@pytest.mark.unit
def test_minimum_installed_cdm_version_met(rubrik, monkeypatch):

    def patch_cluster_version(timeout):
        return "5.0.1-1280"

    # Test to validate the version of CDM meets the minimum requirements
    monkeypatch.setattr(rubrik, "cluster_version", patch_cluster_version)
    assert rubrik.minimum_installed_cdm_version("5.0") is True


@pytest.mark.unit
def test_minimum_installed_cdm_version_not_met(rubrik, monkeypatch):

    def patch_cluster_version(timeout):
        return "5.0.1-1280"

    # Test to validate the version of CDM does not meet the minimum requirements
    monkeypatch.setattr(rubrik, "cluster_version", patch_cluster_version)
    assert rubrik.minimum_installed_cdm_version("5.2") is False
    
@pytest.mark.unit
def test_cluster_node_ip(rubrik, monkeypatch):

    def patch_internal_cluster_me_node(api_version, api_endpoint, timeout):
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "brikId": "string",
                    "status": "string",
                    "ipAddress": "192.168.1.1",
                    "supportTunnel": {
                        "isTunnelEnabled": True,
                        "port": 0,
                        "enabledTime": "2019-04-16T14:16:15.573Z",
                        "lastActivityTime": "2019-04-16T14:16:15.573Z",
                        "inactivityTimeoutInSeconds": 0
                    }
                },
                {
                    "id": "string",
                    "brikId": "string",
                    "status": "string",
                    "ipAddress": "192.168.1.2",
                    "supportTunnel": {
                        "isTunnelEnabled": True,
                        "port": 0,
                        "enabledTime": "2019-04-16T14:16:15.573Z",
                        "lastActivityTime": "2019-04-16T14:16:15.573Z",
                        "inactivityTimeoutInSeconds": 0
                    }
                },
                {
                    "id": "string",
                    "brikId": "string",
                    "status": "string",
                    "ipAddress": "192.168.1.3",
                    "supportTunnel": {
                        "isTunnelEnabled": True,
                        "port": 0,
                        "enabledTime": "2019-04-16T14:16:15.573Z",
                        "lastActivityTime": "2019-04-16T14:16:15.573Z",
                        "inactivityTimeoutInSeconds": 0
                    }
                }

            ],
            "total": 0
        }

    # Test to validate the version of CDM does not meet the minimum requirements
    monkeypatch.setattr(rubrik, "get", patch_internal_cluster_me_node)
    assert rubrik.cluster_node_ip() == ["192.168.1.1", "192.168.1.2", "192.168.1.3"]

@pytest.mark.unit
def test_cluster_node_name(rubrik, monkeypatch):

    def patch_internal_cluster_me_node(api_version, api_endpoint, timeout):
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "RVM000A000001",
                    "brikId": "string",
                    "status": "string",
                    "ipAddress": "string",
                    "supportTunnel": {
                        "isTunnelEnabled": True,
                        "port": 0,
                        "enabledTime": "2019-04-16T14:16:15.573Z",
                        "lastActivityTime": "2019-04-16T14:16:15.573Z",
                        "inactivityTimeoutInSeconds": 0
                    }
                },
                {
                    "id": "RVM000A000002",
                    "brikId": "string",
                    "status": "string",
                    "ipAddress": "string",
                    "supportTunnel": {
                        "isTunnelEnabled": True,
                        "port": 0,
                        "enabledTime": "2019-04-16T14:16:15.573Z",
                        "lastActivityTime": "2019-04-16T14:16:15.573Z",
                        "inactivityTimeoutInSeconds": 0
                    }
                },
                {
                    "id": "RVM000A000003",
                    "brikId": "string",
                    "status": "string",
                    "ipAddress": "string",
                    "supportTunnel": {
                        "isTunnelEnabled": True,
                        "port": 0,
                        "enabledTime": "2019-04-16T14:16:15.573Z",
                        "lastActivityTime": "2019-04-16T14:16:15.573Z",
                        "inactivityTimeoutInSeconds": 0
                    }
                }

            ],
            "total": 0
        }

    # Test to validate the version of CDM does not meet the minimum requirements
    monkeypatch.setattr(rubrik, "get", patch_internal_cluster_me_node)
    assert rubrik.cluster_node_name() == ["RVM000A000001", "RVM000A000002", "RVM000A000003"]

