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


@responses.activate
def test_bootstrap_status(rubrik_connect):
    rubrik = rubrik_connect

    request_id = "1"

    api_version = 'internal'
    api_endpoint = '/cluster/me/bootstrap?request_id={}'.format(request_id)

    url = "https://{}/api/{}{}".format(rubrik.node_ip, api_version, api_endpoint)

    response_body = {
        "status": "string",
        "message": "string",
        "ipConfig": "string",
        "cassandraSetup": "string",
        "installSchema": "string",
        "startServices": "string",
        "ipmiConfig": "string",
        "configAdminUser": "string",
        "resetNodes": "string",
        "setupDisks": "string",
        "setupEncryptionAtRest": "string",
        "setupOsAndMetadataPartitions": "string",
        "createTopLevelFilesystemDirs": "string",
        "setupLoopDevices": "string"
    }

    responses.add(responses.GET, url, json=response_body, status=200)
    responses.add(responses.GET, url, status=500)

    resp = rubrik.bootstrap_status()
    assert resp == response_body

    with pytest.raises(SystemExit, match="500 Server Error: Internal Server Error for url"):
        resp = rubrik.bootstrap_status()
