import pytest
from rubrik_cdm.exceptions import CDMVersionException

import urllib3
urllib3.disable_warnings()


@pytest.mark.integration
def test_cluster_version_check(rubrik, monkeypatch):

    with pytest.raises(CDMVersionException):
        rubrik.cluster_version_check("5.0")
