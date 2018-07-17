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


@responses.activate
def test_bootstrap(rubrik_connect):

    rubrik = rubrik_connect

    # node_config must be populated
    with pytest.raises(SystemExit, match='Error: You must provide a valid dictionary for "node_config".'):
        resp = rubrik.bootstrap("test-cluster", "test-email", "admin-password", "10.255.100.1", "255.255.255.0",
                                enable_encryption=True, node_config=None, dns_search_domains=None, dns_nameservers=None, ntp_servers=None)
    # node_config must be a dict
    with pytest.raises(SystemExit, match='Error: You must provide a valid dictionary for "node_config".'):
        resp = rubrik.bootstrap("test-cluster", "test-email", "admin-password", "10.255.100.1", "255.255.255.0",
                                enable_encryption=True, node_config="Incorrect_Config_Type", dns_search_domains=None, dns_nameservers=None, ntp_servers=None)
    # dns_search_domains must be a dic
    with pytest.raises(SystemExit, match='Error: You must provide a valid list for "dns_search_domains".'):
        resp = rubrik.bootstrap("test-cluster", "test-email", "admin-password", "10.255.100.1", "255.255.255.0",
                                enable_encryption=True, node_config={}, dns_search_domains="Invalid_Search_Domain_Type", dns_nameservers=None, ntp_servers=None)
    # dns_nameservers must be a dic
    with pytest.raises(SystemExit, match='Error: You must provide a valid list for "dns_nameservers".'):
        resp = rubrik.bootstrap("test-cluster", "test-email", "admin-password", "10.255.100.1", "255.255.255.0",
                                enable_encryption=True, node_config={}, dns_search_domains=None, dns_nameservers="Invalid_Nameserver", ntp_servers=None)

    # ntp_servers must be a dic
    with pytest.raises(SystemExit, match='Error: You must provide a valid list for "ntp_servers".'):
        resp = rubrik.bootstrap("test-cluster", "test-email", "admin-password", "10.255.100.1", "255.255.255.0",
                                enable_encryption=True, node_config={}, dns_search_domains=None, dns_nameservers=None, ntp_servers="Invalid_NTP_Type")

    api_version = 'internal'
    api_endpoint = '/cluster/me/bootstrap'

    url = "https://{}/api/{}{}".format(rubrik.node_ip, api_version, api_endpoint)

    response_body = {
        "status": "string",
        "id": 0
    }

    cluster_name = "PythonSDK"
    admin_email = "test@rubrikpythonsdk.com"
    admin_password = "RubrikGoForward"
    management_gateway = '172.31.0.1'
    management_subnet_mask = '255.255.240.0'

    node_config = {
        '1': '172.98.9.245',
        '2': '172.98.15.64',
        '3': '172.98.0.117',
        '4': '172.98.10.112'
    }

    responses.add(responses.POST, url, json=response_body, status=200)
    responses.add(responses.POST, url, status=500)

    resp = bootstrap = rubrik.bootstrap(cluster_name, admin_email, admin_password, management_gateway,
                                        management_subnet_mask, enable_encryption=False, node_config=node_config)
    assert resp == response_body

    with pytest.raises(SystemExit, match="500 Server Error: Internal Server Error for url"):
        resp = bootstrap = rubrik.bootstrap(cluster_name, admin_email, admin_password, management_gateway,
                                            management_subnet_mask, enable_encryption=False, node_config=node_config)
