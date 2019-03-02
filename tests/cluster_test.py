import pytest
from rubrik_cdm.exceptions import CDMVersion

import urllib3
urllib3.disable_warnings()


@pytest.mark.unit
def test_unit_cluster_version_check(rubrik, monkeypatch):

    def patch_cluster_version():
        return "4.2.1-1417"

    # Monkey match rubrik.cluster_version to equal the patch_cluster_version() result
    monkeypatch.setattr(rubrik, "cluster_version", patch_cluster_version)

    with pytest.raises(CDMVersion):
        rubrik.cluster_version_check("5.0")


@pytest.mark.integration
def test_integration_cluster_version_check(rubrik, monkeypatch):

    with pytest.raises(CDMVersion):
        rubrik.cluster_version_check("5.0")
