import pytest
from rubrik_cdm.exceptions import InvalidParameterException, CDMVersionException, InvalidTypeException
from rubrik_cdm import Connect


def test_add_physical_host_empty_hostname_list(rubrik):

    with pytest.raises(InvalidParameterException) as error:
        rubrik.add_physical_host([])

    error_message = error.value.args[0]

    assert error_message == "The provided hostname list is empty."


def test_add_physical_host_idempotence(rubrik, mocker):

    def mock_get_v1_host():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "string",
                    "hostname": "hostname",
                    "primaryClusterId": "string",
                    "operatingSystem": "string",
                    "operatingSystemType": "string",
                    "status": "string",
                    "nasBaseConfig": {
                        "vendorType": "string",
                        "apiUsername": "string",
                        "apiCertificate": "string",
                        "apiHostname": "string",
                        "apiEndpoint": "string",
                        "zoneName": "string"
                    },
                    "mssqlCbtEnabled": "Enabled",
                    "mssqlCbtEffectiveStatus": "On",
                    "organizationId": "string",
                    "organizationName": "string"
                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_host()

    assert rubrik.add_physical_host("hostname") == \
        "No change required. The host 'hostname' is already connected to the Rubrik cluster."


def test_add_physical_host_list_idempotence(rubrik, mocker):

    def mock_get_v1_host():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "string",
                    "hostname": "hostname1",
                    "primaryClusterId": "string",
                    "operatingSystem": "string",
                    "operatingSystemType": "string",
                    "status": "string",
                    "nasBaseConfig": {
                        "vendorType": "string",
                        "apiUsername": "string",
                        "apiCertificate": "string",
                        "apiHostname": "string",
                        "apiEndpoint": "string",
                        "zoneName": "string"
                    },
                    "mssqlCbtEnabled": "Enabled",
                    "mssqlCbtEffectiveStatus": "On",
                    "organizationId": "string",
                    "organizationName": "string"
                },
                {
                    "id": "string",
                    "name": "string",
                    "hostname": "hostname2",
                    "primaryClusterId": "string",
                    "operatingSystem": "string",
                    "operatingSystemType": "string",
                    "status": "string",
                    "nasBaseConfig": {
                        "vendorType": "string",
                        "apiUsername": "string",
                        "apiCertificate": "string",
                        "apiHostname": "string",
                        "apiEndpoint": "string",
                        "zoneName": "string"
                    },
                    "mssqlCbtEnabled": "Enabled",
                    "mssqlCbtEffectiveStatus": "On",
                    "organizationId": "string",
                    "organizationName": "string"
                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_host()

    assert rubrik.add_physical_host(["hostname1", "hostname2"]) == \
        "No Change Required. All Hosts Already added or supplied list was empty"


def test_add_physical_host(rubrik, mocker):

    def mock_get_v1_host():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "string",
                    "hostname": "string",
                    "primaryClusterId": "string",
                    "operatingSystem": "string",
                    "operatingSystemType": "string",
                    "status": "string",
                    "nasBaseConfig": {
                        "vendorType": "string",
                        "apiUsername": "string",
                        "apiCertificate": "string",
                        "apiHostname": "string",
                        "apiEndpoint": "string",
                        "zoneName": "string"
                    },
                    "mssqlCbtEnabled": "Enabled",
                    "mssqlCbtEffectiveStatus": "On",
                    "organizationId": "string",
                    "organizationName": "string"
                }
            ],
            "total": 1
        }

    def mock_post_v1_host():
        return {
            "id": "string",
            "name": "string",
            "hostname": "string",
            "primaryClusterId": "string",
            "operatingSystem": "string",
            "operatingSystemType": "string",
            "status": "string",
            "nasBaseConfig": {
                "vendorType": "string",
                "apiUsername": "string",
                "apiCertificate": "string",
                "apiHostname": "string",
                "apiEndpoint": "string",
                "zoneName": "string"
            },
            "mssqlCbtEnabled": "Enabled",
            "mssqlCbtEffectiveStatus": "On",
            "organizationId": "string",
            "organizationName": "string",
            "agentId": "string",
            "compressionEnabled": True,
            "isRelic": True,
            "mssqlCbtDriverInstalled": True,
            "hostVfdEnabled": "Enabled",
            "hostVfdDriverState": "NotInstalled",
            "oracleSysDbaUser": "string"
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_host()

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_v1_host()

    assert rubrik.add_physical_host("hostname") == mock_post_v1_host()


def test_add_physical_host_list(rubrik, mocker):

    def mock_get_v1_host():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "string",
                    "hostname": "string",
                    "primaryClusterId": "string",
                    "operatingSystem": "string",
                    "operatingSystemType": "string",
                    "status": "string",
                    "nasBaseConfig": {
                        "vendorType": "string",
                        "apiUsername": "string",
                        "apiCertificate": "string",
                        "apiHostname": "string",
                        "apiEndpoint": "string",
                        "zoneName": "string"
                    },
                    "mssqlCbtEnabled": "Enabled",
                    "mssqlCbtEffectiveStatus": "On",
                    "organizationId": "string",
                    "organizationName": "string"
                },
                {
                    "id": "string",
                    "name": "string",
                    "hostname": "string",
                    "primaryClusterId": "string",
                    "operatingSystem": "string",
                    "operatingSystemType": "string",
                    "status": "string",
                    "nasBaseConfig": {
                        "vendorType": "string",
                        "apiUsername": "string",
                        "apiCertificate": "string",
                        "apiHostname": "string",
                        "apiEndpoint": "string",
                        "zoneName": "string"
                    },
                    "mssqlCbtEnabled": "Enabled",
                    "mssqlCbtEffectiveStatus": "On",
                    "organizationId": "string",
                    "organizationName": "string"
                }
            ],
            "total": 2
        }

    def mock_post_v1_host():
        return {
            "id": "string",
            "name": "string",
            "hostname": "string",
            "primaryClusterId": "string",
            "operatingSystem": "string",
            "operatingSystemType": "string",
            "status": "string",
            "nasBaseConfig": {
                "vendorType": "string",
                "apiUsername": "string",
                "apiCertificate": "string",
                "apiHostname": "string",
                "apiEndpoint": "string",
                "zoneName": "string"
            },
            "mssqlCbtEnabled": "Enabled",
            "mssqlCbtEffectiveStatus": "On",
            "organizationId": "string",
            "organizationName": "string",
            "agentId": "string",
            "compressionEnabled": True,
            "isRelic": True,
            "mssqlCbtDriverInstalled": True,
            "hostVfdEnabled": "Enabled",
            "hostVfdDriverState": "NotInstalled",
            "oracleSysDbaUser": "string"
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_host()

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_v1_host()

    assert rubrik.add_physical_host("hostname") == mock_post_v1_host()


def test_delete_physical_host_idempotence(rubrik, mocker):

    def mock_get_v1_host():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "string",
                    "hostname": "string",
                    "primaryClusterId": "string",
                    "operatingSystem": "string",
                    "operatingSystemType": "string",
                    "status": "string",
                    "nasBaseConfig": {
                        "vendorType": "string",
                        "apiUsername": "string",
                        "apiCertificate": "string",
                        "apiHostname": "string",
                        "apiEndpoint": "string",
                        "zoneName": "string"
                    },
                    "mssqlCbtEnabled": "Enabled",
                    "mssqlCbtEffectiveStatus": "On",
                    "organizationId": "string",
                    "organizationName": "string"
                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_host()

    assert rubrik.delete_physical_host("hostname") == \
        "No change required. The host 'hostname' is not connected to the Rubrik cluster."


def test_delete_physical_host(rubrik, mocker):

    def mock_get_v1_host():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "string",
                    "hostname": "hostname",
                    "primaryClusterId": "string",
                    "operatingSystem": "string",
                    "operatingSystemType": "string",
                    "status": "string",
                    "nasBaseConfig": {
                        "vendorType": "string",
                        "apiUsername": "string",
                        "apiCertificate": "string",
                        "apiHostname": "string",
                        "apiEndpoint": "string",
                        "zoneName": "string"
                    },
                    "mssqlCbtEnabled": "Enabled",
                    "mssqlCbtEffectiveStatus": "On",
                    "organizationId": "string",
                    "organizationName": "string"
                },
                {
                    "id": "string",
                    "name": "string",
                    "hostname": "string",
                    "primaryClusterId": "string",
                    "operatingSystem": "string",
                    "operatingSystemType": "string",
                    "status": "string",
                    "nasBaseConfig": {
                        "vendorType": "string",
                        "apiUsername": "string",
                        "apiCertificate": "string",
                        "apiHostname": "string",
                        "apiEndpoint": "string",
                        "zoneName": "string"
                    },
                    "mssqlCbtEnabled": "Enabled",
                    "mssqlCbtEffectiveStatus": "On",
                    "organizationId": "string",
                    "organizationName": "string"
                }
            ],
            "total": 2
        }

    def mock_delete_v1_host_id():
        return {"status_code: 204"}

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_host()

    mock_delete = mocker.patch('rubrik_cdm.Connect.delete', autospec=True, spec_set=True)
    mock_delete.return_value = mock_delete_v1_host_id()

    assert rubrik.delete_physical_host("hostname") == mock_delete_v1_host_id()


def test_create_physical_fileset_invalid_operating_system(rubrik):

    with pytest.raises(InvalidParameterException) as error:
        rubrik.create_physical_fileset("name", "not_a_valid_operating_system",
                                       "include", "exclude", "exclude_exception")

    error_message = error.value.args[0]

    assert error_message == "The create_physical_fileset() operating_system argument must be one of the following: ['Linux', 'Windows']."


def test_create_physical_fileset_invalid_follow_network_shares(rubrik):

    with pytest.raises(InvalidTypeException) as error:
        rubrik.create_physical_fileset("name", "Linux",
                                       "include", "exclude", "exclude_exception", follow_network_shares="not_a_valid_follow_network_shares")

    error_message = error.value.args[0]

    assert error_message == "The 'follow_network_shares' argument must be True or False."


def test_create_physical_fileset_invalid_backup_hidden_folders(rubrik):

    with pytest.raises(InvalidTypeException) as error:
        rubrik.create_physical_fileset("name", "Linux",
                                       "include", "exclude", "exclude_exception", backup_hidden_folders="not_a_valid_backup_hidden_folders")

    error_message = error.value.args[0]

    assert error_message == "The 'backup_hidden_folders' argument must be True or False."


