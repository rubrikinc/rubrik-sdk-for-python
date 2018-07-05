import pytest
import responses


@responses.activate
def test_cluster_version(rubrik_connect):
    rubrik = rubrik_connect

    api_version = 'v1'
    api_endpoint = '/cluster/me/version'

    url = "https://{}/api/{}{}".format(rubrik.node_ip, api_version, api_endpoint)

    response_body = {'version': '4.1.1-p2-2263'}

    responses.add(responses.GET, url, json=response_body, status=200)
    responses.add(responses.GET, url, status=500)

    resp = rubrik.cluster_version()
    assert resp == response_body

    with pytest.raises(SystemExit, match="500 Server Error: Internal Server Error for url"):
        resp = rubrik.cluster_version()
