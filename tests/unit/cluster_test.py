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
