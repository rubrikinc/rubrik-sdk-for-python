import pytest
from rubrik_cdm.exceptions import InvalidParameterException, CDMVersionException
from rubrik_cdm import Connect


def test_on_demand_snapshot_invalid_object_type(rubrik):
    with pytest.raises(InvalidParameterException) as error:
        rubrik.on_demand_snapshot("object_name", "not_a_valid_object_type")

    error_message = error.value.args[0]

    assert error_message == "The on_demand_snapshot() `object_type` argument must be one of the following: ['vmware', 'physical_host', 'ahv', 'mssql_db']."


def test_on_demand_snapshot_invalid_host_os_type(rubrik):
    with pytest.raises(InvalidParameterException) as error:
        rubrik.on_demand_snapshot("object_name", "physical_host", host_os="not_a_valid_host_os")

    error_message = error.value.args[0]

    assert error_message == "The on_demand_snapshot() `host_os` argument must be one of the following: ['Linux', 'Windows']."


def test_on_demand_snapshot_vmware_current_sla(rubrik, mocker):

    def mock_get_v1_vmware_vm():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "object_name",
                    "configuredSlaDomainId": "string",
                    "configuredSlaDomainName": "string",
                    "primaryClusterId": "string",
                    "slaAssignment": "Derived",
                    "effectiveSlaDomainId": "string",
                    "effectiveSlaDomainName": "string",
                    "effectiveSlaDomainPolarisManagedId": "string",
                    "effectiveSlaSourceObjectId": "string",
                    "effectiveSlaSourceObjectName": "string",
                    "moid": "string",
                    "vcenterId": "string",
                    "hostName": "string",
                    "hostId": "string",
                    "clusterName": "string",
                    "snapshotConsistencyMandate": "UNKNOWN",
                    "powerStatus": "string",
                    "protectionDate": "2019-05-05T18:57:06.133Z",
                    "ipAddress": "string",
                    "agentStatus": {
                        "agentStatus": "string",
                        "disconnectReason": "string"
                    },
                    "toolsInstalled": True,
                    "guestOsName": "string",
                    "isReplicationEnabled": True,
                    "folderPath": [
                        {
                            "id": "string",
                            "managedId": "string",
                            "name": "string"
                        }
                    ],
                    "infraPath": [
                        {
                            "id": "string",
                            "managedId": "string",
                            "name": "string"
                        }
                    ],
                    "vmwareToolsInstalled": True,
                    "isRelic": True,
                    "guestCredentialAuthorizationStatus": "string",
                    "cloudInstantiationSpec": {
                        "imageRetentionInSeconds": 0
                    },
                    "parentAppInfo": {
                        "id": "string",
                        "isProtectedThruHierarchy": True
                    }
                }
            ],
            "total": 1
        }

    def mock_get_v1_vmware_vm_id():
        return {
            "maxNestedVsphereSnapshots": 0,
            "isVmPaused": True,
            "configuredSlaDomainId": "string",
            "snapshotConsistencyMandate": "UNKNOWN",
            "preBackupScript": {
                "scriptPath": "string",
                "timeoutMs": 0,
                "failureHandling": "abort"
            },
            "postSnapScript": {
                "scriptPath": "string",
                "timeoutMs": 0,
                "failureHandling": "abort"
            },
            "postBackupScript": {
                "scriptPath": "string",
                "timeoutMs": 0,
                "failureHandling": "abort"
            },
            "isArrayIntegrationEnabled": True,
            "cloudInstantiationSpec": {
                "imageRetentionInSeconds": 0
            },
            "throttlingSettings": {
                "ioLatencyThreshold": 0,
                "datastoreIoLatencyThreshold": 0,
                "cpuUtilizationThreshold": 0
            },
            "id": "string",
            "name": "string",
            "configuredSlaDomainName": "string",
            "primaryClusterId": "string",
            "slaAssignment": "Derived",
            "effectiveSlaDomainId": "string",
            "effectiveSlaDomainName": "string",
            "effectiveSlaDomainPolarisManagedId": "string",
            "effectiveSlaSourceObjectId": "string",
            "effectiveSlaSourceObjectName": "string",
            "moid": "string",
            "vcenterId": "string",
            "hostName": "string",
            "hostId": "string",
            "clusterName": "string",
            "powerStatus": "string",
            "protectionDate": "2019-05-05T18:57:06.257Z",
            "ipAddress": "string",
            "agentStatus": {
                "agentStatus": "string",
                "disconnectReason": "string"
            },
            "toolsInstalled": True,
            "guestOsName": "string",
            "isReplicationEnabled": True,
            "folderPath": [
                {
                    "id": "string",
                    "managedId": "string",
                    "name": "string"
                }
            ],
            "infraPath": [
                {
                    "id": "string",
                    "managedId": "string",
                    "name": "string"
                }
            ],
            "vmwareToolsInstalled": True,
            "isRelic": True,
            "guestCredentialAuthorizationStatus": "string",
            "parentAppInfo": {
                "id": "string",
                "isProtectedThruHierarchy": True
            },
            "blackoutWindowStatus": {
                "isGlobalBlackoutActive": True,
                "isSnappableBlackoutActive": True
            },
            "blackoutWindows": {
                "globalBlackoutWindows": [
                    {
                        "startTime": "string",
                        "endTime": "string"
                    }
                ],
                "snappableBlackoutWindows": [
                    {
                        "startTime": "string",
                        "endTime": "string"
                    }
                ]
            },
            "effectiveSlaDomain": {
                "id": "string",
                "primaryClusterId": "string",
                "name": "string",
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
            },
            "currentHost": {
                "id": "string",
                "name": "string",
                "configuredSlaDomainId": "string",
                "configuredSlaDomainName": "string",
                "primaryClusterId": "string",
                "datacenterId": "string",
                "computeClusterId": "string",
                "datastores": [
                    {
                        "id": "string",
                        "name": "string",
                        "capacity": 0,
                        "dataStoreType": "string",
                        "dataCenterName": "string",
                        "isLocal": True
                    }
                ],
                "effectiveSlaDomainId": "string",
                "effectiveSlaDomainName": "string",
                "effectiveSlaSourceObjectId": "string",
                "effectiveSlaSourceObjectName": "string",
                "effectiveSlaDomainPolarisManagedId": "string"
            },
            "virtualDiskIds": [
                "string"
            ],
            "snapshots": [
                {
                    "id": "string",
                    "date": "2019-05-05T18:57:06.257Z",
                    "expirationDate": "2019-05-05T18:57:06.257Z",
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
                    "vmName": "string"
                }
            ],
            "snapshotCount": 0,
            "physicalStorage": 0,
            "guestOsType": "Linux",
            "isArrayIntegrationPossible": True,
            "guestCredential": {
                "username": "string"
            },
            "isAgentRegistered": True
        }

    def mock_post_v1_vmware_vm_id_snapshot():
        return {
            "id": "string",
            "status": "string",
            "progress": 0,
            "startTime": "2019-05-05T18:57:06.298Z",
            "endTime": "2019-05-05T18:57:06.298Z",
            "nodeId": "string",
            "error": {
                "message": "string"
            },
            "links": [
                {
                    "href": "href_string",
                    "rel": "string"
                }
            ]
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_v1_vmware_vm(), mock_get_v1_vmware_vm_id()]

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_v1_vmware_vm_id_snapshot()

    assert rubrik.on_demand_snapshot(
        "object_name", "vmware", "current") == (
        mock_post_v1_vmware_vm_id_snapshot(), "href_string")


