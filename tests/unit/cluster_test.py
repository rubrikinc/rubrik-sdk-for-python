import pytest
from rubrik_cdm.exceptions import InvalidParameterException
from rubrik_cdm import Connect


def test_cluster_version(rubrik, mocker):

    def patch_get_v1_cluster_me_version():
        return {'version': '5.0.1-1280'}

    get_patch = mocker.patch('rubrik_cdm.Connect.get', autospec=True)
    get_patch.return_value = patch_get_v1_cluster_me_version()

    assert rubrik.cluster_version() == "5.0.1-1280"


def test_minimum_installed_cdm_version_met(rubrik, mocker):

    def patch_cluster_version():
        return "5.0.1-1280"

    cluster_version_patch = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True)
    cluster_version_patch.return_value = patch_cluster_version()

    assert rubrik.minimum_installed_cdm_version("5.0") is True


def test_minimum_installed_cdm_version_not_met(rubrik, mocker):

    def patch_cluster_version():
        return "5.0.1-1280"

    cluster_version_patch = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True)
    cluster_version_patch.return_value = patch_cluster_version()

    assert rubrik.minimum_installed_cdm_version("5.2") is False


def test_cluster_node_ip(rubrik, mocker):

    def patch_internal_cluster_me_node():
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

    get_patch = mocker.patch('rubrik_cdm.Connect.get', autospec=True)
    get_patch.return_value = patch_internal_cluster_me_node()

    assert rubrik.cluster_node_ip() == ["192.168.1.1", "192.168.1.2", "192.168.1.3"]


def test_cluster_node_name(rubrik, mocker):

    def patch_internal_cluster_me_node():
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

    get_patch = mocker.patch('rubrik_cdm.Connect.get', autospec=True)
    get_patch.return_value = patch_internal_cluster_me_node()

    assert rubrik.cluster_node_name() == ["RVM000A000001", "RVM000A000002", "RVM000A000003"]


def test_end_user_authorization_invalid_object(rubrik):

    with pytest.raises(InvalidParameterException):
        rubrik.end_user_authorization("object_name", "end_user", "not_a_supported_object_type")


def test_end_user_authorization_invalid_end_user(rubrik, mocker):

    def patch_object_id():
        return "VirtualMachine:::e6a7e6f1-6050-1ee33-9ba6-8e284e2801de-vm-38297"

    def patch_internal_user_username():
        return []

    object_patch = mocker.patch('rubrik_cdm.Connect.object_id', autospec=True)
    object_patch.return_value = patch_object_id()

    get_patch = mocker.patch('rubrik_cdm.Connect.get', autospec=True)
    get_patch.return_value = patch_internal_user_username()

    with pytest.raises(InvalidParameterException):
        rubrik.end_user_authorization("object_name", "end_user", "vmware")


def test_end_user_authorization_idempotence(rubrik, mocker, monkeypatch):

    def patch_object_id(api_version, api_endpoint, timeout):
        return "VirtualMachine:::e6a7e6f1-6050-1ee33-9ba6-8e284e2801de-vm-38297"

    def patch_internal_user_username():
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

    def patch_internal_authorization_role_end_user_principals():
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

    monkeypatch.setattr(rubrik, "object_id", patch_object_id)

    get_patch = mocker.patch('rubrik_cdm.Connect.get', autospec=True)
    get_patch.side_effect = [patch_internal_user_username(), patch_internal_authorization_role_end_user_principals()]

    assert rubrik.end_user_authorization("object_name", "end_user", "vmware", 1) \
        == 'No change required. The End User "end_user" is already authorized to interact with the "object_name" VM.'


def test_end_user_authorization(rubrik, mocker, monkeypatch):

    def patch_object_id(api_version, api_endpoint, timeout):
        return "VirtualMachine:::e6a7e6f1-6050-1ee33-9ba6-8e284e2801de-vm-38297"

    def patch_internal_user_username():
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

    def patch_internal_authorization_role_end_user_principals():
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

    def patch_internal_authorization_role_end_user():
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

    monkeypatch.setattr(rubrik, "object_id", patch_object_id)

    get_patch = mocker.patch('rubrik_cdm.Connect.get', autospec=True)
    get_patch.side_effect = [patch_internal_user_username(), patch_internal_authorization_role_end_user_principals()]

    post_patch = mocker.patch('rubrik_cdm.Connect.post', autospec=True)
    post_patch.return_value = patch_internal_authorization_role_end_user()

    assert rubrik.end_user_authorization("object_name", "end_user", "vmware") \
        == patch_internal_authorization_role_end_user()


def test_add_vcenter_idempotence(rubrik, mocker):

    def patch_vmware_vcenter_primary_cluster_id():
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

    get_patch = mocker.patch('rubrik_cdm.Connect.get', autospec=True)
    get_patch.return_value = patch_vmware_vcenter_primary_cluster_id()

    assert rubrik.add_vcenter("vCenter-Hostname", "vcenter_username", "vcenter_password") == \
        "No change required. The vCenter 'vCenter-Hostname' has already been added to the Rubrik cluster."
