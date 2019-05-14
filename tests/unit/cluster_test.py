import pytest
from rubrik_cdm.exceptions import InvalidParameterException, CDMVersionException, InvalidTypeException
from rubrik_cdm import Connect


def test_cluster_version(rubrik, mocker):

    def mock_get_v1_cluster_me_version():
        return {'version': '5.0.1-1280'}

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_cluster_me_version()

    assert rubrik.cluster_version() == "5.0.1-1280"


def test_minimum_installed_cdm_version_met(rubrik, mocker):

    def mock_self_cluster_version():
        return "5.0.1-1280"

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = mock_self_cluster_version()

    assert rubrik.minimum_installed_cdm_version("5.0") is True


def test_minimum_installed_cdm_version_not_met(rubrik, mocker):

    def mock_self_cluster_version():
        return "5.0.1-1280"

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = mock_self_cluster_version()

    assert rubrik.minimum_installed_cdm_version("5.2") is False


def test_cluster_node_ip(rubrik, mocker):

    def mock_internal_cluster_me_node():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "brikId": "string",
                    "status": "string",
                    "ipAddress": "192.168.1.1",
                    "supportTunnel": {
                        "isTunnelEnabled": True,
                        "port": 0,
                        "enabledTime": "2019-04-16T14:16:15.573Z",
                        "lastActivityTime": "2019-04-16T14:16:15.573Z",
                        "inactivityTimeoutInSeconds": 0
                    }
                },
                {
                    "id": "string",
                    "brikId": "string",
                    "status": "string",
                    "ipAddress": "192.168.1.2",
                    "supportTunnel": {
                        "isTunnelEnabled": True,
                        "port": 0,
                        "enabledTime": "2019-04-16T14:16:15.573Z",
                        "lastActivityTime": "2019-04-16T14:16:15.573Z",
                        "inactivityTimeoutInSeconds": 0
                    }
                },
                {
                    "id": "string",
                    "brikId": "string",
                    "status": "string",
                    "ipAddress": "192.168.1.3",
                    "supportTunnel": {
                        "isTunnelEnabled": True,
                        "port": 0,
                        "enabledTime": "2019-04-16T14:16:15.573Z",
                        "lastActivityTime": "2019-04-16T14:16:15.573Z",
                        "inactivityTimeoutInSeconds": 0
                    }
                }

            ],
            "total": 0
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_internal_cluster_me_node()

    assert rubrik.cluster_node_ip() == ["192.168.1.1", "192.168.1.2", "192.168.1.3"]


def test_cluster_node_name(rubrik, mocker):

    def mock_internal_cluster_me_node():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "RVM000A000001",
                    "brikId": "string",
                    "status": "string",
                    "ipAddress": "string",
                    "supportTunnel": {
                        "isTunnelEnabled": True,
                        "port": 0,
                        "enabledTime": "2019-04-16T14:16:15.573Z",
                        "lastActivityTime": "2019-04-16T14:16:15.573Z",
                        "inactivityTimeoutInSeconds": 0
                    }
                },
                {
                    "id": "RVM000A000002",
                    "brikId": "string",
                    "status": "string",
                    "ipAddress": "string",
                    "supportTunnel": {
                        "isTunnelEnabled": True,
                        "port": 0,
                        "enabledTime": "2019-04-16T14:16:15.573Z",
                        "lastActivityTime": "2019-04-16T14:16:15.573Z",
                        "inactivityTimeoutInSeconds": 0
                    }
                },
                {
                    "id": "RVM000A000003",
                    "brikId": "string",
                    "status": "string",
                    "ipAddress": "string",
                    "supportTunnel": {
                        "isTunnelEnabled": True,
                        "port": 0,
                        "enabledTime": "2019-04-16T14:16:15.573Z",
                        "lastActivityTime": "2019-04-16T14:16:15.573Z",
                        "inactivityTimeoutInSeconds": 0
                    }
                }

            ],
            "total": 0
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_internal_cluster_me_node()

    assert rubrik.cluster_node_name() == ["RVM000A000001", "RVM000A000002", "RVM000A000003"]