def test_on_demand_snapshot_vmware_specific_sla(rubrik, mocker):

    def mock_get_v1_vmware_vm():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "object_name",
                    "configuredSlaDomainId": "string",
                    "configuredSlaDomainName": "string",
                    "primaryClusterId": "string",
                    "slaAssignment": "Derived",
                    "effectiveSlaDomainId": "string",
                    "effectiveSlaDomainName": "string",
                    "effectiveSlaDomainPolarisManagedId": "string",
                    "effectiveSlaSourceObjectId": "string",
                    "effectiveSlaSourceObjectName": "string",
                    "moid": "string",
                    "vcenterId": "string",
                    "hostName": "string",
                    "hostId": "string",
                    "clusterName": "string",
                    "snapshotConsistencyMandate": "UNKNOWN",
                    "powerStatus": "string",
                    "protectionDate": "2019-05-05T18:57:06.133Z",
                    "ipAddress": "string",
                    "agentStatus": {
                        "agentStatus": "string",
                        "disconnectReason": "string"
                    },
                    "toolsInstalled": True,
                    "guestOsName": "string",
                    "isReplicationEnabled": True,
                    "folderPath": [
                        {
                            "id": "string",
                            "managedId": "string",
                            "name": "string"
                        }
                    ],
                    "infraPath": [
                        {
                            "id": "string",
                            "managedId": "string",
                            "name": "string"
                        }
                    ],
                    "vmwareToolsInstalled": True,
                    "isRelic": True,
                    "guestCredentialAuthorizationStatus": "string",
                    "cloudInstantiationSpec": {
                        "imageRetentionInSeconds": 0
                    },
                    "parentAppInfo": {
                        "id": "string",
                        "isProtectedThruHierarchy": True
                    }
                }
            ],
            "total": 1
        }

    def mock_get_v1_sla_domain():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "primaryClusterId": "string",
                    "name": "Gold",
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

    def mock_post_v1_vmware_vm_id_snapshot():
        return {
            "id": "string",
            "status": "string",
            "progress": 0,
            "startTime": "2019-05-05T18:57:06.298Z",
            "endTime": "2019-05-05T18:57:06.298Z",
            "nodeId": "string",
            "error": {
                "message": "string"
            },
            "links": [
                {
                    "href": "href_string",
                    "rel": "string"
                }
            ]
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_v1_vmware_vm(), mock_get_v1_sla_domain()]

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_v1_vmware_vm_id_snapshot()

    assert rubrik.on_demand_snapshot(
        "object_name", "vmware", "Gold") == (
        mock_post_v1_vmware_vm_id_snapshot(), "href_string")


