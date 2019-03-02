import pytest
from rubrik_cdm.exceptions import CDMVersion


@pytest.mark.unit
def test_cluster_version_check(rubrik, monkeypatch):

    def patch_cluster_version(timeout):
        return "4.2.1-1417"

    # Monkey match rubrik.cluster_version to equal the patch_cluster_version() result
    monkeypatch.setattr(rubrik, "cluster_version", patch_cluster_version)

    with pytest.raises(CDMVersion):
        rubrik.cluster_version_check("5.0")