def test_end_user_authorization_invalid_object(rubrik):

    with pytest.raises(InvalidParameterException):
        rubrik.end_user_authorization("object_name", "end_user", "not_a_supported_object_type")


def test_end_user_authorization_invalid_end_user(rubrik, mocker):

    def mock_self_object_id():
        return "VirtualMachine:::e6a7e6f1-6050-1ee33-9ba6-8e284e2801de-vm-38297"

    def mock_internal_user_username():
        return []

    mock_object_id = mocker.patch('rubrik_cdm.Connect.object_id', autospec=True, spec_set=True)
    mock_object_id.return_value = mock_self_object_id

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_internal_user_username()

    with pytest.raises(InvalidParameterException):
        rubrik.end_user_authorization("object_name", "end_user", "vmware")


def test_end_user_authorization_idempotence(rubrik, mocker):

    def mock_self_object_id():
        return "VirtualMachine:::e6a7e6f1-6050-1ee33-9ba6-8e284e2801de-vm-38297"

    def mock_internal_user_username():
        return [
            {
                "id": "User:::119283ae-22ea-13f3-bfe2-9387cdf1d4a",
                "authDomainId": "string",
                "username": "string",
                "firstName": "string",
                "lastName": "string",
                "emailAddress": "string",
                "contactNumber": "string",
                "mfaServerId": "string"
            }
        ]

    def mock_internal_authorization_role_end_user_principals():
        return {
            "hasMore": True,
            "data": [
                {
                    "principal": "string",
                    "privileges": {
                        "destructiveRestore": [
                            "string"
                        ],
                        "restore": [
                            "VirtualMachine:::e6a7e6f1-6050-1ee33-9ba6-8e284e2801de-vm-38297"
                        ],
                        "onDemandSnapshot": [
                            "string"
                        ],
                        "restoreWithoutDownload": [
                            "string"
                        ],
                        "viewEvent": [
                            "string"
                        ],
                        "provisionOnInfra": [
                            "string"
                        ],
                        "viewReport": [
                            "string"
                        ]
                    },
                    "organizationId": "string"
                }
            ],
            "total": 0
        }

    mock_object_id = mocker.patch('rubrik_cdm.Connect.object_id', autospec=True, spec_set=True)
    mock_object_id.return_value = mock_self_object_id()

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_internal_user_username(), mock_internal_authorization_role_end_user_principals()]

    assert rubrik.end_user_authorization("object_name", "end_user", "vmware", 1) \
        == 'No change required. The End User "end_user" is already authorized to interact with the "object_name" VM.'


def test_end_user_authorization(rubrik, mocker):

    def mock_self_object_id():
        return "VirtualMachine:::e6a7e6f1-6050-1ee33-9ba6-8e284e2801de-vm-38297"

    def mock_internal_user_username():
        return [
            {
                "id": "User:::119283ae-22ea-13f3-bfe2-9387cdf1d4a",
                "authDomainId": "string",
                "username": "string",
                "firstName": "string",
                "lastName": "string",
                "emailAddress": "string",
                "contactNumber": "string",
                "mfaServerId": "string"
            }
        ]

    def mock_internal_authorization_role_end_user_principals():
        return {
            "hasMore": True,
            "data": [
                {
                    "principal": "string",
                    "privileges": {
                        "destructiveRestore": [
                            "string"
                        ],
                        "restore": [
                            "VirtualMachine:::e6a7e6r3-6050-1ee33-9ba6-8e284e2801de"
                        ],
                        "onDemandSnapshot": [
                            "string"
                        ],
                        "restoreWithoutDownload": [
                            "string"
                        ],
                        "viewEvent": [
                            "string"
                        ],
                        "provisionOnInfra": [
                            "string"
                        ],
                        "viewReport": [
                            "string"
                        ]
                    },
                    "organizationId": "string"
                }
            ],
            "total": 0
        }

    def mock_internal_authorization_role_end_user():
        return {
            "hasMore": False,
            "data": [
                {
                    "principal": "User:::119283ae-22ea-13f3-bfe2-9387cdf1d4a",
                    "privileges": {
                        "destructiveRestore": [],
                        "restore": [
                            "VirtualMachine:::e6a7e6f1-6050-1ee33-9ba6-8e284e2801de-vm-38297-not-present"
                        ],
                        "onDemandSnapshot": [],
                        "restoreWithoutDownload": [],
                        "viewEvent": [],
                        "provisionOnInfra": [],
                        "viewReport": []
                    },
                    "organizationId": "Organization:::05e3ee0b-5ec1-e33b-88a5-d916855aff5f"
                }
            ],
            "total": 1
        }

    mock_object_id = mocker.patch('rubrik_cdm.Connect.object_id', autospec=True, spec_set=True)
    mock_object_id.return_value = mock_self_object_id()

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_internal_user_username(), mock_internal_authorization_role_end_user_principals()]

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_internal_authorization_role_end_user()

    assert rubrik.end_user_authorization("object_name", "end_user", "vmware") \
        == mock_internal_authorization_role_end_user()