def test_create_physical_fileset_invalid_include(rubrik):

    with pytest.raises(InvalidTypeException) as error:
        rubrik.create_physical_fileset("name", "Linux", "not_a_valid_include", "exclude", "exclude_exception")

    error_message = error.value.args[0]

    assert error_message == "The 'include' argument must be a list object."


def test_create_physical_fileset_invalid_exclude(rubrik):

    with pytest.raises(InvalidTypeException) as error:
        rubrik.create_physical_fileset("name", "Linux", [""], "not_a_valid_exclude", "exclude_exception")

    error_message = error.value.args[0]

    assert error_message == "The 'exclude' argument must be a list object."


def test_create_physical_fileset_invalid_exclude_exception(rubrik):

    with pytest.raises(InvalidTypeException) as error:
        rubrik.create_physical_fileset("name", "Linux", [""], [""], "not_a_valid_exclude_exception")

    error_message = error.value.args[0]

    assert error_message == "The 'exclude_exception' argument must be a list object."


def test_create_physical_fileset_idempotence(rubrik, mocker):

    def mock_get_v1_fileset_template():
        return {
            "hasMore": True,
            "data": [
                {
                    "allowBackupNetworkMounts": True,
                    "allowBackupHiddenFoldersInNetworkMounts": True,
                    "useWindowsVss": True,
                    "name": "name",
                    "includes": [
                        "includes"
                    ],
                    "excludes": [
                        "excludes"
                    ],
                    "exceptions": [
                        "exceptions"
                    ],
                    "operatingSystemType": "Linux",
                    "shareType": "NFS",
                    "preBackupScript": "string",
                    "postBackupScript": "string",
                    "backupScriptTimeout": 0,
                    "backupScriptErrorHandling": "string",
                    "isArrayEnabled": True,
                    "id": "string",
                    "primaryClusterId": "string",
                    "isArchived": True,
                    "hostCount": 0,
                    "shareCount": 0
                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_fileset_template()

    assert rubrik.create_physical_fileset("name", "Linux", ["includes"], ["excludes"], ["exceptions"], True, True) == \
        "No change required. The Rubrik cluster already has a Linux Fileset named 'name' configured with the provided variables."


def test_create_physical_fileset(rubrik, mocker):

    def mock_get_v1_fileset_template():
        return {
            "hasMore": True,
            "data": [],
            "total": 1
        }

    def mock_post_v1_fileset_template_bulk():
        return {
            "allowBackupNetworkMounts": True,
            "allowBackupHiddenFoldersInNetworkMounts": True,
            "useWindowsVss": True,
            "name": "string",
            "includes": [
                "string"
            ],
            "excludes": [
                "string"
            ],
            "exceptions": [
                "string"
            ],
            "operatingSystemType": "UnixLike",
            "shareType": "NFS",
            "preBackupScript": "string",
            "postBackupScript": "string",
            "backupScriptTimeout": 0,
            "backupScriptErrorHandling": "string",
            "isArrayEnabled": True,
            "id": "string",
            "primaryClusterId": "string",
            "isArchived": True,
            "hostCount": 0,
            "shareCount": 0
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_fileset_template()

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_v1_fileset_template_bulk()

    assert rubrik.create_physical_fileset("name", "Linux", ["includes"], ["excludes"], ["exceptions"], True, True) == \
        mock_post_v1_fileset_template_bulk()


def test_create_nas_fileset_invalid_share_type(rubrik):

    with pytest.raises(InvalidParameterException) as error:
        rubrik.create_nas_fileset("name", "not_a_valid_share_type", "include", "exclude", "exclude_exception")

    error_message = error.value.args[0]

    assert error_message == "The create_fileset() share_type argument must be one of the following: ['NFS', 'SMB']."


def test_create_nas_fileset_invalid_follow_network_shares(rubrik):

    with pytest.raises(InvalidTypeException) as error:
        rubrik.create_nas_fileset(
            "name",
            "NFS",
            "include",
            "exclude",
            "exclude_exception",
            "not_a_valid_follow_network_share")

    error_message = error.value.args[0]

    assert error_message == "The 'follow_network_shares' argument must be True or False."


def test_create_nas_fileset_invalid_include(rubrik):

    with pytest.raises(InvalidTypeException) as error:
        rubrik.create_nas_fileset(
            "name", "NFS", "not_a_valid_include", "exclude", "exclude_exception")

    error_message = error.value.args[0]

    assert error_message == "The 'include' argument must be a list object."


def test_create_nas_fileset_invalid_exclude(rubrik):

    with pytest.raises(InvalidTypeException) as error:
        rubrik.create_nas_fileset(
            "name", "NFS", [""], "not_a_valid_exclude", "exclude_exception")

    error_message = error.value.args[0]

    assert error_message == "The 'exclude' argument must be a list object."


def test_create_nas_fileset_invalid_exclude_exception(rubrik):

    with pytest.raises(InvalidTypeException) as error:
        rubrik.create_nas_fileset(
            "name", "NFS", [""], [""], "not_a_valid_exclude_exception")

    error_message = error.value.args[0]

    assert error_message == "The 'exclude_exception' argument must be a list object."


def test_create_nas_fileset_idempotence(rubrik, mocker):

    def mock_get_v1_fileset_template():
        return {
            "hasMore": True,
            "data": [
                {
                    "allowBackupNetworkMounts": True,
                    "allowBackupHiddenFoldersInNetworkMounts": True,
                    "useWindowsVss": True,
                    "name": "name",
                    "includes": [
                        "includes"
                    ],
                    "excludes": [
                        "excludes"
                    ],
                    "exceptions": [
                        "exceptions"
                    ],
                    "operatingSystemType": "Linux",
                    "shareType": "NFS",
                    "preBackupScript": "string",
                    "postBackupScript": "string",
                    "backupScriptTimeout": 0,
                    "backupScriptErrorHandling": "string",
                    "isArrayEnabled": True,
                    "id": "string",
                    "primaryClusterId": "string",
                    "isArchived": True,
                    "hostCount": 0,
                    "shareCount": 0
                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_fileset_template()

    assert rubrik.create_nas_fileset("name", "NFS", ["includes"], ["excludes"], ["exceptions"], True) == \
        "No change required. The Rubrik cluster already has a NAS Fileset named 'name' configured with the provided variables."


@pytest.mark.parametrize('share', ["NFS", "SMB"])
def test_create_nas_fileset(rubrik, mocker, share):

    def mock_get_v1_fileset_template():
        return {
            "hasMore": True,
            "data": [],
            "total": 1
        }

    def mock_post_v1_fileset_template_bulk():
        return {
            "allowBackupNetworkMounts": True,
            "allowBackupHiddenFoldersInNetworkMounts": True,
            "useWindowsVss": True,
            "name": "string",
            "includes": [
                "string"
            ],
            "excludes": [
                "string"
            ],
            "exceptions": [
                "string"
            ],
            "operatingSystemType": "UnixLike",
            "shareType": "NFS",
            "preBackupScript": "string",
            "postBackupScript": "string",
            "backupScriptTimeout": 0,
            "backupScriptErrorHandling": "string",
            "isArrayEnabled": True,
            "id": "string",
            "primaryClusterId": "string",
            "isArchived": True,
            "hostCount": 0,
            "shareCount": 0
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_fileset_template()

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_v1_fileset_template_bulk()

    assert rubrik.create_nas_fileset("name", share, ["includes"], ["excludes"], ["exceptions"], True) == \
        mock_post_v1_fileset_template_bulk()


def test_assign_physical_host_fileset_invalid_operating_system(rubrik):

    with pytest.raises(InvalidParameterException) as error:
        rubrik.assign_physical_host_fileset("hostname", "fileset_name", "not_a_valid_operting_system", "sla_name")

    error_message = error.value.args[0]

    assert error_message == "The assign_physical_host_fileset() operating_system argument must be one of the following: ['Linux', 'Windows']."


def test_assign_physical_host_fileset_invalid_follow_network_shares(rubrik):

    with pytest.raises(InvalidTypeException) as error:
        rubrik.assign_physical_host_fileset(
            "hostname",
            "fileset_name",
            "Linux",
            "sla_name",
            follow_network_shares="not_a_valid_follow_network_shares")

    error_message = error.value.args[0]

    assert error_message == "The 'follow_network_shares' argument must be True or False."


def test_assign_physical_host_fileset_invalid_backup_hidden_folders(rubrik):

    with pytest.raises(InvalidTypeException) as error:
        rubrik.assign_physical_host_fileset(
            "hostname",
            "fileset_name",
            "Linux",
            "sla_name",
            backup_hidden_folders="not_a_valid_backup_hidden_folders")

    error_message = error.value.args[0]

    assert error_message == "The 'backup_hidden_folders' argument must be True or False."


def test_assign_physical_host_fileset_invalid_include(rubrik):

    with pytest.raises(InvalidTypeException) as error:
        rubrik.assign_physical_host_fileset(
            "hostname",
            "fileset_name",
            "Linux",
            "sla_name",
            include="not_a_valid_include")

    error_message = error.value.args[0]

    assert error_message == "The 'include' argument must be a list object."


def test_assign_physical_host_fileset_invalid_exclude(rubrik):

    with pytest.raises(InvalidTypeException) as error:
        rubrik.assign_physical_host_fileset(
            "hostname",
            "fileset_name",
            "Linux",
            "sla_name",
            exclude="not_a_valid_exclude")

    error_message = error.value.args[0]

    assert error_message == "The 'exclude' argument must be a list object."


def test_assign_physical_host_fileset_invalid_exclude_exception(rubrik):

    with pytest.raises(InvalidTypeException) as error:
        rubrik.assign_physical_host_fileset(
            "hostname",
            "fileset_name",
            "Linux",
            "sla_name",
            exclude_exception="not_a_valid_exclude_exception")

    error_message = error.value.args[0]

    assert error_message == "The 'exclude_exception' argument must be a list object."


def test_assign_physical_host_fileset_invalid_hostname(rubrik, mocker):

    def mock_get_v1_host():
        return {
            "hasMore": True,
            "data": [],
            "total": 0
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_host()

    with pytest.raises(InvalidParameterException) as error:
        rubrik.assign_physical_host_fileset("hostname", "fileset_name", "Linux", "sla_name")

    error_message = error.value.args[0]

    assert error_message == "The Rubrik cluster is not connected to a Linux physical host named 'hostname'."


def test_assign_physical_host_fileset_invalid_hostname_no_match(rubrik, mocker):

    def mock_get_v1_host():
        return {
            "hasMore": True,
            "data": [],
            "total": 0
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_host()

    with pytest.raises(InvalidParameterException) as error:
        rubrik.assign_physical_host_fileset("hostname", "fileset_name", "Linux", "sla_name")

    error_message = error.value.args[0]

    assert error_message == "The Rubrik cluster is not connected to a Linux physical host named 'hostname'."


def test_assign_physical_host_fileset_invalid_hostname_close_match(rubrik, mocker):

    def mock_get_v1_host():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "string",
                    "hostname": "string",
                    "primaryClusterId": "string",
                    "operatingSystem": "string",
                    "operatingSystemType": "string",
                    "status": "string",
                    "nasBaseConfig": {
                        "vendorType": "string",
                        "apiUsername": "string",
                        "apiCertificate": "string",
                        "apiHostname": "string",
                        "apiEndpoint": "string",
                        "zoneName": "string"
                    },
                    "mssqlCbtEnabled": "Enabled",
                    "mssqlCbtEffectiveStatus": "On",
                    "organizationId": "string",
                    "organizationName": "string"
                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_host()

    with pytest.raises(InvalidParameterException) as error:
        rubrik.assign_physical_host_fileset("hostname", "fileset_name", "Linux", "sla_name")

    error_message = error.value.args[0]

    assert error_message == "The Rubrik cluster is not connected to a Linux physical host named 'hostname'."


def test_assign_physical_host_fileset_invalid_fileset_name(rubrik, mocker):

    def mock_get_v1_host():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "string",
                    "hostname": "hostname",
                    "primaryClusterId": "string",
                    "operatingSystem": "string",
                    "operatingSystemType": "string",
                    "status": "string",
                    "nasBaseConfig": {
                        "vendorType": "string",
                        "apiUsername": "string",
                        "apiCertificate": "string",
                        "apiHostname": "string",
                        "apiEndpoint": "string",
                        "zoneName": "string"
                    },
                    "mssqlCbtEnabled": "Enabled",
                    "mssqlCbtEffectiveStatus": "On",
                    "organizationId": "string",
                    "organizationName": "string"
                }
            ],
            "total": 1
        }

    def mock_get_v1_fileset_template():
        return {
            "hasMore": True,
            "data": [],
            "total": 0
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_v1_host(), mock_get_v1_fileset_template()]

    with pytest.raises(InvalidParameterException) as error:
        rubrik.assign_physical_host_fileset("hostname", "fileset_name", "Linux", "sla_name")

    error_message = error.value.args[0]

    assert error_message == "The Rubrik cluster does not have a Linux Fileset named 'fileset_name'."


def test_assign_physical_host_fileset_invalid_fileset_name_multiple_matches_not_specific(rubrik, mocker):

    def mock_get_v1_host():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "string",
                    "hostname": "hostname",
                    "primaryClusterId": "string",
                    "operatingSystem": "string",
                    "operatingSystemType": "string",
                    "status": "string",
                    "nasBaseConfig": {
                        "vendorType": "string",
                        "apiUsername": "string",
                        "apiCertificate": "string",
                        "apiHostname": "string",
                        "apiEndpoint": "string",
                        "zoneName": "string"
                    },
                    "mssqlCbtEnabled": "Enabled",
                    "mssqlCbtEffectiveStatus": "On",
                    "organizationId": "string",
                    "organizationName": "string"
                }
            ],
            "total": 2
        }

    def mock_get_v1_fileset_template():
        return {
            "hasMore": True,
            "data": [
                {
                    "allowBackupNetworkMounts": True,
                    "allowBackupHiddenFoldersInNetworkMounts": True,
                    "useWindowsVss": True,
                    "name": "fileset_name",
                    "includes": [
                        "string"
                    ],
                    "excludes": [
                        "string"
                    ],
                    "exceptions": [
                        "string"
                    ],
                    "operatingSystemType": "UnixLike",
                    "shareType": "NFS",
                    "preBackupScript": "string",
                    "postBackupScript": "string",
                    "backupScriptTimeout": 0,
                    "backupScriptErrorHandling": "string",
                    "isArrayEnabled": True,
                    "id": "string",
                    "primaryClusterId": "string",
                    "isArchived": True,
                    "hostCount": 0,
                    "shareCount": 0
                },
                {
                    "allowBackupNetworkMounts": True,
                    "allowBackupHiddenFoldersInNetworkMounts": True,
                    "useWindowsVss": True,
                    "name": "fileset_name",
                    "includes": [
                        "string"
                    ],
                    "excludes": [
                        "string"
                    ],
                    "exceptions": [
                        "string"
                    ],
                    "operatingSystemType": "UnixLike",
                    "shareType": "NFS",
                    "preBackupScript": "string",
                    "postBackupScript": "string",
                    "backupScriptTimeout": 0,
                    "backupScriptErrorHandling": "string",
                    "isArrayEnabled": True,
                    "id": "string",
                    "primaryClusterId": "string",
                    "isArchived": True,
                    "hostCount": 0,
                    "shareCount": 0
                }
            ],
            "total": 2
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_v1_host(), mock_get_v1_fileset_template()]

    with pytest.raises(InvalidParameterException) as error:
        rubrik.assign_physical_host_fileset("hostname", "fileset_name", "Linux", "sla_name")

    error_message = error.value.args[0]

    assert error_message == "The Rubrik cluster contains multiple Linux Filesets named 'fileset_name'. Please populate all function arguments to find a more specific match."


def test_assign_physical_host_fileset_invalid_fileset_name_multiple_matches_specific(rubrik, mocker):

    def mock_get_v1_host():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "string",
                    "hostname": "hostname",
                    "primaryClusterId": "string",
                    "operatingSystem": "string",
                    "operatingSystemType": "string",
                    "status": "string",
                    "nasBaseConfig": {
                        "vendorType": "string",
                        "apiUsername": "string",
                        "apiCertificate": "string",
                        "apiHostname": "string",
                        "apiEndpoint": "string",
                        "zoneName": "string"
                    },
                    "mssqlCbtEnabled": "Enabled",
                    "mssqlCbtEffectiveStatus": "On",
                    "organizationId": "string",
                    "organizationName": "string"
                }
            ],
            "total": 2
        }

    def mock_get_v1_fileset_template():
        return {
            "hasMore": True,
            "data": [
                {
                    "allowBackupNetworkMounts": True,
                    "allowBackupHiddenFoldersInNetworkMounts": True,
                    "useWindowsVss": True,
                    "name": "fileset_name",
                    "includes": [
                        "string"
                    ],
                    "excludes": [
                        "string"
                    ],
                    "exceptions": [
                        "string"
                    ],
                    "operatingSystemType": "UnixLike",
                    "shareType": "NFS",
                    "preBackupScript": "string",
                    "postBackupScript": "string",
                    "backupScriptTimeout": 0,
                    "backupScriptErrorHandling": "string",
                    "isArrayEnabled": True,
                    "id": "string",
                    "primaryClusterId": "string",
                    "isArchived": True,
                    "hostCount": 0,
                    "shareCount": 0
                },
                {
                    "allowBackupNetworkMounts": True,
                    "allowBackupHiddenFoldersInNetworkMounts": True,
                    "useWindowsVss": True,
                    "name": "fileset_name",
                    "includes": [
                        "string"
                    ],
                    "excludes": [
                        "string"
                    ],
                    "exceptions": [
                        "string"
                    ],
                    "operatingSystemType": "UnixLike",
                    "shareType": "NFS",
                    "preBackupScript": "string",
                    "postBackupScript": "string",
                    "backupScriptTimeout": 0,
                    "backupScriptErrorHandling": "string",
                    "isArrayEnabled": True,
                    "id": "string",
                    "primaryClusterId": "string",
                    "isArchived": True,
                    "hostCount": 0,
                    "shareCount": 0
                }
            ],
            "total": 2
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_v1_host(), mock_get_v1_fileset_template()]

    with pytest.raises(InvalidParameterException) as error:
        rubrik.assign_physical_host_fileset("hostname", "fileset_name", "Linux", "sla_name", [""], ["", True, True])

    error_message = error.value.args[0]

    assert error_message == "The Rubrik cluster contains multiple Linux Filesets named 'fileset_name' that match all of the populate function arguments. Please use a unique Fileset."


def test_assign_physical_host_fileset_patch_sla(rubrik, mocker):

    def mock_get_v1_host():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "string",
                    "hostname": "hostname",
                    "primaryClusterId": "string",
                    "operatingSystem": "string",
                    "operatingSystemType": "string",
                    "status": "string",
                    "nasBaseConfig": {
                        "vendorType": "string",
                        "apiUsername": "string",
                        "apiCertificate": "string",
                        "apiHostname": "string",
                        "apiEndpoint": "string",
                        "zoneName": "string"
                    },
                    "mssqlCbtEnabled": "Enabled",
                    "mssqlCbtEffectiveStatus": "On",
                    "organizationId": "string",
                    "organizationName": "string"
                }
            ],
            "total": 2
        }

    def mock_get_v1_fileset_template():
        return {
            "hasMore": True,
            "data": [
                {
                    "allowBackupNetworkMounts": True,
                    "allowBackupHiddenFoldersInNetworkMounts": True,
                    "useWindowsVss": True,
                    "name": "fileset_name",
                    "includes": [
                        "string"
                    ],
                    "excludes": [
                        "string"
                    ],
                    "exceptions": [
                        "string"
                    ],
                    "operatingSystemType": "UnixLike",
                    "shareType": "NFS",
                    "preBackupScript": "string",
                    "postBackupScript": "string",
                    "backupScriptTimeout": 0,
                    "backupScriptErrorHandling": "string",
                    "isArrayEnabled": True,
                    "id": "string",
                    "primaryClusterId": "string",
                    "isArchived": True,
                    "hostCount": 0,
                    "shareCount": 0
                }
            ],
            "total": 1
        }

    def mock_get_v1_sla_domain():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_sla_id",
                    "primaryClusterId": "string",
                    "name": "sla_name",
                    "frequencies": [
                        {
                            "timeUnit": "string",
                            "frequency": 0,
                            "retention": 0
                        }
                    ],
                    "allowedBackupWindows": [
                        {
                            "startTimeAttributes": {
                                "minutes": 0,
                                "hour": 0,
                                "dayOfWeek": 0
                            },
                            "durationInHours": 0
                        }
                    ],
                    "firstFullAllowedBackupWindows": [
                        {
                            "startTimeAttributes": {
                                "minutes": 0,
                                "hour": 0,
                                "dayOfWeek": 0
                            },
                            "durationInHours": 0
                        }
                    ],
                    "localRetentionLimit": 0,
                    "maxLocalRetentionLimit": 0,
                    "archivalSpecs": [
                        {
                            "locationId": "string",
                            "archivalThreshold": 0
                        }
                    ],
                    "replicationSpecs": [
                        {
                            "locationId": "string",
                            "retentionLimit": 0
                        }
                    ],
                    "numDbs": 0,
                    "numOracleDbs": 0,
                    "numFilesets": 0,
                    "numHypervVms": 0,
                    "numNutanixVms": 0,
                    "numManagedVolumes": 0,
                    "numStorageArrayVolumeGroups": 0,
                    "numWindowsVolumeGroups": 0,
                    "numLinuxHosts": 0,
                    "numShares": 0,
                    "numWindowsHosts": 0,
                    "numVms": 0,
                    "numEc2Instances": 0,
                    "numVcdVapps": 0,
                    "numProtectedObjects": 0,
                    "isDefault": True,
                    "uiColor": "string"
                }
            ],
            "total": 1
        }

    def mock_get_v1_fileset():
        return {
            "hasMore": True,
            "data": [
                {
                    "allowBackupNetworkMounts": True,
                    "allowBackupHiddenFoldersInNetworkMounts": True,
                    "useWindowsVss": True,
                    "id": "string",
                    "name": "string",
                    "configuredSlaDomainId": "string",
                    "configuredSlaDomainName": "string",
                    "primaryClusterId": "string",
                    "hostId": "string",
                    "shareId": "string",
                    "hostName": "string",
                    "templateId": "string",
                    "templateName": "string",
                    "operatingSystemType": "string",
                    "effectiveSlaDomainId": "string",
                    "effectiveSlaDomainName": "string",
                    "effectiveSlaDomainPolarisManagedId": "string",
                    "includes": [
                        "string"
                    ],
                    "excludes": [
                        "string"
                    ],
                    "exceptions": [
                        "string"
                    ],
                    "isRelic": True,
                    "arraySpec": {
                        "proxyHostId": "string"
                    },
                    "isPassthrough": True
                }
            ],
            "total": 1
        }

    def mock_patch_v1_fileset():
        return {
            "configuredSlaDomainId": "string",
            "allowBackupNetworkMounts": True,
            "allowBackupHiddenFoldersInNetworkMounts": True,
            "useWindowsVss": True,
            "id": "string",
            "name": "string",
            "configuredSlaDomainName": "string",
            "primaryClusterId": "string",
            "hostId": "string",
            "shareId": "string",
            "hostName": "string",
            "templateId": "string",
            "templateName": "string",
            "operatingSystemType": "string",
            "effectiveSlaDomainId": "string",
            "effectiveSlaDomainName": "string",
            "effectiveSlaDomainPolarisManagedId": "string",
            "includes": [
                "string"
            ],
            "excludes": [
                "string"
            ],
            "exceptions": [
                "string"
            ],
            "isRelic": True,
            "arraySpec": {
                "proxyHostId": "string"
            },
            "isPassthrough": True,
            "protectionDate": "2019-05-23T15:36:06.889Z",
            "snapshotCount": 0,
            "archivedSnapshotCount": 0,
            "snapshots": [
                {
                    "id": "string",
                    "date": "2019-05-23T15:36:06.889Z",
                    "expirationDate": "2019-05-23T15:36:06.889Z",
                    "sourceObjectType": "string",
                    "isOnDemandSnapshot": True,
                    "cloudState": 0,
                    "consistencyLevel": "string",
                    "indexState": 0,
                    "replicationLocationIds": [
                        "string"
                    ],
                    "archivalLocationIds": [
                        "string"
                    ],
                    "slaId": "string",
                    "slaName": "string",
                    "filesetName": "string",
                    "fileCount": 0
                }
            ],
            "localStorage": 0,
            "archiveStorage": 0,
            "preBackupScript": "string",
            "postBackupScript": "string",
            "backupScriptTimeout": 0,
            "backupScriptErrorHandling": "string"
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [
        mock_get_v1_host(),
        mock_get_v1_fileset_template(),
        mock_get_v1_sla_domain(),
        mock_get_v1_fileset()]

    mock_patch = mocker.patch('rubrik_cdm.Connect.patch', autospec=True, spec_set=True)
    mock_patch.return_value = mock_patch_v1_fileset()

    assert rubrik.assign_physical_host_fileset("hostname", "fileset_name", "Linux", "sla_name") == \
        mock_patch_v1_fileset()


def test_assign_physical_host_fileset_idempotence(rubrik, mocker):

    def mock_get_v1_host():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "string",
                    "hostname": "hostname",
                    "primaryClusterId": "string",
                    "operatingSystem": "string",
                    "operatingSystemType": "string",
                    "status": "string",
                    "nasBaseConfig": {
                        "vendorType": "string",
                        "apiUsername": "string",
                        "apiCertificate": "string",
                        "apiHostname": "string",
                        "apiEndpoint": "string",
                        "zoneName": "string"
                    },
                    "mssqlCbtEnabled": "Enabled",
                    "mssqlCbtEffectiveStatus": "On",
                    "organizationId": "string",
                    "organizationName": "string"
                }
            ],
            "total": 2
        }

    def mock_get_v1_fileset_template():
        return {
            "hasMore": True,
            "data": [
                {
                    "allowBackupNetworkMounts": True,
                    "allowBackupHiddenFoldersInNetworkMounts": True,
                    "useWindowsVss": True,
                    "name": "fileset_name",
                    "includes": [
                        "string"
                    ],
                    "excludes": [
                        "string"
                    ],
                    "exceptions": [
                        "string"
                    ],
                    "operatingSystemType": "UnixLike",
                    "shareType": "NFS",
                    "preBackupScript": "string",
                    "postBackupScript": "string",
                    "backupScriptTimeout": 0,
                    "backupScriptErrorHandling": "string",
                    "isArrayEnabled": True,
                    "id": "string",
                    "primaryClusterId": "string",
                    "isArchived": True,
                    "hostCount": 0,
                    "shareCount": 0
                }
            ],
            "total": 1
        }

    def mock_get_v1_sla_domain():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_sla_id",
                    "primaryClusterId": "string",
                    "name": "sla_name",
                    "frequencies": [
                        {
                            "timeUnit": "string",
                            "frequency": 0,
                            "retention": 0
                        }
                    ],
                    "allowedBackupWindows": [
                        {
                            "startTimeAttributes": {
                                "minutes": 0,
                                "hour": 0,
                                "dayOfWeek": 0
                            },
                            "durationInHours": 0
                        }
                    ],
                    "firstFullAllowedBackupWindows": [
                        {
                            "startTimeAttributes": {
                                "minutes": 0,
                                "hour": 0,
                                "dayOfWeek": 0
                            },
                            "durationInHours": 0
                        }
                    ],
                    "localRetentionLimit": 0,
                    "maxLocalRetentionLimit": 0,
                    "archivalSpecs": [
                        {
                            "locationId": "string",
                            "archivalThreshold": 0
                        }
                    ],
                    "replicationSpecs": [
                        {
                            "locationId": "string",
                            "retentionLimit": 0
                        }
                    ],
                    "numDbs": 0,
                    "numOracleDbs": 0,
                    "numFilesets": 0,
                    "numHypervVms": 0,
                    "numNutanixVms": 0,
                    "numManagedVolumes": 0,
                    "numStorageArrayVolumeGroups": 0,
                    "numWindowsVolumeGroups": 0,
                    "numLinuxHosts": 0,
                    "numShares": 0,
                    "numWindowsHosts": 0,
                    "numVms": 0,
                    "numEc2Instances": 0,
                    "numVcdVapps": 0,
                    "numProtectedObjects": 0,
                    "isDefault": True,
                    "uiColor": "string"
                }
            ],
            "total": 1
        }

    def mock_get_v1_fileset():
        return {
            "hasMore": True,
            "data": [
                {
                    "allowBackupNetworkMounts": True,
                    "allowBackupHiddenFoldersInNetworkMounts": True,
                    "useWindowsVss": True,
                    "id": "string",
                    "name": "string",
                    "configuredSlaDomainId": "string_sla_id",
                    "configuredSlaDomainName": "string",
                    "primaryClusterId": "string",
                    "hostId": "string",
                    "shareId": "string",
                    "hostName": "string",
                    "templateId": "string",
                    "templateName": "string",
                    "operatingSystemType": "string",
                    "effectiveSlaDomainId": "string",
                    "effectiveSlaDomainName": "string",
                    "effectiveSlaDomainPolarisManagedId": "string",
                    "includes": [
                        "string"
                    ],
                    "excludes": [
                        "string"
                    ],
                    "exceptions": [
                        "string"
                    ],
                    "isRelic": True,
                    "arraySpec": {
                        "proxyHostId": "string"
                    },
                    "isPassthrough": True
                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [
        mock_get_v1_host(),
        mock_get_v1_fileset_template(),
        mock_get_v1_sla_domain(),
        mock_get_v1_fileset()]

    assert rubrik.assign_physical_host_fileset("hostname", "fileset_name", "Linux", "sla_name") == \
        "No change required. The Linux Fileset 'fileset_name' is already assigned to the SLA Domain 'sla_name' on the physical host 'hostname'."


def test_assign_physical_host_fileset_no_current_fileset(rubrik, mocker):

    def mock_get_v1_host():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "string",
                    "hostname": "hostname",
                    "primaryClusterId": "string",
                    "operatingSystem": "string",
                    "operatingSystemType": "string",
                    "status": "string",
                    "nasBaseConfig": {
                        "vendorType": "string",
                        "apiUsername": "string",
                        "apiCertificate": "string",
                        "apiHostname": "string",
                        "apiEndpoint": "string",
                        "zoneName": "string"
                    },
                    "mssqlCbtEnabled": "Enabled",
                    "mssqlCbtEffectiveStatus": "On",
                    "organizationId": "string",
                    "organizationName": "string"
                }
            ],
            "total": 2
        }

    def mock_get_v1_fileset_template():
        return {
            "hasMore": True,
            "data": [
                {
                    "allowBackupNetworkMounts": True,
                    "allowBackupHiddenFoldersInNetworkMounts": True,
                    "useWindowsVss": True,
                    "name": "fileset_name",
                    "includes": [
                        "string"
                    ],
                    "excludes": [
                        "string"
                    ],
                    "exceptions": [
                        "string"
                    ],
                    "operatingSystemType": "UnixLike",
                    "shareType": "NFS",
                    "preBackupScript": "string",
                    "postBackupScript": "string",
                    "backupScriptTimeout": 0,
                    "backupScriptErrorHandling": "string",
                    "isArrayEnabled": True,
                    "id": "string",
                    "primaryClusterId": "string",
                    "isArchived": True,
                    "hostCount": 0,
                    "shareCount": 0
                }
            ],
            "total": 1
        }

    def mock_get_v1_sla_domain():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_sla_id",
                    "primaryClusterId": "string",
                    "name": "sla_name",
                    "frequencies": [
                        {
                            "timeUnit": "string",
                            "frequency": 0,
                            "retention": 0
                        }
                    ],
                    "allowedBackupWindows": [
                        {
                            "startTimeAttributes": {
                                "minutes": 0,
                                "hour": 0,
                                "dayOfWeek": 0
                            },
                            "durationInHours": 0
                        }
                    ],
                    "firstFullAllowedBackupWindows": [
                        {
                            "startTimeAttributes": {
                                "minutes": 0,
                                "hour": 0,
                                "dayOfWeek": 0
                            },
                            "durationInHours": 0
                        }
                    ],
                    "localRetentionLimit": 0,
                    "maxLocalRetentionLimit": 0,
                    "archivalSpecs": [
                        {
                            "locationId": "string",
                            "archivalThreshold": 0
                        }
                    ],
                    "replicationSpecs": [
                        {
                            "locationId": "string",
                            "retentionLimit": 0
                        }
                    ],
                    "numDbs": 0,
                    "numOracleDbs": 0,
                    "numFilesets": 0,
                    "numHypervVms": 0,
                    "numNutanixVms": 0,
                    "numManagedVolumes": 0,
                    "numStorageArrayVolumeGroups": 0,
                    "numWindowsVolumeGroups": 0,
                    "numLinuxHosts": 0,
                    "numShares": 0,
                    "numWindowsHosts": 0,
                    "numVms": 0,
                    "numEc2Instances": 0,
                    "numVcdVapps": 0,
                    "numProtectedObjects": 0,
                    "isDefault": True,
                    "uiColor": "string"
                }
            ],
            "total": 1
        }

    def mock_get_v1_fileset():
        return {
            "hasMore": True,
            "data": [],
            "total": 0
        }

    def mock_post_v1_fileset():
        return {
            "configuredSlaDomainId": "string",
            "allowBackupNetworkMounts": True,
            "allowBackupHiddenFoldersInNetworkMounts": True,
            "useWindowsVss": True,
            "id": "string",
            "name": "string",
            "configuredSlaDomainName": "string",
            "primaryClusterId": "string",
            "hostId": "string",
            "shareId": "string",
            "hostName": "string",
            "templateId": "string",
            "templateName": "string",
            "operatingSystemType": "string",
            "effectiveSlaDomainId": "string",
            "effectiveSlaDomainName": "string",
            "effectiveSlaDomainPolarisManagedId": "string",
            "includes": [
                "string"
            ],
            "excludes": [
                "string"
            ],
            "exceptions": [
                "string"
            ],
            "isRelic": True,
            "arraySpec": {
                "proxyHostId": "string"
            },
            "isPassthrough": True,
            "protectionDate": "2019-05-23T15:36:06.821Z",
            "snapshotCount": 0,
            "archivedSnapshotCount": 0,
            "snapshots": [
                {
                    "id": "string",
                    "date": "2019-05-23T15:36:06.821Z",
                    "expirationDate": "2019-05-23T15:36:06.821Z",
                    "sourceObjectType": "string",
                    "isOnDemandSnapshot": True,
                    "cloudState": 0,
                    "consistencyLevel": "string",
                    "indexState": 0,
                    "replicationLocationIds": [
                        "string"
                    ],
                    "archivalLocationIds": [
                        "string"
                    ],
                    "slaId": "string",
                    "slaName": "string",
                    "filesetName": "string",
                    "fileCount": 0
                }
            ],
            "localStorage": 0,
            "archiveStorage": 0,
            "preBackupScript": "string",
            "postBackupScript": "string",
            "backupScriptTimeout": 0,
            "backupScriptErrorHandling": "string"
        }

    def mock_patch_v1_fileset():
        return {
            "configuredSlaDomainId": "string",
            "allowBackupNetworkMounts": True,
            "allowBackupHiddenFoldersInNetworkMounts": True,
            "useWindowsVss": True,
            "id": "string",
            "name": "string",
            "configuredSlaDomainName": "string",
            "primaryClusterId": "string",
            "hostId": "string",
            "shareId": "string",
            "hostName": "string",
            "templateId": "string",
            "templateName": "string",
            "operatingSystemType": "string",
            "effectiveSlaDomainId": "string",
            "effectiveSlaDomainName": "string",
            "effectiveSlaDomainPolarisManagedId": "string",
            "includes": [
                "string"
            ],
            "excludes": [
                "string"
            ],
            "exceptions": [
                "string"
            ],
            "isRelic": True,
            "arraySpec": {
                "proxyHostId": "string"
            },
            "isPassthrough": True,
            "protectionDate": "2019-05-23T15:36:06.889Z",
            "snapshotCount": 0,
            "archivedSnapshotCount": 0,
            "snapshots": [
                {
                    "id": "string",
                    "date": "2019-05-23T15:36:06.889Z",
                    "expirationDate": "2019-05-23T15:36:06.889Z",
                    "sourceObjectType": "string",
                    "isOnDemandSnapshot": True,
                    "cloudState": 0,
                    "consistencyLevel": "string",
                    "indexState": 0,
                    "replicationLocationIds": [
                        "string"
                    ],
                    "archivalLocationIds": [
                        "string"
                    ],
                    "slaId": "string",
                    "slaName": "string",
                    "filesetName": "string",
                    "fileCount": 0
                }
            ],
            "localStorage": 0,
            "archiveStorage": 0,
            "preBackupScript": "string",
            "postBackupScript": "string",
            "backupScriptTimeout": 0,
            "backupScriptErrorHandling": "string"
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [
        mock_get_v1_host(),
        mock_get_v1_fileset_template(),
        mock_get_v1_sla_domain(),
        mock_get_v1_fileset()]

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_v1_fileset()

    mock_patch = mocker.patch('rubrik_cdm.Connect.patch', autospec=True, spec_set=True)
    mock_patch.return_value = mock_patch_v1_fileset()

    assert rubrik.assign_physical_host_fileset("hostname", "fileset_name", "Linux", "sla_name") == \
        (mock_post_v1_fileset(), mock_patch_v1_fileset())


#######
#######
#######
#######

# def test_aws_s3_cloudout_invalid_aws_region(rubrik):

#     with pytest.raises(InvalidParameterException) as error:
#         rubrik.aws_s3_cloudout(
#             "awsbucketname",
#             "archive_name",
#             "not_a_valid_aws_region",
#             "aws_region",
#             "aws_access_key",
#             "aws_secret_key")

#     error_message = error.value.args[0]

#     assert error_message == "The `aws_region` must be one of the following: ['ap-south-1', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'ca-central-1', 'cn-north-1', 'cn-northwest-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'sa-east-1', 'us-gov-west-1', 'us-west-1', 'us-east-1', 'us-east-2', 'us-west-2']"


# def test_aws_s3_cloudout_invalid_storage_class(rubrik):

#     with pytest.raises(InvalidParameterException) as error:
#         rubrik.aws_s3_cloudout(
#             "awsbucketname",
#             "archive_name",
#             "ap-south-1",
#             "aws_access_key",
#             "aws_secret_key",
#             "kms_master_key_id",
#             "rsa_key",
#             "not_a_valid_storage_class")

#     error_message = error.value.args[0]

#     assert error_message == "The `storage_class` must be one of the following: ['standard', 'standard_ia', 'reduced_redundancy', 'onezone_ia']"


# @pytest.mark.parametrize('archive_name', ["_", "/", "*", "?", "%", ".", ":", "|", "<", ">"])
# def test_aws_s3_cloudout_invalid_aws_bucket_name(rubrik, archive_name):

#     with pytest.raises(InvalidParameterException) as error:
#         rubrik.aws_s3_cloudout(archive_name)

#     error_message = error.value.args[0]

#     assert error_message == r"The `aws_bucket_name` may not contain any of the following characters: _\/*?%.:|<>"


# def test_aws_s3_cloudout_missing_aws_region(rubrik):

#     with pytest.raises(InvalidParameterException) as error:
#         rubrik.aws_s3_cloudout("awsbucketname")

#     error_message = error.value.args[0]

#     assert error_message == "`aws_region` has not been provided."


# def test_aws_s3_cloudout_missing_aws_access_key(rubrik):

#     with pytest.raises(InvalidParameterException) as error:
#         rubrik.aws_s3_cloudout("awsbucketname", "archive_name", "ap-south-1")

#     error_message = error.value.args[0]

#     assert error_message == "`aws_access_key` has not been provided."


# def test_aws_s3_cloudout_missing_aws_secret_key(rubrik):

#     with pytest.raises(InvalidParameterException) as error:
#         rubrik.aws_s3_cloudout("awsbucketname", "archive_name", "ap-south-1", "aws_access_key")

#     error_message = error.value.args[0]

#     assert error_message == "`aws_secret_key` has not been provided."


# def test_aws_s3_cloudout_missing_kms_and_rsa(rubrik):

#     with pytest.raises(InvalidParameterException) as error:
#         rubrik.aws_s3_cloudout(
#             "awsbucketname",
#             "archive_name",
#             "ap-south-1",
#             "aws_access_key",
#             "aws_secret_key")

#     error_message = error.value.args[0]

#     assert error_message == "You must populated either `kms_master_key_id` or `rsa_key`."


# def test_aws_s3_cloudout_both_kms_and_rsa_populated(rubrik):

#     with pytest.raises(InvalidParameterException) as error:
#         rubrik.aws_s3_cloudout(
#             "awsbucketname",
#             "archive_name",
#             "ap-south-1",
#             "aws_access_key",
#             "aws_secret_key",
#             "kms_master_key_id",
#             "rsa_key")

#     error_message = error.value.args[0]

#     assert error_message == "Both `kms_master_key_id` or `rsa_key` have been populated. You may only use one."


# def test_aws_s3_cloudout_idempotence(rubrik, mocker):

#     def mock_get_internal_archive_object_store():
#         return {
#             "hasMore": True,
#             "data": [
#                 {
#                     "id": "string",
#                     "polarisManagedId": "string",
#                     "definition": {
#                         "objectStoreType": "S3",
#                         "name": "archive_name",
#                         "accessKey": "aws_access_key",
#                         "bucket": "awsbucketname",
#                         "defaultRegion": "ap-south-1",
#                         "isComputeEnabled": True,
#                         "isConsolidationEnabled": True,
#                         "defaultComputeNetworkConfig": {
#                             "subnetId": "string",
#                             "vNetId": "string",
#                             "securityGroupId": "string",
#                             "resourceGroupId": "string"
#                         },
#                         "storageClass": "STANDARD",
#                         "encryptionType": "RSA_KEY_ENCRYPTION"
#                     },

#                 }
#             ],
#             "total": 1
#         }

#     mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
#     mock_get.return_value = mock_get_internal_archive_object_store()

#     assert rubrik.aws_s3_cloudout("awsbucketname", "archive_name", "ap-south-1", "aws_access_key", "aws_secret_key", None, "rsa_key") \
#         == "No change required. The 'archive_name' archival location is already configured on the Rubrik cluster."


# def test_aws_s3_cloudout_archive_name_already_exsits(rubrik, mocker):

#     def mock_get_internal_archive_object_store():
#         return {
#             "hasMore": True,
#             "data": [
#                 {
#                     "id": "string",
#                     "polarisManagedId": "string",
#                     "definition": {
#                         "objectStoreType": "S3",
#                         "name": "archive_name",
#                         "accessKey": "string",
#                         "bucket": "string",
#                         "defaultRegion": "string",
#                         "isComputeEnabled": True,
#                         "isConsolidationEnabled": True,
#                         "defaultComputeNetworkConfig": {
#                             "subnetId": "string",
#                             "vNetId": "string",
#                             "securityGroupId": "string",
#                             "resourceGroupId": "string"
#                         },
#                         "storageClass": "STANDARD",
#                         "encryptionType": "RSA_KEY_ENCRYPTION"
#                     },

#                 }
#             ],
#             "total": 1
#         }

#     mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
#     mock_get.return_value = mock_get_internal_archive_object_store()

#     with pytest.raises(InvalidParameterException) as error:
#         rubrik.aws_s3_cloudout(
#             "awsbucketname",
#             "archive_name",
#             "ap-south-1",
#             "aws_access_key",
#             "aws_secret_key",
#             None,
#             "rsa_key")

#     error_message = error.value.args[0]

#     assert error_message == "Archival location with name 'archive_name' already exists. Please enter a unique `archive_name`."


# def test_aws_s3_cloudout(rubrik, mocker):

#     def mock_get_internal_archive_object_store():
#         return {
#             "hasMore": True,
#             "data": [
#                 {
#                     "id": "string",
#                     "polarisManagedId": "string",
#                     "definition": {
#                         "objectStoreType": "S3",
#                         "name": "string",
#                         "accessKey": "aws_access_key",
#                         "bucket": "awsbucketname",
#                         "defaultRegion": "ap-south-1",
#                         "isComputeEnabled": True,
#                         "isConsolidationEnabled": True,
#                         "defaultComputeNetworkConfig": {
#                             "subnetId": "string",
#                             "vNetId": "string",
#                             "securityGroupId": "string",
#                             "resourceGroupId": "string"
#                         },
#                         "storageClass": "STANDARD",
#                         "encryptionType": "RSA_KEY_ENCRYPTION"
#                     },

#                 }
#             ],
#             "total": 1
#         }

#     def mock_post_internal_archive_object_store():
#         return {
#             "jobInstanceId": "string"
#         }

#     mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
#     mock_get.return_value = mock_get_internal_archive_object_store()

#     mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
#     mock_post.return_value = mock_post_internal_archive_object_store()

#     assert rubrik.aws_s3_cloudout("awsbucketname", "archive_name", "ap-south-1", "aws_access_key", "aws_secret_key", None, "rsa_key") \
#         == mock_post_internal_archive_object_store()


# def test_update_aws_s3_cloudout_invalid_storage_class(rubrik):

#     with pytest.raises(InvalidParameterException) as error:
#         rubrik.update_aws_s3_cloudout("current_archive_name", storage_class="not_a_valid_storage_class")

#     error_message = error.value.args[0]

#     assert error_message == "The `storage_class` must be one of the following: ['standard', 'standard_ia', 'reduced_redundancy', 'onezone_ia']"


# def test_update_aws_s3_cloudout_current_archive_name_not_found(rubrik, mocker):

#     def mock_get_internal_archive_object_store():
#         return {
#             "hasMore": True,
#             "data": [
#                 {
#                     "id": "string",
#                     "polarisManagedId": "string",
#                     "definition": {
#                         "objectStoreType": "S3",
#                         "name": "string",
#                         "accessKey": "aws_access_key",
#                         "bucket": "awsbucketname",
#                         "defaultRegion": "ap-south-1",
#                         "isComputeEnabled": True,
#                         "isConsolidationEnabled": True,
#                         "defaultComputeNetworkConfig": {
#                             "subnetId": "string",
#                             "vNetId": "string",
#                             "securityGroupId": "string",
#                             "resourceGroupId": "string"
#                         },
#                         "storageClass": "STANDARD",
#                         "encryptionType": "RSA_KEY_ENCRYPTION"
#                     },

#                 }
#             ],
#             "total": 1
#         }

#     mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
#     mock_get.return_value = mock_get_internal_archive_object_store()

#     with pytest.raises(InvalidParameterException) as error:
#         rubrik.update_aws_s3_cloudout("current_archive_name")

#     error_message = error.value.args[0]

#     assert error_message == "No S3 archival location with name 'current_archive_name' exists."


# def test_update_aws_s3_cloudout(rubrik, mocker):

#     def mock_get_internal_archive_object_store():
#         return {
#             "hasMore": True,
#             "data": [
#                 {
#                     "id": "string",
#                     "polarisManagedId": "string",
#                     "definition": {
#                         "objectStoreType": "S3",
#                         "name": "current_archive_name",
#                         "accessKey": "aws_access_key",
#                         "bucket": "awsbucketname",
#                         "defaultRegion": "ap-south-1",
#                         "isComputeEnabled": True,
#                         "isConsolidationEnabled": True,
#                         "defaultComputeNetworkConfig": {
#                             "subnetId": "string",
#                             "vNetId": "string",
#                             "securityGroupId": "string",
#                             "resourceGroupId": "string"
#                         },
#                         "storageClass": "STANDARD",
#                         "encryptionType": "RSA_KEY_ENCRYPTION"
#                     },

#                 }
#             ],
#             "total": 1
#         }

#     def mock_patch_internal_archive_object_store():
#         return {
#             "jobInstanceId": "string"
#         }

#     mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
#     mock_get.return_value = mock_get_internal_archive_object_store()

#     mock_patch = mocker.patch('rubrik_cdm.Connect.patch', autospec=True, spec_set=True)
#     mock_patch.return_value = mock_patch_internal_archive_object_store()

#     assert rubrik.update_aws_s3_cloudout("current_archive_name", "new_archive_name", "aws_access_key", "aws_secret_key", "standard") \
#         == mock_patch_internal_archive_object_store()


# def test_aws_s3_cloudon_idempotence(rubrik, mocker):

#     def mock_get_internal_archive_object_store():
#         return {
#             "hasMore": True,
#             "data": [
#                 {
#                     "id": "string",
#                     "polarisManagedId": "string",
#                     "definition": {
#                         "objectStoreType": "S3",
#                         "name": "archive_name",
#                         "accessKey": "aws_access_key",
#                         "bucket": "awsbucketname",
#                         "defaultRegion": "ap-south-1",
#                         "isComputeEnabled": True,
#                         "isConsolidationEnabled": True,
#                         "defaultComputeNetworkConfig": {
#                             "subnetId": "subnet_id",
#                             "vNetId": "vpc_id",
#                             "securityGroupId": "security_group_id",
#                         },
#                         "storageClass": "STANDARD",
#                         "encryptionType": "RSA_KEY_ENCRYPTION"
#                     },

#                 }
#             ],
#             "total": 1
#         }

#     mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
#     mock_get.return_value = mock_get_internal_archive_object_store()

#     assert rubrik.aws_s3_cloudon("archive_name", "vpc_id", "subnet_id", "security_group_id") \
#         == "No change required. The 'archive_name' archival location is already configured for CloudOn."


# def test_aws_s3_cloudon_archive_name_not_found(rubrik, mocker):

#     def mock_get_internal_archive_object_store():
#         return {
#             "hasMore": True,
#             "data": [
#                 {
#                     "id": "string",
#                     "polarisManagedId": "string",
#                     "definition": {
#                         "objectStoreType": "S3",
#                         "name": "string",
#                         "accessKey": "aws_access_key",
#                         "bucket": "awsbucketname",
#                         "defaultRegion": "ap-south-1",
#                         "isComputeEnabled": True,
#                         "isConsolidationEnabled": True,
#                         "storageClass": "STANDARD",
#                         "encryptionType": "RSA_KEY_ENCRYPTION"
#                     },

#                 }
#             ],
#             "total": 1
#         }

#     mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
#     mock_get.return_value = mock_get_internal_archive_object_store()

#     with pytest.raises(InvalidParameterException) as error:
#         rubrik.aws_s3_cloudon("archive_name", "vpc_id", "subnet_id", "security_group_id")

#     error_message = error.value.args[0]

#     assert error_message == "The Rubrik cluster does not have an archive location named 'archive_name'."


# def test_aws_s3_cloudon(rubrik, mocker):

#     def mock_get_internal_archive_object_store():
#         return {
#             "hasMore": True,
#             "data": [
#                 {
#                     "id": "string",
#                     "polarisManagedId": "string",
#                     "definition": {
#                         "objectStoreType": "S3",
#                         "name": "archive_name",
#                         "accessKey": "aws_access_key",
#                         "bucket": "awsbucketname",
#                         "defaultRegion": "ap-south-1",
#                         "isComputeEnabled": True,
#                         "isConsolidationEnabled": True,
#                         "storageClass": "STANDARD",
#                         "encryptionType": "RSA_KEY_ENCRYPTION"
#                     },

#                 }
#             ],
#             "total": 1
#         }

#     def mock_patch_internal_archive_object_store():
#         return {
#             "jobInstanceId": "string"
#         }

#     mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
#     mock_get.return_value = mock_get_internal_archive_object_store()

#     mock_patch = mocker.patch('rubrik_cdm.Connect.patch', autospec=True, spec_set=True)
#     mock_patch.return_value = mock_patch_internal_archive_object_store()

#     assert rubrik.aws_s3_cloudon("archive_name", "vpc_id", "subnet_id", "security_group_id") \
#         == mock_patch_internal_archive_object_store()


# @pytest.mark.parametrize('container', ["_", "/", "*", "?", "%", ".", ":", "|", "<", ">"])
# def test_azure_cloudout_invalid_container(rubrik, container):

#     with pytest.raises(InvalidParameterException) as error:
#         rubrik.azure_cloudout(container, "azure_access_key", "storage_account_name", "rsa_key")

#     error_message = error.value.args[0]

#     assert error_message == r"The `container` may not contain any of the following characters: _\/*?%.:|<>"


# def test_azure_cloudout_invalid_instance_type(rubrik):

#     with pytest.raises(InvalidParameterException) as error:
#         rubrik.azure_cloudout("container", "azure_access_key", "storage_account_name",
#                               "rsa_key", instance_type="not_a_valid_instance_type")

#     error_message = error.value.args[0]

#     assert error_message == "The `instance_type` argument must be one of the following: ['default', 'china', 'germany', 'government']"


# def test_azure_cloudout_idempotence(rubrik, mocker):

#     def mock_get_internal_archive_object_store():
#         return {
#             "hasMore": True,
#             "data": [
#                 {
#                     "id": "string",
#                     "polarisManagedId": "string",
#                     "definition": {
#                         "objectStoreType": "Azure",
#                         "name": "archive_name",
#                         "accessKey": "storage_account_name",
#                         "bucket": "container",
#                         "isComputeEnabled": True,
#                         "isConsolidationEnabled": True,
#                         "encryptionType": "RSA_KEY_ENCRYPTION"
#                     },

#                 }
#             ],
#             "total": 1
#         }

#     mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
#     mock_get.return_value = mock_get_internal_archive_object_store()

#     assert rubrik.azure_cloudout("container", "azure_access_key", "storage_account_name", "rsa_key", "archive_name") \
#         == "No change required. The 'archive_name' archival location is already configured on the Rubrik cluster."


# def test_azure_cloudout_invalid_archive_name(rubrik, mocker):

#     def mock_get_internal_archive_object_store():
#         return {
#             "hasMore": True,
#             "data": [
#                 {
#                     "id": "string",
#                     "polarisManagedId": "string",
#                     "definition": {
#                         "objectStoreType": "Azure",
#                         "name": "archive_name",
#                         "accessKey": "string",
#                         "bucket": "string",
#                         "isComputeEnabled": True,
#                         "isConsolidationEnabled": True,
#                         "encryptionType": "RSA_KEY_ENCRYPTION"
#                     },

#                 }
#             ],
#             "total": 1
#         }

#     mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
#     mock_get.return_value = mock_get_internal_archive_object_store()

#     with pytest.raises(InvalidParameterException) as error:
#         rubrik.azure_cloudout("container", "azure_access_key", "storage_account_name", "rsa_key", "archive_name")

#     error_message = error.value.args[0]

#     assert error_message == "Archival location with name 'archive_name' already exists. Please enter a unique `name`."


# def test_azure_cloudout(rubrik, mocker):

#     def mock_get_internal_archive_object_store():
#         return {
#             "hasMore": True,
#             "data": [
#                 {
#                     "id": "string",
#                     "polarisManagedId": "string",
#                     "definition": {
#                         "objectStoreType": "Azure",
#                         "name": "string",
#                         "accessKey": "storage_account_name",
#                         "bucket": "container",
#                         "isComputeEnabled": True,
#                         "isConsolidationEnabled": True,
#                         "encryptionType": "RSA_KEY_ENCRYPTION"
#                     },

#                 }
#             ],
#             "total": 1
#         }

#     def mock_patch_internal_archive_object_store():
#         return {
#             "jobInstanceId": "string"
#         }

#     mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
#     mock_get.return_value = mock_get_internal_archive_object_store()

#     mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
#     mock_post.return_value = mock_patch_internal_archive_object_store()

#     assert rubrik.azure_cloudout("container", "azure_access_key", "storage_account_name",
#                                  "rsa_key", "archive_name") == mock_patch_internal_archive_object_store()


# def test_azure_cloudon_invalid_region(rubrik):

#     with pytest.raises(InvalidParameterException) as error:
#         rubrik.azure_cloudon(
#             "archive_name",
#             "container",
#             "storage_account_name",
#             "application_id",
#             "application_key",
#             "tenant_id",
#             "not_a_valid_region",
#             "virtual_network_id",
#             "subnet_name",
#             "security_group_id")

#     error_message = error.value.args[0]

#     assert error_message == "The `region` must be one of the following: ['westus', 'westus2', 'centralus', 'eastus', 'eastus2', 'northcentralus', 'southcentralus', 'westcentralus', 'canadacentral', 'canadaeast', 'brazilsouth', 'northeurope', 'westeurope', 'uksouth', 'ukwest', 'eastasia', 'southeastasia', 'japaneast', 'japanwest', 'australiaeast', 'australiasoutheast', 'centralindia', 'southindia', 'westindia', 'koreacentral', 'koreasouth']"


# def test_azure_cloudon_idempotence(rubrik, mocker):

#     def mock_get_internal_archive_object_store():
#         return {
#             "hasMore": True,
#             "data": [
#                 {
#                     "id": "string",
#                     "polarisManagedId": "string",
#                     "definition": {
#                         "objectStoreType": "Azure",
#                         "name": "archive_name",
#                         "accessKey": "storage_account_name",
#                         "bucket": "container",
#                         "isComputeEnabled": True,
#                         "isConsolidationEnabled": True,
#                         "defaultComputeNetworkConfig": {
#                             "subnetId": "subnet_name",
#                             "vNetId": "/subscriptions/89b90dec-a6e1-4q9e-bc12-23138bb3cee4/resourceGroups/PythonSDK/providers/Microsoft.Network/virtualNetworks/pythonsdk",
#                             "securityGroupId": "security_group_id",
#                             "resourceGroupId": "string"
#                         },
#                         "azureComputeSummary": {
#                             "tenantId": "tenant_id",
#                             "subscriptionId": "89b90dec-a6e1-4q9e-bc12-23138bb3cee4",
#                             "clientId": "application_id",
#                             "region": "westus",
#                             "generalPurposeStorageAccountName": "storage_account_name",
#                             "containerName": "container",
#                             "environment": "AZURE"
#                         },
#                         "encryptionType": "RSA_KEY_ENCRYPTION"
#                     },


#                 }
#             ],
#             "total": 1
#         }

#     mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
#     mock_get.return_value = mock_get_internal_archive_object_store()

#     assert rubrik.azure_cloudon(
#         "archive_name",
#         "container",
#         "storage_account_name",
#         "application_id",
#         "application_key",
#         "tenant_id",
#         "westus",
#         "/subscriptions/89b90dec-a6e1-4q9e-bc12-23138bb3cee4/resourceGroups/PythonSDK/providers/Microsoft.Network/virtualNetworks/pythonsdk",
#         "subnet_name",
#         "security_group_id") == "No change required. The 'archive_name' archival location is already configured for CloudOn."


# def test_update_aws_native_account_minimum_installed_cdm_version_not_met(rubrik, mocker):

#     def mock_self_cluster_version():
#         return "4.0.1-1280"

#     mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
#     mock_cluster_version.return_value = mock_self_cluster_version()

#     with pytest.raises(CDMVersionException) as error:
#         rubrik.update_aws_native_account("aws_account_name", {})


# def test_update_aws_native_account_invalid_config(rubrik, mocker):

#     def mock_self_cluster_version():
#         return "4.2.1-1280"

#     mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
#     mock_cluster_version.return_value = mock_self_cluster_version()

#     with pytest.raises(InvalidTypeException) as error:
#         rubrik.update_aws_native_account("aws_account_name", "not_a_dictionary")

#     error_message = error.value.args[0]

#     assert error_message == "The 'config' argument must be a dictionary."


# def test_update_aws_native_account(rubrik, mocker):

#     def mock_self_cluster_version():
#         return "4.2.1-1280"

#     def mock_get_internal_aws_account_name():
#         return {
#             "hasMore": True,
#             "data": [
#                 {
#                     "id": "string",
#                     "name": "aws_account_name",
#                     "primaryClusterId": "string",
#                     "status": "Connected"
#                 }
#             ],
#             "total": 1
#         }

#     def mock_patch_internal_aws_account_id():
#         return {
#             "name": "string",
#             "accessKey": "string",
#             "regions": [
#                 "string"
#             ],
#             "regionalBoltNetworkConfigs": [
#                 {
#                     "region": "string",
#                     "vNetId": "string",
#                     "subnetId": "string",
#                     "securityGroupId": "string"
#                 }
#             ],
#             "disasterRecoveryArchivalLocationId": "string",
#             "id": "string",
#             "configuredSlaDomainId": "string",
#             "configuredSlaDomainName": "string",
#             "primaryClusterId": "string"
#         }

#     mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
#     mock_cluster_version.return_value = mock_self_cluster_version()

#     mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
#     mock_get.return_value = mock_get_internal_aws_account_name()

#     mock_patch = mocker.patch('rubrik_cdm.Connect.patch', autospec=True, spec_set=True)
#     mock_patch.return_value = mock_patch_internal_aws_account_id()

#     assert rubrik.update_aws_native_account("aws_account_name", {}) == \
#         mock_patch_internal_aws_account_id()


# def test_add_aws_native_account_minimum_installed_cdm_version_not_met(rubrik, mocker):

#     def mock_self_cluster_version():
#         return "4.0.1-1280"

#     mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
#     mock_cluster_version.return_value = mock_self_cluster_version()

#     with pytest.raises(CDMVersionException) as error:
#         rubrik.add_aws_native_account(
#             "aws_account_name",
#             "aws_access_key",
#             "aws_secret_key",
#             ["not_a_valid_region"],
#             {})


# def test_add_aws_native_account_missing_aws_region(rubrik, mocker):

#     def mock_self_cluster_version():
#         return "4.2.1-1280"

#     mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
#     mock_cluster_version.return_value = mock_self_cluster_version()

#     with pytest.raises(InvalidParameterException) as error:
#         rubrik.add_aws_native_account("aws_account_name")

#     error_message = error.value.args[0]

#     assert error_message == "`aws_region` has not been provided."


# def test_add_aws_native_account_missing_aws_access_key(rubrik, mocker):

#     def mock_self_cluster_version():
#         return "4.2.1-1280"

#     mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
#     mock_cluster_version.return_value = mock_self_cluster_version()

#     with pytest.raises(InvalidParameterException) as error:
#         rubrik.add_aws_native_account("aws_account_name", aws_regions=["ap-south-1"])

#     error_message = error.value.args[0]

#     assert error_message == "`aws_access_key` has not been provided."


# def test_add_aws_native_account_missing_aws_secret_key(rubrik, mocker):

#     def mock_self_cluster_version():
#         return "4.2.1-1280"

#     mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
#     mock_cluster_version.return_value = mock_self_cluster_version()

#     with pytest.raises(InvalidParameterException) as error:
#         rubrik.add_aws_native_account("aws_account_name", "aws_access_key", aws_regions=["ap-south-1"])

#     error_message = error.value.args[0]

#     assert error_message == "`aws_secret_key` has not been provided."


# def test_add_aws_native_account_invalid_aws_regionss(rubrik, mocker):

#     def mock_self_cluster_version():
#         return "4.2.1-1280"

#     mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
#     mock_cluster_version.return_value = mock_self_cluster_version()

#     with pytest.raises(InvalidParameterException) as error:
#         rubrik.add_aws_native_account(
#             "aws_account_name",
#             "aws_access_key",
#             "aws_secret_key",
#             ["not_a_valid_region"],
#             {})

#     error_message = error.value.args[0]

#     assert error_message == "The list `aws_regions` may only contain the following values: ['ap-south-1', 'ap-northeast-3', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'ca-central-1', 'cn-north-1', 'cn-northwest-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'us-west-1', 'us-east-1', 'us-east-2', 'us-west-2']"


# def test_add_aws_native_account_invalid_regional_bolt_network_configs_list(rubrik, mocker):

#     def mock_self_cluster_version():
#         return "4.2.1-1280"

#     mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
#     mock_cluster_version.return_value = mock_self_cluster_version()

#     with pytest.raises(InvalidTypeException) as error:
#         rubrik.add_aws_native_account(
#             "aws_account_name",
#             "aws_access_key",
#             "aws_secret_key",
#             ["ap-south-1"],
#             "not_a_valid_regional_bolt_config")

#     error_message = error.value.args[0]

#     assert error_message == "`regional_bolt_network_configs` must be a list if defined."


# def test_add_aws_native_account_invalid_regional_bolt_network_configs_list_dict(rubrik, mocker):

#     def mock_self_cluster_version():
#         return "4.2.1-1280"

#     mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
#     mock_cluster_version.return_value = mock_self_cluster_version()

#     with pytest.raises(InvalidTypeException) as error:
#         rubrik.add_aws_native_account(
#             "aws_account_name",
#             "aws_access_key",
#             "aws_secret_key",
#             ["ap-south-1"],
#             ["not_a_valid_regional_bolt_config"])

#     error_message = error.value.args[0]

#     assert error_message == "The `regional_bolt_network_configs` list can only contain dicts."


# def test_add_aws_native_account_invalid_regional_bolt_network_configs_list_dict_value(rubrik, mocker):

#     def mock_self_cluster_version():
#         return "4.2.1-1280"

#     mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
#     mock_cluster_version.return_value = mock_self_cluster_version()

#     with pytest.raises(InvalidParameterException) as error:
#         rubrik.add_aws_native_account(
#             "aws_account_name",
#             "aws_access_key",
#             "aws_secret_key",
#             ["ap-south-1"],
#             [{"not_a_valid_key": "string"}])

#     error_message = error.value.args[0]

#     assert error_message == "Each `regional_bolt_network_config` dict must contain the following keys: 'region', 'vNetId', 'subnetId', 'securityGroupId'."


# def test_add_aws_native_account_invalid_aws_account_name(rubrik, mocker):

#     def mock_self_cluster_version():
#         return "4.2.1-1280"

#     def mock_get_internal_aws_account_name():
#         return {
#             "hasMore": True,
#             "data": [
#                 {
#                     "id": "string",
#                     "name": "aws_account_name",
#                     "primaryClusterId": "string",
#                     "status": "Connected"
#                 }
#             ],
#             "total": 1
#         }

#     mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
#     mock_cluster_version.return_value = mock_self_cluster_version()

#     mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
#     mock_get.return_value = mock_get_internal_aws_account_name()

#     with pytest.raises(InvalidParameterException) as error:
#         rubrik.add_aws_native_account(
#             "aws_account_name",
#             "aws_access_key",
#             "aws_secret_key",
#             ["ap-south-1"],
#             [{"region": "string", "vNetId": "string", "subnetId": "string", "securityGroupId": "string"}])

#     error_message = error.value.args[0]

#     assert error_message == "Cloud native source with name 'aws_account_name' already exists. Please enter a unique `aws_account_name`."


# def test_add_aws_native_account_idempotence(rubrik, mocker):

#     def mock_self_cluster_version():
#         return "4.2.1-1280"

#     def mock_get_internal_aws_account_name():
#         return {
#             "hasMore": True,
#             "data": [
#                 {
#                     "id": "string",
#                     "name": "string",
#                     "primaryClusterId": "string",
#                     "status": "Connected"
#                 }
#             ],
#             "total": 1
#         }

#     def mock_get_internal_aws_account_id():
#         return {
#             "name": "string",
#             "accessKey": "aws_access_key",
#             "regions": [
#                 "string"
#             ],
#             "regionalBoltNetworkConfigs": [
#                 {
#                     "region": "string",
#                     "vNetId": "string",
#                     "subnetId": "string",
#                     "securityGroupId": "string"
#                 }
#             ],
#             "disasterRecoveryArchivalLocationId": "string",
#             "id": "string",
#             "configuredSlaDomainId": "string",
#             "configuredSlaDomainName": "string",
#             "primaryClusterId": "string"
#         }

#     mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
#     mock_cluster_version.return_value = mock_self_cluster_version()

#     mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
#     mock_get.side_effect = [mock_get_internal_aws_account_name(), mock_get_internal_aws_account_id()]

#     assert rubrik.add_aws_native_account("aws_account_name",
#                                          "aws_access_key",
#                                          "aws_secret_key",
#                                          ["ap-south-1"],
#                                          [{"region": "string",
#                                            "vNetId": "string",
#                                            "subnetId": "string",
#                                            "securityGroupId": "string"}]) == "No change required. Cloud native source with access key 'aws_access_key' is already configured on the Rubrik cluster."


# def test_add_aws_native_account(rubrik, mocker):

#     def mock_self_cluster_version():
#         return "4.2.1-1280"

#     def mock_get_internal_aws_account_name():
#         return {
#             "hasMore": True,
#             "data": [
#                 {
#                     "id": "string",
#                     "name": "string",
#                     "primaryClusterId": "string",
#                     "status": "Connected"
#                 }
#             ],
#             "total": 1
#         }

#     def mock_get_internal_aws_account_id():
#         return {
#             "name": "string",
#             "accessKey": "string",
#             "regions": [
#                 "string"
#             ],
#             "regionalBoltNetworkConfigs": [
#                 {
#                     "region": "string",
#                     "vNetId": "string",
#                     "subnetId": "string",
#                     "securityGroupId": "string"
#                 }
#             ],
#             "disasterRecoveryArchivalLocationId": "string",
#             "id": "string",
#             "configuredSlaDomainId": "string",
#             "configuredSlaDomainName": "string",
#             "primaryClusterId": "string"
#         }

#     def mock_post_internal_aws_account():
#         return {
#             "id": "string",
#             "status": "string",
#             "progress": 0,
#             "startTime": "2019-05-03T16:15:38.827Z",
#             "endTime": "2019-05-03T16:15:38.827Z",
#             "nodeId": "string",
#             "error": {
#                 "message": "string"
#             },
#             "links": [
#                 {
#                     "href": "string",
#                     "rel": "string"
#                 }
#             ]
#         }
#     mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
#     mock_cluster_version.return_value = mock_self_cluster_version()

#     mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
#     mock_get.side_effect = [mock_get_internal_aws_account_name(), mock_get_internal_aws_account_id()]

#     mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
#     mock_post.return_value = mock_post_internal_aws_account()

#     assert rubrik.add_aws_native_account("aws_account_name",
#                                          "aws_access_key",
#                                          "aws_secret_key",
#                                          ["ap-south-1"],
#                                          [{"region": "string",
#                                            "vNetId": "string",
#                                            "subnetId": "string",
#                                            "securityGroupId": "string"}]) == mock_post_internal_aws_account()
