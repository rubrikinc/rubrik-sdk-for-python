import pytest


@pytest.mark.unit
def test_cluster_version_check(rubrik, monkeypatch):

    # Result of self.get('v1', '/cluster/me/version', timeout=timeout)
    def patch_get_v1_cluster_me_version(api_version, api_endpoint, timeout):
        return {'version': '5.0.1-1280'}

    # Monkey match rubrik.cluster_version to equal the patch_cluster_version() result
    monkeypatch.setattr(rubrik, "get", patch_get_v1_cluster_me_version)

    assert rubrik.cluster_version() == "5.0.1-1280"