def test_add_vcenter_idempotence(rubrik, mocker):

    def mock_v1_vmware_vcenter_primary_cluster_id():
        return {
            "hasMore": True,
            "data": [
                {
                    "caCerts": "string",
                    "configuredSlaDomainId": "string",
                    "id": "string",
                    "name": "string",
                    "configuredSlaDomainName": "string",
                    "primaryClusterId": "string",
                    "hostname": "vCenter-Hostname",
                    "username": "string",
                    "conflictResolutionAuthz": "AllowAutoConflictResolution",
                    "configuredSlaDomainPolarisManagedId": "string"
                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_v1_vmware_vcenter_primary_cluster_id()

    assert rubrik.add_vcenter("vCenter-Hostname", "vcenter_username", "vcenter_password") == \
        "No change required. The vCenter 'vCenter-Hostname' has already been added to the Rubrik cluster."


def test_add_vcenter(rubrik, mocker):

    def mock_v1_vmware_vcenter_primary_cluster_id():
        return {
            "hasMore": True,
            "data": [
                {
                    "caCerts": "string",
                    "configuredSlaDomainId": "string",
                    "id": "string",
                    "name": "string",
                    "configuredSlaDomainName": "string",
                    "primaryClusterId": "string",
                    "hostname": "string",
                    "username": "string",
                    "conflictResolutionAuthz": "AllowAutoConflictResolution",
                    "configuredSlaDomainPolarisManagedId": "string"
                }
            ],
            "total": 1
        }

    def mock_v1_vmware_vcenter():
        return {
            "id": "string",
            "status": "string",
            "progress": 0,
            "startTime": "2019-04-17T02:46:12.097Z",
            "endTime": "2019-04-17T02:46:12.097Z",
            "nodeId": "string",
            "error": {
                "message": "string"
            },
            "links": [
                {
                    "href": "www.example.com",
                    "rel": "string"
                }
            ]
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_v1_vmware_vcenter_primary_cluster_id()

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_v1_vmware_vcenter()

    assert rubrik.add_vcenter("vCenter-Hostname", "vcenter_username", "vcenter_password") == \
        (mock_v1_vmware_vcenter(), "www.example.com")


def test_configure_timezone_invalid_timezone(rubrik):

    with pytest.raises(InvalidParameterException):
        rubrik.configure_timezone("not_a_supported_timezone")


def test_configure_timezone_idempotence(rubrik, mocker):

    def mock_get_v1_cluster_me():
        return {
            "id": "string",
            "version": "string",
            "apiVersion": "string",
            "name": "string",
            "timezone": {
                "timezone": "America/Chicago"
            },
            "geolocation": {
                "address": "string"
            },
            "acceptedEulaVersion": "string",
            "latestEulaVersion": "string"
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_cluster_me()

    assert rubrik.configure_timezone("America/Chicago") \
        == "No change required. The Rubrik cluster is already configured with 'America/Chicago' as it's timezone."


def test_configure_timezone(rubrik, mocker):

    def mock_get_v1_cluster_me():
        return {
            "id": "string",
            "version": "string",
            "apiVersion": "string",
            "name": "string",
            "timezone": {
                "timezone": "America/Denver"
            },
            "geolocation": {
                "address": "string"
            },
            "acceptedEulaVersion": "string",
            "latestEulaVersion": "string"
        }

    def mock_patch_v1_cluster_me():
        return {
            "id": "string",
            "version": "string",
            "apiVersion": "string",
            "name": "string",
            "timezone": {
                "timezone": "America/Denver"
            },
            "geolocation": {
                "address": "string"
            },
            "acceptedEulaVersion": "string",
            "latestEulaVersion": "string"
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_cluster_me()

    mock_patch = mocker.patch('rubrik_cdm.Connect.patch', autospec=True, spec_set=True)
    mock_patch.return_value = mock_patch_v1_cluster_me()

    assert rubrik.configure_timezone("America/Chicago") == mock_patch_v1_cluster_me()


def test_configure_ntp_invalid_type(rubrik):

    with pytest.raises(InvalidTypeException):
        rubrik.configure_ntp("not_a_list")


def test_configure_syslog_invalid_protocol(rubrik):

    with pytest.raises(InvalidParameterException):
        rubrik.configure_syslog("syslog_ip", "not_a_valid_protocol")


def test_configure_syslog_invalid_idempotence(rubrik, mocker):

    def mock_get_internal_syslog():
        return {
            "hasMore": True,
            "data": [
                {
                    "hostname": "syslog_ip",
                    "port": 514,
                    "protocol": "TCP",
                    "id": "string"
                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_syslog()

    assert rubrik.configure_syslog("syslog_ip", "TCP") == \
        "No change required. The Rubrik cluster is already configured to use the syslog server 'syslog_ip' on port '514' using the 'TCP' protocol."


def test_configure_syslog(rubrik, mocker):

    def mock_get_internal_syslog():
        return {
            "hasMore": True,
            "data": [
                {
                    "hostname": "syslog_ip",
                    "port": 514,
                    "protocol": "TCP",
                    "id": "string"
                }
            ],
            "total": 1
        }

    def mock_delete_internal_syslog_id():
        return {'status_code': '204'}

    def mock_post_internal_syslog():
        return {
            "hostname": "syslog_ip_new",
            "port": 514,
            "protocol": "TCP",
            "id": "string"
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_syslog()

    mock_delete = mocker.patch('rubrik_cdm.Connect.delete', autospec=True, spec_set=True)
    mock_delete.return_value = mock_delete_internal_syslog_id()

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_internal_syslog()

    assert rubrik.configure_syslog("syslog_ip_new", "TCP") == mock_post_internal_syslog()


def test_configure_vlan_invalid_ip(rubrik):

    with pytest.raises(InvalidParameterException):
        rubrik.configure_vlan("vlan", "netmask", "not_valid_a_list_or_dict")


def test_configure_vlan_invalid_number_of_vlans(rubrik, mocker):

    def mock_internal_cluster_me_node():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "RVM000A000001",
                    "brikId": "string",
                    "status": "string",
                    "ipAddress": "string",
                    "supportTunnel": {
                        "isTunnelEnabled": True,
                        "port": 0,
                        "enabledTime": "2019-04-16T14:16:15.573Z",
                        "lastActivityTime": "2019-04-16T14:16:15.573Z",
                        "inactivityTimeoutInSeconds": 0
                    }
                },
                {
                    "id": "RVM000A000002",
                    "brikId": "string",
                    "status": "string",
                    "ipAddress": "string",
                    "supportTunnel": {
                        "isTunnelEnabled": True,
                        "port": 0,
                        "enabledTime": "2019-04-16T14:16:15.573Z",
                        "lastActivityTime": "2019-04-16T14:16:15.573Z",
                        "inactivityTimeoutInSeconds": 0
                    }
                },
                {
                    "id": "RVM000A000003",
                    "brikId": "string",
                    "status": "string",
                    "ipAddress": "string",
                    "supportTunnel": {
                        "isTunnelEnabled": True,
                        "port": 0,
                        "enabledTime": "2019-04-16T14:16:15.573Z",
                        "lastActivityTime": "2019-04-16T14:16:15.573Z",
                        "inactivityTimeoutInSeconds": 0
                    }
                }

            ],
            "total": 0
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_internal_cluster_me_node()

    with pytest.raises(InvalidParameterException):
        rubrik.configure_vlan("vlan", "netmask", ["IP_1", "IP_2"])


def test_configure_vlan(rubrik, mocker):

    def mock_internal_cluster_me_node():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "RVM000A000001",
                    "brikId": "string",
                    "status": "string",
                    "ipAddress": "string",
                    "supportTunnel": {
                        "isTunnelEnabled": True,
                        "port": 0,
                        "enabledTime": "2019-04-16T14:16:15.573Z",
                        "lastActivityTime": "2019-04-16T14:16:15.573Z",
                        "inactivityTimeoutInSeconds": 0
                    }
                },
                {
                    "id": "RVM000A000002",
                    "brikId": "string",
                    "status": "string",
                    "ipAddress": "string",
                    "supportTunnel": {
                        "isTunnelEnabled": True,
                        "port": 0,
                        "enabledTime": "2019-04-16T14:16:15.573Z",
                        "lastActivityTime": "2019-04-16T14:16:15.573Z",
                        "inactivityTimeoutInSeconds": 0
                    }
                },
                {
                    "id": "RVM000A000003",
                    "brikId": "string",
                    "status": "string",
                    "ipAddress": "string",
                    "supportTunnel": {
                        "isTunnelEnabled": True,
                        "port": 0,
                        "enabledTime": "2019-04-16T14:16:15.573Z",
                        "lastActivityTime": "2019-04-16T14:16:15.573Z",
                        "inactivityTimeoutInSeconds": 0
                    }
                }

            ],
            "total": 0
        }

    def mock_internal_cluster_me_vlan():
        return {
            "hasMore": True,
            "data": [
                {
                    "vlan": 0,
                    "netmask": "string",
                    "interfaces": [
                        {
                            "node": "string",
                            "ip": "string"
                        }
                    ]
                }
            ],
            "total": 0
        }

    def mock_post_internal_cluster_me_vlan():
        return {'status_code': '204'}

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_internal_cluster_me_node(), mock_internal_cluster_me_vlan()]

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_internal_cluster_me_vlan()

    assert rubrik.configure_vlan("100", "netmask", ["IP_1", "IP_2", "IP_3"]) == mock_post_internal_cluster_me_vlan()


def test_configure_dns_servers_invalid_server_ip(rubrik):

    with pytest.raises(InvalidTypeException):
        rubrik.configure_dns_servers("not_a_valid_server_ip_type")


def test_configure_dns_servers_idempotence(rubrik, mocker):

    def mock_get_internal_cluster_me_dns_nameserver():
        return [
            "server_1"
        ]

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_cluster_me_dns_nameserver()

    assert rubrik.configure_dns_servers(["server_1"]) == \
        "No change required. The Rubrik cluster is already configured with the provided DNS servers."


def test_configure_dns_servers(rubrik, mocker):

    def mock_get_internal_cluster_me_dns_nameserver():
        return [
            "server_1",
            "server_2"
        ]

    def mock_post_internal_cluster_me_dns_nameserver():
        return {'status_code': '204'}

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_cluster_me_dns_nameserver()

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_internal_cluster_me_dns_nameserver()

    assert rubrik.configure_dns_servers(["server_1"]) == mock_post_internal_cluster_me_dns_nameserver()


def test_configure_search_domain_invalid_search_domain(rubrik):

    with pytest.raises(InvalidTypeException):
        rubrik.configure_search_domain("not_a_valid_search_domain_type")


def test_configure_search_domain_idempotence(rubrik, mocker):

    def mock_get_internal_cluster_me_dns_search_domain():
        return [
            "domain.1",
        ]

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_cluster_me_dns_search_domain()

    assert rubrik.configure_search_domain(["domain.1"]) == \
        "No change required. The Rubrik cluster is already configured with the provided DNS Search Domains."


def test_configure_search_domain(rubrik, mocker):

    def mock_get_internal_cluster_me_dns_search_domain():
        return [
            "server_1",
        ]

    def mock_post_internal_cluster_me_dns_search_domain():
        return {'status_code': '204'}

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_cluster_me_dns_search_domain()

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_internal_cluster_me_dns_search_domain()

    assert rubrik.configure_search_domain(["domain.1"]) == mock_post_internal_cluster_me_dns_search_domain()


def test_configure_smtp_settings_invalid_encryption(rubrik):

    with pytest.raises(InvalidParameterException):
        rubrik.configure_smtp_settings("hostname", "port", "from_email", "smtp_username",
                                       "smtp_password", "not_a_valid_encryption_value")


def test_configure_smtp_settings_idempotence(rubrik, mocker):

    def mock_get_internal_smtp_instance():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "smtpHostname": "hostname",
                    "smtpPort": 0,
                    "smtpSecurity": "NONE",
                    "smtpUsername": "smtp_username",
                    "fromEmailId": "from_email"
                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_smtp_instance()

    assert rubrik.configure_smtp_settings("hostname", "0", "from_email", "smtp_username", "smtp_password", "NONE") == \
        "No change required. The Rubrik cluster is already configured with the provided SMTP settings."


def test_configure_smtp_settings_new(rubrik, mocker):

    def mock_get_internal_smtp_instance():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "smtpHostname": "string",
                    "smtpPort": 0,
                    "smtpSecurity": "string",
                    "smtpUsername": "string",
                    "fromEmailId": "string"
                }
            ],
            "total": 0
        }

    def mock_post_internal_smtp_instance():
        return {
            "id": "string",
            "smtpHostname": "string",
            "smtpPort": 0,
            "smtpSecurity": "string",
            "smtpUsername": "string",
            "fromEmailId": "string"
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_smtp_instance()

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_internal_smtp_instance()

    assert rubrik.configure_smtp_settings("hostname", "0", "from_email", "smtp_username", "smtp_password", "NONE") == \
        mock_post_internal_smtp_instance()


def test_configure_smtp_settings_update(rubrik, mocker):

    def mock_get_internal_smtp_instance():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "smtpHostname": "string",
                    "smtpPort": 0,
                    "smtpSecurity": "string",
                    "smtpUsername": "string",
                    "fromEmailId": "string"
                }
            ],
            "total": 1
        }

    def mock_patch_internal_smtp_instance_id():
        return {
            "id": "string",
            "smtpHostname": "string",
            "smtpPort": 0,
            "smtpSecurity": "string",
            "smtpUsername": "string",
            "fromEmailId": "string"
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_smtp_instance()

    mock_patch = mocker.patch('rubrik_cdm.Connect.patch', autospec=True, spec_set=True)
    mock_patch.return_value = mock_patch_internal_smtp_instance_id()

    assert rubrik.configure_smtp_settings("hostname", "0", "from_email", "smtp_username", "smtp_password", "NONE") == \
        mock_patch_internal_smtp_instance_id()


def test_refresh_vcenter_no_wait(rubrik, mocker):

    def mock_object_id():
        return "vCenter:::eeeb7c90-a074-1233-e6e6-90386f8c3d70"

    def mock_post_v1_vmware_vcenter_id_refresh():
        return {
            "id": "string",
            "status": "string",
            "progress": 0,
            "startTime": "2019-04-17T21:22:14.214Z",
            "endTime": "2019-04-17T21:22:14.214Z",
            "nodeId": "string",
            "error": {
                "message": "string"
            },
            "links": [
                {
                    "href": "build.rubrik.com",
                    "rel": "string"
                }
            ]
        }

    mock_get_object_id = mocker.patch('rubrik_cdm.Connect.object_id', autospec=True, spec_set=True)
    mock_get_object_id.return_value = mock_object_id()

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_v1_vmware_vcenter_id_refresh()

    assert rubrik.refresh_vcenter("vcenter_ip", False) == mock_post_v1_vmware_vcenter_id_refresh()


def test_refresh_vcenter_wait_for_completion(rubrik, mocker):

    def mock_object_id():
        return "vCenter:::eeeb7c90-a074-1233-e6e6-90386f8c3d70"

    def mock_job_status():
        return {
            "id": "REFRESH_METADATA_eeeeb7c81-a074-4525-b5b5-81796f8c3d70_0d3e10b0-6741-4c1a-e208-c661325c1efd:::0",
            "status": "SUCCEEDED",
            "startTime": "2019-04-17T21:31:17.785Z",
            "endTime": "2019-04-17T21:31:39.056Z",
            "nodeId": "cluster:::RVM189S019012",
            "links": [
                {
                    "href": "REFRESH_METADATA_eeeeb7c81-a074-4525-b5b5-81796f8c3d70_0d3e10b0-6741-4c1a-e208-c661325c1efd:::0",
                    "rel": "self"
                }
            ]
        }

    mock_get_object_id = mocker.patch('rubrik_cdm.Connect.object_id', autospec=True, spec_set=True)
    mock_get_object_id.return_value = mock_object_id()

    mock_common_api = mocker.patch('rubrik_cdm.Connect._common_api', autospec=True, spec_set=True)
    mock_common_api.return_value = mock_job_status()

    assert rubrik.refresh_vcenter("vcenter_ip", True) == mock_job_status()


def test_create_user_idempotence(rubrik, mocker):

    def mock_get_internal_user():
        return [
            {
                "id": "string",
                "authDomainId": "string",
                "username": "string",
                "firstName": "string",
                "lastName": "string",
                "emailAddress": "string",
                "contactNumber": "string",
                "mfaServerId": "string"
            }
        ]

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_user()

    assert rubrik.create_user("username", "password") == \
        "No change required. The user 'username' already exists on the Rubrik cluster."


def test_create_user(rubrik, mocker):

    def mock_get_internal_user():
        return []

    def mock_post_internal_user():
        return {
            "id": "string",
            "authDomainId": "string",
            "username": "username",
            "firstName": "string",
            "lastName": "string",
            "emailAddress": "string",
            "contactNumber": "string",
            "createdById": "string",
            "createTime": "string",
            "mfaServerId": "string"
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_user()

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_internal_user()

    assert rubrik.create_user("username", "password") == mock_post_internal_user()


def test_read_only_authorization_minimum_installed_cdm_version(rubrik, mocker):

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = "4.1.2"

    with pytest.raises(CDMVersionException):
        rubrik.read_only_authorization("username")


def test_read_only_authorization_invalid_user(rubrik, mocker):

    def mock_get_internal_user():
        return []

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = "5.0.1"

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_user()

    with pytest.raises(InvalidParameterException):
        rubrik.read_only_authorization("username")


def test_read_only_authorization_idempotence(rubrik, mocker):

    def mock_get_internal_user():
        return [
            {
                "id": "string",
                "authDomainId": "string",
                "username": "string",
                "firstName": "string",
                "lastName": "string",
                "emailAddress": "string",
                "contactNumber": "string",
                "mfaServerId": "string"
            }
        ]

    def mock_get_internal_authorization_role_read_only_admin_principals():
        return {
            "hasMore": True,
            "data": [
                {
                    "principal": "string",
                    "privileges": {
                        "basic": [
                            "Global:::All"
                        ]
                    },
                    "organizationId": "string"
                }
            ],
            "total": 0
        }

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = "5.0.1"

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_internal_user(),
                            mock_get_internal_authorization_role_read_only_admin_principals()]

    assert rubrik.read_only_authorization("username") == \
        "No change required. The user 'username' already has read-only permissions."


def test_read_only_authorization(rubrik, mocker):

    def mock_get_internal_user():
        return [
            {
                "id": "string",
                "authDomainId": "string",
                "username": "string",
                "firstName": "string",
                "lastName": "string",
                "emailAddress": "string",
                "contactNumber": "string",
                "mfaServerId": "string"
            }
        ]

    def mock_get_internal_authorization_role_read_only_admin_principals():
        return {
            "hasMore": True,
            "data": [
                {
                    "principal": "string",
                    "privileges": {
                        "basic": [
                            "string"
                        ]
                    },
                    "organizationId": "string"
                }
            ],
            "total": 0
        }

    def mock_post_internal_authorization_role_read_only_admin():
        return {
            "hasMore": True,
            "data": [
                {
                    "principal": "string",
                    "privileges": {
                        "basic": [
                            "string"
                        ]
                    },
                    "organizationId": "string"
                }
            ],
            "total": 1
        }

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = "5.0.1"

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_internal_user(),
                            mock_get_internal_authorization_role_read_only_admin_principals()]

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_internal_authorization_role_read_only_admin()

    assert rubrik.read_only_authorization("username") == mock_post_internal_authorization_role_read_only_admin()
