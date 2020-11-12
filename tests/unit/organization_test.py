import pytest
from rubrik_cdm import Connect


def test_add_organization_protectable_object_sql_host_idempotence(rubrik, mocker):

    def mock_get_internal_organization_org_id_mssql():
        return {
            "hasMore": True,
            "data": [
                {
                    "managedId": "host_id",
                    "objectType": "string",
                    "name": "string",
                    "primaryClusterId": "string",
                    "isDeleted": True,
                    "isRelic": True,
                    "effectiveSlaDomainId": "string",
                    "effectiveSlaDomainName": "string",
                    "descendantCounts": {
                        "appBlueprint": 0,
                        "fileset": 0,
                        "shareFileset": 0,
                        "mssqlDatabase": 0,
                        "oracleDatabase": 0,
                        "storageArrayVolumeGroup": 0,
                        "vapp": 0,
                        "volumeGroup": 0,
                        "virtualMachine": 0
                    },
                    "locations": {
                        "folder": [
                            {
                                "managedId": "string",
                                "name": "string"
                            }
                        ],
                        "infrastructure": [
                            {
                                "managedId": "string",
                                "name": "string"
                            }
                        ],
                        "physical": [
                            {
                                "managedId": "string",
                                "name": "string"
                            }
                        ]
                    },
                    "properties": {
                        "hostname": "string",
                        "clusterName": "string",
                        "operatingSystem": "string",
                        "operatingSystemType": "string",
                        "instanceName": "string"
                    },
                    "isEffectiveSlaDomainRetentionLocked": True
                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get',
                            autospec=True, spec_set=True)

    mock_get.return_value = mock_get_internal_organization_org_id_mssql()

    mock_object_id = mocker.patch('rubrik_cdm.Connect.object_id',
                                  autospec=True, spec_set=True)

    mock_object_id.side_effect = [
        "org_id", "ord_admin_role_id", "host_id"]

    assert rubrik.add_organization_protectable_object_mssql_server_host(
        "org_name", "mssql_host") == "No change required. The MSSQL host mssql_host is already assigned to the org_name organization."


def test_add_organization_protectable_object_sql_host(rubrik, mocker):

    def mock_get_internal_organization_org_id_mssql():
        return {
            "hasMore": True,
            "data": [
                {
                    "managedId": "string",
                    "objectType": "string",
                    "name": "string",
                    "primaryClusterId": "string",
                    "isDeleted": True,
                    "isRelic": True,
                    "effectiveSlaDomainId": "string",
                    "effectiveSlaDomainName": "string",
                    "descendantCounts": {
                        "appBlueprint": 0,
                        "fileset": 0,
                        "shareFileset": 0,
                        "mssqlDatabase": 0,
                        "oracleDatabase": 0,
                        "storageArrayVolumeGroup": 0,
                        "vapp": 0,
                        "volumeGroup": 0,
                        "virtualMachine": 0
                    },
                    "locations": {
                        "folder": [
                            {
                                "managedId": "string",
                                "name": "string"
                            }
                        ],
                        "infrastructure": [
                            {
                                "managedId": "string",
                                "name": "string"
                            }
                        ],
                        "physical": [
                            {
                                "managedId": "string",
                                "name": "string"
                            }
                        ]
                    },
                    "properties": {
                        "hostname": "string",
                        "clusterName": "string",
                        "operatingSystem": "string",
                        "operatingSystemType": "string",
                        "instanceName": "string"
                    },
                    "isEffectiveSlaDomainRetentionLocked": True
                }
            ],
            "total": 1
        }

    def mock_post_internal_role_org_admin_id_authorization():
        return {
            "authorizationSpecifications": [
                {
                    "privilege": "string",
                    "resources": [
                        "string"
                    ]
                }
            ],
            "roleTemplate": "string"
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get',
                            autospec=True, spec_set=True)

    mock_get.return_value = mock_get_internal_organization_org_id_mssql()

    mock_object_id = mocker.patch('rubrik_cdm.Connect.object_id',
                                  autospec=True, spec_set=True)

    mock_object_id.side_effect = [
        "org_id", "ord_admin_role_id", "host_id"]

    mock_post = mocker.patch('rubrik_cdm.Connect.post',
                             autospec=True, spec_set=True)

    mock_post.return_value = mock_post_internal_role_org_admin_id_authorization()

    assert rubrik.add_organization_protectable_object_mssql_server_host(
        "org_name", "mssql_host") == mock_post_internal_role_org_admin_id_authorization()


def test_add_organization_protectable_object_sql_server_db_idempotence(rubrik, mocker):

    def mock_get_internal_organization_org_id_mssql():
        return {
            "hasMore": True,
            "data": [
                {
                    "managedId": "mssql_db_id",
                    "objectType": "string",
                    "name": "string",
                    "primaryClusterId": "string",
                    "isDeleted": True,
                    "isRelic": True,
                    "effectiveSlaDomainId": "string",
                    "effectiveSlaDomainName": "string",
                    "descendantCounts": {
                        "appBlueprint": 0,
                        "fileset": 0,
                        "shareFileset": 0,
                        "mssqlDatabase": 0,
                        "oracleDatabase": 0,
                        "storageArrayVolumeGroup": 0,
                        "vapp": 0,
                        "volumeGroup": 0,
                        "virtualMachine": 0
                    },
                    "locations": {
                        "folder": [
                            {
                                "managedId": "string",
                                "name": "string"
                            }
                        ],
                        "infrastructure": [
                            {
                                "managedId": "string",
                                "name": "string"
                            }
                        ],
                        "physical": [
                            {
                                "managedId": "string",
                                "name": "string"
                            }
                        ]
                    },
                    "properties": {
                        "hostname": "string",
                        "clusterName": "string",
                        "operatingSystem": "string",
                        "operatingSystemType": "string",
                        "instanceName": "string"
                    },
                    "isEffectiveSlaDomainRetentionLocked": True
                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get',
                            autospec=True, spec_set=True)

    mock_get.return_value = mock_get_internal_organization_org_id_mssql()

    mock_object_id = mocker.patch('rubrik_cdm.Connect.object_id',
                                  autospec=True, spec_set=True)

    mock_object_id.side_effect = [
        "org_id", "ord_admin_role_id", "mssql_db_id"]

    assert rubrik.add_organization_protectable_object_sql_server_db(
        "org_name", "mssql_db", "mssql_host", "mssql_instance") == "No change required. The MSSQL DB mssql_db is already assigned to the org_name organization."


def test_add_organization_protectable_object_sql_server_db(rubrik, mocker):

    def mock_get_internal_organization_org_id_mssql():
        return {
            "hasMore": True,
            "data": [
                {
                    "managedId": "string",
                    "objectType": "string",
                    "name": "string",
                    "primaryClusterId": "string",
                    "isDeleted": True,
                    "isRelic": True,
                    "effectiveSlaDomainId": "string",
                    "effectiveSlaDomainName": "string",
                    "descendantCounts": {
                        "appBlueprint": 0,
                        "fileset": 0,
                        "shareFileset": 0,
                        "mssqlDatabase": 0,
                        "oracleDatabase": 0,
                        "storageArrayVolumeGroup": 0,
                        "vapp": 0,
                        "volumeGroup": 0,
                        "virtualMachine": 0
                    },
                    "locations": {
                        "folder": [
                            {
                                "managedId": "string",
                                "name": "string"
                            }
                        ],
                        "infrastructure": [
                            {
                                "managedId": "string",
                                "name": "string"
                            }
                        ],
                        "physical": [
                            {
                                "managedId": "string",
                                "name": "string"
                            }
                        ]
                    },
                    "properties": {
                        "hostname": "string",
                        "clusterName": "string",
                        "operatingSystem": "string",
                        "operatingSystemType": "string",
                        "instanceName": "string"
                    },
                    "isEffectiveSlaDomainRetentionLocked": True
                }
            ],
            "total": 1
        }

    def mock_post_internal_role_org_admin_id_authorization():
        return {
            "authorizationSpecifications": [
                {
                    "privilege": "string",
                    "resources": [
                        "string"
                    ]
                }
            ],
            "roleTemplate": "string"
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get',
                            autospec=True, spec_set=True)

    mock_get.return_value = mock_get_internal_organization_org_id_mssql()

    mock_object_id = mocker.patch('rubrik_cdm.Connect.object_id',
                                  autospec=True, spec_set=True)

    mock_object_id.side_effect = [
        "org_id", "ord_admin_role_id", "mssql_db_id"]

    mock_post = mocker.patch('rubrik_cdm.Connect.post',
                             autospec=True, spec_set=True)

    mock_post.return_value = mock_post_internal_role_org_admin_id_authorization()

    assert rubrik.add_organization_protectable_object_sql_server_db(
        "org_name", "mssql_db", "mssql_host", "mssql_instance") == mock_post_internal_role_org_admin_id_authorization()


def test_add_organization_protectable_object_sql_availability_group_idempotence(rubrik, mocker):

    def mock_get_internal_organization_org_id_mssql():
        return {
            "hasMore": True,
            "data": [
                {
                    "managedId": "ag_id",
                    "objectType": "string",
                    "name": "string",
                    "primaryClusterId": "string",
                    "isDeleted": True,
                    "isRelic": True,
                    "effectiveSlaDomainId": "string",
                    "effectiveSlaDomainName": "string",
                    "descendantCounts": {
                        "appBlueprint": 0,
                        "fileset": 0,
                        "shareFileset": 0,
                        "mssqlDatabase": 0,
                        "oracleDatabase": 0,
                        "storageArrayVolumeGroup": 0,
                        "vapp": 0,
                        "volumeGroup": 0,
                        "virtualMachine": 0
                    },
                    "locations": {
                        "folder": [
                            {
                                "managedId": "string",
                                "name": "string"
                            }
                        ],
                        "infrastructure": [
                            {
                                "managedId": "string",
                                "name": "string"
                            }
                        ],
                        "physical": [
                            {
                                "managedId": "string",
                                "name": "string"
                            }
                        ]
                    },
                    "properties": {
                        "hostname": "string",
                        "clusterName": "string",
                        "operatingSystem": "string",
                        "operatingSystemType": "string",
                        "instanceName": "string"
                    },
                    "isEffectiveSlaDomainRetentionLocked": True
                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get',
                            autospec=True, spec_set=True)

    mock_get.return_value = mock_get_internal_organization_org_id_mssql()

    mock_object_id = mocker.patch('rubrik_cdm.Connect.object_id',
                                  autospec=True, spec_set=True)

    mock_object_id.side_effect = [
        "org_id", "ord_admin_role_id", "ag_id"]

    assert rubrik.add_organization_protectable_object_sql_server_availability_group(
        "org_name", "mssql_ag") == "No change required. The MSSQL Availability Group mssql_ag is already assigned to the org_name organization."


def test_add_organization_protectable_object_sql_availability_group(rubrik, mocker):

    def mock_get_internal_organization_org_id_mssql():
        return {
            "hasMore": True,
            "data": [
                {
                    "managedId": "string",
                    "objectType": "string",
                    "name": "string",
                    "primaryClusterId": "string",
                    "isDeleted": True,
                    "isRelic": True,
                    "effectiveSlaDomainId": "string",
                    "effectiveSlaDomainName": "string",
                    "descendantCounts": {
                        "appBlueprint": 0,
                        "fileset": 0,
                        "shareFileset": 0,
                        "mssqlDatabase": 0,
                        "oracleDatabase": 0,
                        "storageArrayVolumeGroup": 0,
                        "vapp": 0,
                        "volumeGroup": 0,
                        "virtualMachine": 0
                    },
                    "locations": {
                        "folder": [
                            {
                                "managedId": "string",
                                "name": "string"
                            }
                        ],
                        "infrastructure": [
                            {
                                "managedId": "string",
                                "name": "string"
                            }
                        ],
                        "physical": [
                            {
                                "managedId": "string",
                                "name": "string"
                            }
                        ]
                    },
                    "properties": {
                        "hostname": "string",
                        "clusterName": "string",
                        "operatingSystem": "string",
                        "operatingSystemType": "string",
                        "instanceName": "string"
                    },
                    "isEffectiveSlaDomainRetentionLocked": True
                }
            ],
            "total": 1
        }

    def mock_post_internal_role_org_admin_id_authorization():
        return {
            "authorizationSpecifications": [
                {
                    "privilege": "string",
                    "resources": [
                        "string"
                    ]
                }
            ],
            "roleTemplate": "string"
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get',
                            autospec=True, spec_set=True)

    mock_get.return_value = mock_get_internal_organization_org_id_mssql()

    mock_object_id = mocker.patch('rubrik_cdm.Connect.object_id',
                                  autospec=True, spec_set=True)

    mock_object_id.side_effect = [
        "org_id", "ord_admin_role_id", "mssql_ag_id"]

    mock_post = mocker.patch('rubrik_cdm.Connect.post',
                             autospec=True, spec_set=True)

    mock_post.return_value = mock_post_internal_role_org_admin_id_authorization()

    assert rubrik.add_organization_protectable_object_sql_server_availability_group(
        "org_name", "mssql_ag") == mock_post_internal_role_org_admin_id_authorization()