def test_on_demand_snapshot_ahv_current_sla(rubrik, mocker):

    def mock_get_internal_nutanix_vm():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "object_name",
                    "configuredSlaDomainId": "string",
                    "configuredSlaDomainName": "string",
                    "primaryClusterId": "string",
                    "slaAssignment": "Derived",
                    "effectiveSlaDomainId": "string",
                    "effectiveSlaDomainName": "string",
                    "effectiveSlaDomainPolarisManagedId": "string",
                    "effectiveSlaSourceObjectId": "string",
                    "effectiveSlaSourceObjectName": "string",
                    "nutanixClusterId": "string",
                    "nutanixClusterName": "string",
                    "isRelic": True,
                    "snapshotConsistencyMandate": "Automatic",
                    "agentStatus": {
                        "agentStatus": "string",
                        "disconnectReason": "string"
                    },
                    "operatingSystemType": "AIX"
                }
            ],
            "total": 1
        }

    def mock_get_internal_nutanix_vm_id():
        return {
            "configuredSlaDomainId": "string",
            "isPaused": True,
            "snapshotConsistencyMandate": "Automatic",
            "excludedDiskIds": [
                "string"
            ],
            "id": "string",
            "name": "string",
            "configuredSlaDomainName": "string",
            "primaryClusterId": "string",
            "slaAssignment": "Derived",
            "effectiveSlaDomainId": "string",
            "effectiveSlaDomainName": "string",
            "effectiveSlaDomainPolarisManagedId": "string",
            "effectiveSlaSourceObjectId": "string",
            "effectiveSlaSourceObjectName": "string",
            "nutanixClusterId": "string",
            "nutanixClusterName": "string",
            "isRelic": True,
            "agentStatus": {
                "agentStatus": "string",
                "disconnectReason": "string"
            },
            "operatingSystemType": "AIX",
            "blackoutWindowStatus": {
                "isGlobalBlackoutActive": True,
                "isSnappableBlackoutActive": True
            },
            "blackoutWindows": {
                "globalBlackoutWindows": [
                    {
                        "startTime": "string",
                        "endTime": "string"
                    }
                ],
                "snappableBlackoutWindows": [
                    {
                        "startTime": "string",
                        "endTime": "string"
                    }
                ]
            },
            "isAgentRegistered": True
        }

    def mock_post_internal_nutanix_vm_id_snapshot():
        return {
            "id": "string",
            "status": "string",
            "progress": 0,
            "startTime": "2019-05-05T19:20:22.137Z",
            "endTime": "2019-05-05T19:20:22.137Z",
            "nodeId": "string",
            "error": {
                "message": "string"
            },
            "links": [
                {
                    "href": "href_string",
                    "rel": "string"
                }
            ]
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_internal_nutanix_vm(), mock_get_internal_nutanix_vm_id()]

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_internal_nutanix_vm_id_snapshot()

    assert rubrik.on_demand_snapshot(
        "object_name", "ahv", "current") == (
        mock_post_internal_nutanix_vm_id_snapshot(), "href_string")


