import pytest
import responses


@responses.activate
def test_get_call(rubrik_connect):
    rubrik = rubrik_connect

    api_version = 'v1'
    api_endpoint = '/cluster/me'

    url = "https://{}/api/{}{}".format(rubrik.node_ip, api_version, api_endpoint)

    response_body = {'id': '89fc0e90-6f1c-8393-efas-90c7qee0e6299', 'version': '4.1.1', 'apiVersion': '1', 'name': 'RubrikAPICluster',
                     'timezone': {'timezone': 'America/Los_Angeles'}, 'acceptedEulaVersion': '1.0', 'latestEulaVersion': '1.0'}

    responses.add(responses.GET, url, json=response_body, status=200)
    responses.add(responses.GET, url, json=response_body, status=500)

    resp = rubrik.get(api_version, api_endpoint)
    assert resp == response_body

    with pytest.raises(SystemExit, match="500 Server Error: Internal Server Error for url"):
        resp = rubrik.get(api_version, api_endpoint)


@responses.activate
def test_post_call(rubrik_connect):
    rubrik = rubrik_connect

    api_version = 'v1'
    api_endpoint = '/host'

    url = "https://{}/api/{}{}".format(rubrik.node_ip, api_version, api_endpoint)

    config = {
        "hostname": "string",
        "hasAgent": True
    }

    response_body = {
        "id": "string",
        "hostname": "string",
        "primaryClusterId": "string",
        "operatingSystem": "string",
        "operatingSystemType": "string",
        "status": "string",
        "agentId": "string",
        "compressionEnabled": True
    }

    responses.add(responses.POST, url, json=response_body, status=200)
    responses.add(responses.POST, url, status=500)

    resp = rubrik.post(api_version, api_endpoint, config)
    assert resp == response_body

    with pytest.raises(SystemExit, match="500 Server Error: Internal Server Error for url"):
        resp = rubrik.post(api_version, api_endpoint, config)


@responses.activate
def test_patch_call(rubrik_connect):
    rubrik = rubrik_connect

    api_version = 'v1'
    api_endpoint = '/cluster/me'

    url = "https://{}/api/{}{}".format(rubrik.node_ip, api_version, api_endpoint)

    config = {
        "name": "string",
        "timezone": {
            "timezone": "America/Anchorage"
        },
        "geolocation": {
            "address": "string"
        },
        "acceptedEulaVersion": "string"
    }

    response_body = {
        "id": "string",
        "version": "string",
        "apiVersion": "string",
        "name": "string",
        "timezone": {
            "timezone": "America/Anchorage"
        },
        "geolocation": {
            "address": "string"
        },
        "acceptedEulaVersion": "string",
        "latestEulaVersion": "string"
    }

    responses.add(responses.PATCH, url, json=response_body, status=200)
    responses.add(responses.PATCH, url, status=500)

    resp = rubrik.patch(api_version, api_endpoint, config)
    assert resp == response_body

    with pytest.raises(SystemExit, match="500 Server Error: Internal Server Error for url"):
        resp = rubrik.patch(api_version, api_endpoint, config)


@responses.activate
def test_delete_call(rubrik_connect):
    rubrik = rubrik_connect

    api_version = 'v1'
    api_endpoint = '/sla_domain/1a98504e-ppd1-411d-e235-814dc045ab87'

    url = "https://{}/api/{}{}".format(rubrik.node_ip, api_version, api_endpoint)

    response_body = {
        "response": "none"
    }

    responses.add(responses.DELETE, url, json=response_body, status=204)
    responses.add(responses.DELETE, url, status=500)

    resp = rubrik.delete(api_version, api_endpoint)
    assert resp == response_body

    with pytest.raises(SystemExit, match="500 Server Error: Internal Server Error for url"):
        resp = rubrik.delete(api_version, api_endpoint)


@responses.activate
def test_job_status(rubrik_connect):
    rubrik = rubrik_connect

    url = "https://172.21.8.90/api/v1/vmware/vm/request/CREATE_VMWARE_SNAPSHOT_1f51-9520-1231-a68c-6fe1448-vm-5008_ecd2-4765-49fa-81f2-19ba417:::0"

    response_body = {
        "response": "none"
    }

    responses.add(responses.GET, url, json=response_body, status=204)
    responses.add(responses.GET, url, status=500)

    resp = rubrik.job_status(url)
    assert resp == response_body

    with pytest.raises(SystemExit, match="500 Server Error: Internal Server Error for url"):
        resp = rubrik.job_status(url)
