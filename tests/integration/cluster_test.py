import pytest
from rubrik_cdm.exceptions import CDMVersion

import urllib3
urllib3.disable_warnings()


@pytest.mark.integration
def test_cluster_version_check(rubrik, monkeypatch):

    with pytest.raises(CDMVersion):
        rubrik.cluster_version_check("5.0")