def test_on_demand_snapshot_ahv_specific_sla(rubrik, mocker):

    def mock_get_internal_nutanix_vm():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "object_name",
                    "configuredSlaDomainId": "string",
                    "configuredSlaDomainName": "string",
                    "primaryClusterId": "string",
                    "slaAssignment": "Derived",
                    "effectiveSlaDomainId": "string",
                    "effectiveSlaDomainName": "string",
                    "effectiveSlaDomainPolarisManagedId": "string",
                    "effectiveSlaSourceObjectId": "string",
                    "effectiveSlaSourceObjectName": "string",
                    "nutanixClusterId": "string",
                    "nutanixClusterName": "string",
                    "isRelic": True,
                    "snapshotConsistencyMandate": "Automatic",
                    "agentStatus": {
                        "agentStatus": "string",
                        "disconnectReason": "string"
                    },
                    "operatingSystemType": "AIX"
                }
            ],
            "total": 1
        }

    def mock_get_v1_sla_domain():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "primaryClusterId": "string",
                    "name": "Gold",
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

    def mock_post_internal_nutanix_vm_id_snapshot():
        return {
            "id": "string",
            "status": "string",
            "progress": 0,
            "startTime": "2019-05-05T19:20:22.137Z",
            "endTime": "2019-05-05T19:20:22.137Z",
            "nodeId": "string",
            "error": {
                "message": "string"
            },
            "links": [
                {
                    "href": "href_string",
                    "rel": "string"
                }
            ]
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_internal_nutanix_vm(), mock_get_v1_sla_domain()]

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_internal_nutanix_vm_id_snapshot()

    assert rubrik.on_demand_snapshot(
        "object_name", "ahv", "Gold") == (
        mock_post_internal_nutanix_vm_id_snapshot(), "href_string")


def test_on_demand_snapshot_mysql_db_current_sla(rubrik, mocker):

    def mock_get_v1_host():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "sql_host",
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

    def mock_get_v1_mssql_instance():
        return {
            "hasMore": True,
            "data": [
                {
                    "logBackupFrequencyInSeconds": 0,
                    "logRetentionHours": 0,
                    "copyOnly": True,
                    "id": "string",
                    "internalTimestamp": 0,
                    "name": "sql_instance",
                    "primaryClusterId": "string",
                    "rootProperties": {
                        "rootType": "Host",
                        "rootId": "string",
                        "rootName": "string"
                    },
                    "clusterInstanceAddress": "string",
                    "protectionDate": "2019-05-05",
                    "version": "string",
                    "configuredSlaDomainId": "string",
                    "configuredSlaDomainName": "string",
                    "unprotectableReasons": [
                        {
                            "unprotectableType": "InsufficientPermissions",
                            "message": "string"
                        }
                    ]
                }
            ],
            "total": 1
        }

    def mock_get_v1_mysql_db():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "sql_db",
                    "configuredSlaDomainId": "string",
                    "configuredSlaDomainName": "string",
                    "primaryClusterId": "string",
                    "slaAssignment": "Derived",
                    "effectiveSlaDomainId": "string",
                    "effectiveSlaDomainName": "string",
                    "effectiveSlaDomainPolarisManagedId": "string",
                    "effectiveSlaSourceObjectId": "string",
                    "effectiveSlaSourceObjectName": "string",
                    "rootProperties": {
                        "rootType": "Host",
                        "rootId": "string",
                        "rootName": "string"
                    },
                    "instanceId": "string",
                    "instanceName": "string",
                    "isRelic": True,
                    "copyOnly": True,
                    "logBackupFrequencyInSeconds": 0,
                    "logBackupRetentionHours": 0,
                    "isLiveMount": True,
                    "isLogShippingSecondary": True,
                    "recoveryModel": "SIMPLE",
                    "state": "string",
                    "hasPermissions": True,
                    "isInAvailabilityGroup": True,
                    "replicas": [
                        {
                            "instanceId": "string",
                            "instanceName": "string",
                            "recoveryModel": "SIMPLE",
                            "state": "string",
                            "hasPermissions": True,
                            "isStandby": True,
                            "recoveryForkGuid": "string",
                            "isArchived": True,
                            "isDeleted": True,
                            "availabilityInfo": {
                                "role": "PRIMARY"
                            },
                            "rootProperties": {
                                "rootType": "Host",
                                "rootId": "string",
                                "rootName": "string"
                            }
                        }
                    ],
                    "availabilityGroupId": "string",
                    "unprotectableReasons": [
                        {
                            "unprotectableType": "InsufficientPermissions",
                            "message": "string"
                        }
                    ]
                }
            ],
            "total": 1
        }

    def mock_get_v1_mysql_db_id():
        return {
            "id": "string",
            "name": "string",
            "configuredSlaDomainId": "string",
            "configuredSlaDomainName": "string",
            "primaryClusterId": "string",
            "slaAssignment": "Derived",
            "effectiveSlaDomainId": "string",
            "effectiveSlaDomainName": "string",
            "effectiveSlaDomainPolarisManagedId": "string",
            "effectiveSlaSourceObjectId": "string",
            "effectiveSlaSourceObjectName": "string",
            "rootProperties": {
                "rootType": "Host",
                "rootId": "string",
                "rootName": "string"
            },
            "instanceId": "string",
            "instanceName": "string",
            "isRelic": True,
            "copyOnly": True,
            "logBackupFrequencyInSeconds": 0,
            "logBackupRetentionHours": 0,
            "isLiveMount": True,
            "isLogShippingSecondary": True,
            "recoveryModel": "SIMPLE",
            "state": "string",
            "hasPermissions": True,
            "isInAvailabilityGroup": True,
            "replicas": [
                {
                    "instanceId": "string",
                    "instanceName": "string",
                    "recoveryModel": "SIMPLE",
                    "state": "string",
                    "hasPermissions": True,
                    "isStandby": True,
                    "recoveryForkGuid": "string",
                    "isArchived": True,
                    "isDeleted": True,
                    "availabilityInfo": {
                        "role": "PRIMARY"
                    },
                    "rootProperties": {
                        "rootType": "Host",
                        "rootId": "string",
                        "rootName": "string"
                    }
                }
            ],
            "availabilityGroupId": "string",
            "unprotectableReasons": [
                {
                    "unprotectableType": "InsufficientPermissions",
                    "message": "string"
                }
            ],
            "snapshotCount": 0,
            "isLocal": True,
            "isStandby": True,
            "latestRecoveryPoint": "2019-05-05",
            "oldestRecoveryPoint": "2019-05-05",
            "protectionDate": "2019-05-05",
            "recoveryForkGuid": "string",
            "maxDataStreams": 0,
            "localStorage": 0,
            "archiveStorage": 0,
            "preBackupScript": {
                "scriptPath": "string",
                "timeoutMs": 0,
                "scriptErrorAction": "abort"
            },
            "postBackupScript": {
                "scriptPath": "string",
                "timeoutMs": 0,
                "scriptErrorAction": "abort"
            }
        }

    def mock_post_v1_mysql_db_snapshot():
        return {
            "id": "string",
            "status": "string",
            "progress": 0,
            "startTime": "2019-05-05T18:57:06.003Z",
            "endTime": "2019-05-05T18:57:06.003Z",
            "nodeId": "string",
            "error": {
                "message": "string"
            },
            "links": [
                {
                    "href": "href_string",
                    "rel": "string"
                }
            ]
        }

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = "5.0"

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [
        mock_get_v1_host(),
        mock_get_v1_mssql_instance(),
        mock_get_v1_mysql_db(),
        mock_get_v1_mysql_db_id()]

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_v1_mysql_db_snapshot()

    assert rubrik.on_demand_snapshot("object_name", "mssql_db", sql_host="sql_host", sql_instance="sql_instance", sql_db="sql_db") == \
        (mock_post_v1_mysql_db_snapshot(), "href_string")


def test_on_demand_snapshot_mysql_db_specific_sla(rubrik, mocker):

    def mock_get_v1_host():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "sql_host",
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

    def mock_get_v1_mssql_instance():
        return {
            "hasMore": True,
            "data": [
                {
                    "logBackupFrequencyInSeconds": 0,
                    "logRetentionHours": 0,
                    "copyOnly": True,
                    "id": "string",
                    "internalTimestamp": 0,
                    "name": "sql_instance",
                    "primaryClusterId": "string",
                    "rootProperties": {
                        "rootType": "Host",
                        "rootId": "string",
                        "rootName": "string"
                    },
                    "clusterInstanceAddress": "string",
                    "protectionDate": "2019-05-05",
                    "version": "string",
                    "configuredSlaDomainId": "string",
                    "configuredSlaDomainName": "string",
                    "unprotectableReasons": [
                        {
                            "unprotectableType": "InsufficientPermissions",
                            "message": "string"
                        }
                    ]
                }
            ],
            "total": 1
        }

    def mock_get_v1_mysql_db():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "sql_db",
                    "configuredSlaDomainId": "string",
                    "configuredSlaDomainName": "string",
                    "primaryClusterId": "string",
                    "slaAssignment": "Derived",
                    "effectiveSlaDomainId": "string",
                    "effectiveSlaDomainName": "string",
                    "effectiveSlaDomainPolarisManagedId": "string",
                    "effectiveSlaSourceObjectId": "string",
                    "effectiveSlaSourceObjectName": "string",
                    "rootProperties": {
                        "rootType": "Host",
                        "rootId": "string",
                        "rootName": "string"
                    },
                    "instanceId": "string",
                    "instanceName": "string",
                    "isRelic": True,
                    "copyOnly": True,
                    "logBackupFrequencyInSeconds": 0,
                    "logBackupRetentionHours": 0,
                    "isLiveMount": True,
                    "isLogShippingSecondary": True,
                    "recoveryModel": "SIMPLE",
                    "state": "string",
                    "hasPermissions": True,
                    "isInAvailabilityGroup": True,
                    "replicas": [
                        {
                            "instanceId": "string",
                            "instanceName": "string",
                            "recoveryModel": "SIMPLE",
                            "state": "string",
                            "hasPermissions": True,
                            "isStandby": True,
                            "recoveryForkGuid": "string",
                            "isArchived": True,
                            "isDeleted": True,
                            "availabilityInfo": {
                                "role": "PRIMARY"
                            },
                            "rootProperties": {
                                "rootType": "Host",
                                "rootId": "string",
                                "rootName": "string"
                            }
                        }
                    ],
                    "availabilityGroupId": "string",
                    "unprotectableReasons": [
                        {
                            "unprotectableType": "InsufficientPermissions",
                            "message": "string"
                        }
                    ]
                }
            ],
            "total": 1
        }

    def mock_get_v1_sla_domain():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "primaryClusterId": "string",
                    "name": "Gold",
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

    def mock_post_v1_mysql_db_snapshot():
        return {
            "id": "string",
            "status": "string",
            "progress": 0,
            "startTime": "2019-05-05T18:57:06.003Z",
            "endTime": "2019-05-05T18:57:06.003Z",
            "nodeId": "string",
            "error": {
                "message": "string"
            },
            "links": [
                {
                    "href": "href_string",
                    "rel": "string"
                }
            ]
        }

    def mock_get_v1_sla_domain():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "primaryClusterId": "string",
                    "name": "Gold",
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

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = "5.0"

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [
        mock_get_v1_host(),
        mock_get_v1_mssql_instance(),
        mock_get_v1_mysql_db(),
        mock_get_v1_sla_domain(),
        mock_get_v1_sla_domain()]

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_v1_mysql_db_snapshot()

    assert rubrik.on_demand_snapshot("object_name", "mssql_db", "Gold", sql_host="sql_host", sql_instance="sql_instance", sql_db="sql_db") == \
        (mock_post_v1_mysql_db_snapshot(), "href_string")


def test_on_demand_snapshot_physical_host_host_os_not_populated(rubrik, mocker):
    with pytest.raises(InvalidParameterException) as error:
        rubrik.on_demand_snapshot("object_name", "physical_host")

    error_message = error.value.args[0]

    assert error_message == "The on_demand_snapshot() `host_os` argument must be populated when taking a Physical host snapshot."


def test_on_demand_snapshot_physical_host_fileset_not_populated(rubrik, mocker):
    with pytest.raises(InvalidParameterException) as error:
        rubrik.on_demand_snapshot("object_name", "physical_host", host_os="Linux")

    error_message = error.value.args[0]

    assert error_message == "The on_demand_snapshot() `fileset` argument must be populated when taking a Physical host snapshot."


def test_on_demand_snapshot_physical_host_invalid_fileset(rubrik, mocker):

    def mock_get_v1_host():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "object_name",
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

    def mock_get_v1_fileset_template():
        return {
            "hasMore": True,
            "data": [
                {
                    "allowBackupNetworkMounts": True,
                    "allowBackupHiddenFoldersInNetworkMounts": True,
                    "useWindowsVss": True,
                    "name": "fileset",
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

    def mock_get_v1_fileset():
        return {
            "hasMore": True,
            "data": [
                {
                    "allowBackupNetworkMounts": True,
                    "allowBackupHiddenFoldersInNetworkMounts": True,
                    "useWindowsVss": True,
                    "id": "string",
                    "name": "fileset",
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
            "total": 0
        }

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = "5.0"

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [
        mock_get_v1_host(),
        mock_get_v1_fileset_template(),
        mock_get_v1_fileset()]

    with pytest.raises(InvalidParameterException) as error:
        rubrik.on_demand_snapshot("object_name", "physical_host", host_os="Linux", fileset="fileset")

    error_message = error.value.args[0]

    assert error_message == "The Physical Host 'object_name' is not assigned to the 'fileset' Fileset."


def test_on_demand_snapshot_physical_host_current_sla(rubrik, mocker):

    def mock_get_v1_host():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "object_name",
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

    def mock_get_v1_fileset_template():
        return {
            "hasMore": True,
            "data": [
                {
                    "allowBackupNetworkMounts": True,
                    "allowBackupHiddenFoldersInNetworkMounts": True,
                    "useWindowsVss": True,
                    "name": "fileset",
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

    def mock_get_v1_fileset():
        return {
            "hasMore": True,
            "data": [
                {
                    "allowBackupNetworkMounts": True,
                    "allowBackupHiddenFoldersInNetworkMounts": True,
                    "useWindowsVss": True,
                    "id": "string",
                    "name": "fileset",
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

    def mock_post_v1_fileset_id_snapshot():
        return {
            "id": "string",
            "status": "string",
            "progress": 0,
            "startTime": "2019-05-05T18:57:06.003Z",
            "endTime": "2019-05-05T18:57:06.003Z",
            "nodeId": "string",
            "error": {
                "message": "string"
            },
            "links": [
                {
                    "href": "href_string",
                    "rel": "string"
                }
            ]
        }

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = "5.0"

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [
        mock_get_v1_host(),
        mock_get_v1_fileset_template(),
        mock_get_v1_fileset()]

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_v1_fileset_id_snapshot()

    assert rubrik.on_demand_snapshot("object_name", "physical_host", host_os="Linux", fileset="fileset") == \
        (mock_post_v1_fileset_id_snapshot(), "href_string")

def test_on_demand_snapshot_physical_host_specific_sla(rubrik, mocker):

    def mock_get_v1_host():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "object_name",
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

    def mock_get_v1_fileset_template():
        return {
            "hasMore": True,
            "data": [
                {
                    "allowBackupNetworkMounts": True,
                    "allowBackupHiddenFoldersInNetworkMounts": True,
                    "useWindowsVss": True,
                    "name": "fileset",
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

    def mock_get_v1_fileset():
        return {
            "hasMore": True,
            "data": [
                {
                    "allowBackupNetworkMounts": True,
                    "allowBackupHiddenFoldersInNetworkMounts": True,
                    "useWindowsVss": True,
                    "id": "string",
                    "name": "fileset",
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

    def mock_post_v1_fileset_id_snapshot():
        return {
            "id": "string",
            "status": "string",
            "progress": 0,
            "startTime": "2019-05-05T18:57:06.003Z",
            "endTime": "2019-05-05T18:57:06.003Z",
            "nodeId": "string",
            "error": {
                "message": "string"
            },
            "links": [
                {
                    "href": "href_string",
                    "rel": "string"
                }
            ]
        }

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = "5.0"

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [
        mock_get_v1_host(),
        mock_get_v1_fileset_template(),
        mock_get_v1_fileset()]

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_v1_fileset_id_snapshot()

    assert rubrik.on_demand_snapshot("object_name", "physical_host", host_os="Linux", fileset="fileset") == \
        (mock_post_v1_fileset_id_snapshot(), "href_string")