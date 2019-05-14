import pytest
from rubrik_cdm.exceptions import InvalidParameterException, CDMVersionException, InvalidTypeException
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


def test_object_id_invalid_object_type(rubrik):
    with pytest.raises(InvalidParameterException) as error:
        rubrik.object_id("object_name", "not_a_valid_object_type")

    error_message = error.value.args[0]

    assert error_message == "The object_id() object_type argument must be one of the following: ['vmware', 'sla', 'vmware_host', 'physical_host', 'fileset_template', 'managed_volume', 'mssql_db', 'mssql_instance', 'vcenter', 'ahv', 'aws_native']."


def test_object_id_invalid_fileset_template(rubrik):
    with pytest.raises(InvalidParameterException) as error:
        rubrik.object_id("object_name", "fileset_template")

    error_message = error.value.args[0]

    assert error_message == "You must provide the Fileset Tempalte OS type."


def test_object_id_invalid_fileset_template_type(rubrik):
    with pytest.raises(InvalidParameterException) as error:
        rubrik.object_id("object_name", "fileset_template", host_os="not_a_valid_host_os")

    error_message = error.value.args[0]

    assert error_message == "The host_os must be either 'Linux' or 'Windows'."


@pytest.mark.parametrize('sla_name', ["forever", "unprotected"])
def test_object_id_sla_forever_or_unprotected(rubrik, sla_name):

    assert rubrik.object_id(sla_name, "sla") == "UNPROTECTED"


def test_object_id_not_found(rubrik, mocker):

    def mock_get_v1_vmware_vm():
        return {
            "hasMore": True,
            "data": [
                {
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
                    "moid": "string",
                    "vcenterId": "string",
                    "hostName": "string",
                    "hostId": "string",
                    "clusterName": "string",
                    "snapshotConsistencyMandate": "UNKNOWN",
                    "powerStatus": "string",
                    "protectionDate": "2019-05-06T04:23:38.418Z",
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
            "total": 0
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_vmware_vm()

    with pytest.raises(InvalidParameterException) as error:
        rubrik.object_id("object_name", "vmware")

    error_message = error.value.args[0]

    assert error_message == "The vmware object 'object_name' was not found on the Rubrik cluster."


def test_object_id_not_in_object_ids_list(rubrik, mocker):

    def mock_get_v1_vmware_vm():
        return {
            "hasMore": True,
            "data": [
                {
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
                    "moid": "string",
                    "vcenterId": "string",
                    "hostName": "string",
                    "hostId": "string",
                    "clusterName": "string",
                    "snapshotConsistencyMandate": "UNKNOWN",
                    "powerStatus": "string",
                    "protectionDate": "2019-05-06T04:23:38.418Z",
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

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_vmware_vm()

    with pytest.raises(InvalidParameterException) as error:
        rubrik.object_id("object_name", "vmware")

    error_message = error.value.args[0]

    assert error_message == "The vmware object 'object_name' was not found on the Rubrik cluster."


def test_object_id_multiple_objects_found(rubrik, mocker):

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
                    "protectionDate": "2019-05-06T04:23:38.418Z",
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
                },
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
                    "protectionDate": "2019-05-06T04:23:38.418Z",
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
            "total": 2
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_vmware_vm()

    with pytest.raises(InvalidParameterException) as error:
        rubrik.object_id("object_name", "vmware")

    error_message = error.value.args[0]

    assert error_message == "Multiple vmware objects named 'object_name' were found on the Rubrik cluster. Unable to return a specific object id."


def test_object_id_vmware(rubrik, mocker):

    def mock_get_v1_vmware_vm():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_id",
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
                    "moid": "string",
                    "vcenterId": "string",
                    "hostName": "string",
                    "hostId": "string",
                    "clusterName": "string",
                    "snapshotConsistencyMandate": "UNKNOWN",
                    "powerStatus": "string",
                    "protectionDate": "2019-05-06T04:23:38.418Z",
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

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_vmware_vm()

    assert rubrik.object_id("string", "vmware") == "string_id"


def test_object_id_sla(rubrik, mocker):

    def mock_get_v1_sla_domain():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_id",
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
                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_sla_domain()

    assert rubrik.object_id("string", "sla") == "string_id"


def test_object_id_vmware_host(rubrik, mocker):

    def mock_get_v1_vmware_host():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_id",
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
                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_vmware_host()

    assert rubrik.object_id("string", "vmware_host") == "string_id"


def test_object_id_fileset_template(rubrik, mocker):

    def mock_get_v1_fileset_template():
        return {
            "hasMore": True,
            "data": [
                {
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
                    "id": "string_id",
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

    assert rubrik.object_id("string", "fileset_template", host_os="Linux") == "string_id"


def test_object_id_managed_volume(rubrik, mocker):

    def mock_get_internal_managed_volume():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_id",
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
                    "snapshotCount": 0,
                    "pendingSnapshotCount": 0,
                    "isRelic": True,
                    "applicationTag": "Oracle",
                    "numChannels": 0,
                    "volumeSize": 0,
                    "usedSize": 0,
                    "state": "ExportRequested",
                    "hostPatterns": [
                        "string"
                    ],
                    "mainExport": {
                        "isActive": True,
                        "channels": [
                            {
                                "ipAddress": "string",
                                "mountPoint": "string"
                            }
                        ],
                        "config": {
                            "hostPatterns": [
                                "string"
                            ],
                            "nodeHint": [
                                "string"
                            ],
                            "smbDomainName": "string",
                            "smbValidUsers": [
                                "string"
                            ],
                            "smbValidIps": [
                                "string"
                            ],
                            "subnet": "string",
                            "shareType": "NFS"
                        }
                    },
                    "isWritable": True,
                    "links": [
                        {
                            "href": "string",
                            "rel": "string"
                        }
                    ],
                    "isDeleted": True,
                    "shareType": "NFS",
                    "smbDomainName": "string",
                    "smbValidUsers": [
                        "string"
                    ],
                    "smbValidIps": [
                        "string"
                    ]
                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_managed_volume()

    assert rubrik.object_id("string", "managed_volume") == "string_id"


def test_object_id_ahv(rubrik, mocker):

    def mock_get_internal_nutanix_vm():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_id",
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

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_nutanix_vm()

    assert rubrik.object_id("string", "ahv") == "string_id"


def test_object_id_mssql_db(rubrik, mocker):

    def mock_get_v1_mssql_db():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_id",
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
                    ]
                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_mssql_db()

    assert rubrik.object_id("string", "mssql_db") == "string_id"


def test_object_id_mssql_instance(rubrik, mocker):

    def mock_get_v1_mssql_instance():
        return {
            "hasMore": True,
            "data": [
                {
                    "logBackupFrequencyInSeconds": 0,
                    "logRetentionHours": 0,
                    "copyOnly": True,
                    "id": "string_id",
                    "internalTimestamp": 0,
                    "name": "string",
                    "primaryClusterId": "string",
                    "rootProperties": {
                        "rootType": "Host",
                        "rootId": "string",
                        "rootName": "string"
                    },
                    "clusterInstanceAddress": "string",
                    "protectionDate": "2019-05-06",
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

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_mssql_instance()

    assert rubrik.object_id("string", "mssql_instance") == "string_id"


def test_object_id_aws_native(rubrik, mocker):

    def mock_get_internal_aws_account():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_id",
                    "name": "string",
                    "primaryClusterId": "string",
                    "status": "Connected"
                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_aws_account()

    assert rubrik.object_id("string", "aws_native") == "string_id"


def test_object_id_vcenter(rubrik, mocker):

    def mock_get_v1_vmware_vcenter():
        return {
            "hasMore": True,
            "data": [
                {
                    "caCerts": "string",
                    "configuredSlaDomainId": "string",
                    "id": "string_id",
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

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_vmware_vcenter()

    assert rubrik.object_id("string", "vcenter") == "string_id"


def test_object_id_physical_host_cdm_4_x(rubrik, mocker):

    def mock_get_v1_host():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_id",
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

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = "4.0"

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_host()

    assert rubrik.object_id("string", "physical_host") == "string_id"


def test_object_id_physical_host_cdm_5_x(rubrik, mocker):

    def mock_get_v1_host():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_id",
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

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = "5.0"

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_host()

    assert rubrik.object_id("string", "physical_host") == "string_id"


def test_assign_sla_invalid_object_type(rubrik):
    with pytest.raises(InvalidParameterException) as error:
        rubrik.assign_sla("object_name", "sla_name", "not_a_valid_object_type")

    error_message = error.value.args[0]

    assert error_message == "The assign_sla() object_type argument must be one of the following: ['vmware', 'mssql_host']."


def test_assign_sla_idempotence_specific_sla(rubrik, mocker):

    def mock_get_v1_sla_domain():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_sla_id",
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

    def mock_get_v1_vmware_vm():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_id",
                    "name": "object_name",
                    "configuredSlaDomainId": "string_sla_id",
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
            "configuredSlaDomainId": "string_sla_id",
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

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_v1_sla_domain(), mock_get_v1_vmware_vm(), mock_get_v1_vmware_vm_id()]
    assert rubrik.assign_sla("object_name", "Gold", "vmware") == \
        "No change required. The vSphere VM 'object_name' is already assigned to the 'Gold' SLA Domain."


def test_assign_sla_idempotence_do_not_protect_sla(rubrik, mocker):

    def mock_get_v1_vmware_vm():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_id",
                    "name": "object_name",
                    "configuredSlaDomainId": "string_sla_id",
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
            "configuredSlaDomainId": "UNPROTECTED",
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

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_v1_vmware_vm(), mock_get_v1_vmware_vm_id()]
    assert rubrik.assign_sla("object_name", "do not protect", "vmware") == \
        "No change required. The vSphere VM 'object_name' is already assigned to the 'do not protect' SLA Domain."


def test_assign_sla_idempotence_clear_sla(rubrik, mocker):

    def mock_get_v1_vmware_vm():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_id",
                    "name": "object_name",
                    "configuredSlaDomainId": "string_sla_id",
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
            "configuredSlaDomainId": "INHERIT",
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

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_v1_vmware_vm(), mock_get_v1_vmware_vm_id()]
    assert rubrik.assign_sla("object_name", "clear", "vmware") == \
        "No change required. The vSphere VM 'object_name' is already assigned to the 'clear' SLA Domain."


def test_assign_sla(rubrik, mocker):

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

    def mock_get_v1_vmware_vm():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_id",
                    "name": "object_name",
                    "configuredSlaDomainId": "string_sla_id",
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
            "configuredSlaDomainId": "string_sla_id",
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

    def mock_post_internal_sla_domain_id_assign():
        return {"status_code": "204"}

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_v1_sla_domain(), mock_get_v1_vmware_vm(), mock_get_v1_vmware_vm_id()]

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_internal_sla_domain_id_assign()

    assert rubrik.assign_sla("object_name", "Gold", "vmware") == mock_post_internal_sla_domain_id_assign()


def test_vsphere_live_mount_invalid_remove_network_devices(rubrik):
    with pytest.raises(InvalidTypeException) as error:
        rubrik.vsphere_live_mount("vm_name", remove_network_devices="not_a_valid_remove_network_devices")

    error_message = error.value.args[0]

    assert error_message == "The 'remove_network_devices' argument must be True or False."


def test_vsphere_live_mount_invalid_power_on(rubrik):
    with pytest.raises(InvalidTypeException) as error:
        rubrik.vsphere_live_mount("vm_name", power_on="not_a_valid_remove_network_devices")

    error_message = error.value.args[0]

    assert error_message == "The 'power_on' argument must be True or False."


def test_vsphere_live_mount_time_not_latest(rubrik):
    with pytest.raises(InvalidParameterException) as error:
        rubrik.vsphere_live_mount("vm_name", time="not_latest")

    error_message = error.value.args[0]

    assert error_message == "The date and time arguments most both be 'latest' or a specific date and time."


def test_vsphere_live_mount_date_not_latest(rubrik):
    with pytest.raises(InvalidParameterException) as error:
        rubrik.vsphere_live_mount("vm_name", date="not_latest")

    error_message = error.value.args[0]

    assert error_message == "The date and time arguments most both be 'latest' or a specific date and time."


def test_vsphere_live_mount_latest(rubrik, mocker):

    def mock_get_v1_vmware_vm():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "vm_name",
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

    def mock_post_v1_vmware_vm_snapshot_id_mount():
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
    mock_post.return_value = mock_post_v1_vmware_vm_snapshot_id_mount()

    assert rubrik.vsphere_live_mount("vm_name") == mock_post_v1_vmware_vm_snapshot_id_mount()


def test_vsphere_live_mount_specific_date_time(rubrik, mocker):

    def mock_get_v1_vmware_vm():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "vm_name",
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
                    "date": "2014-01-15T09:30:06.257Z",
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

    def mock_post_v1_vmware_vm_snapshot_id_mount():
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

    mock__date_time_conversion = mocker.patch('rubrik_cdm.Connect._date_time_conversion', autospec=True, spec_set=True)
    mock__date_time_conversion.return_value = "2014-01-15T09:30"

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_v1_vmware_vm_snapshot_id_mount()

    assert rubrik.vsphere_live_mount(
        "vm_name",
        date="1-15-2014",
        time="1:30 AM") == mock_post_v1_vmware_vm_snapshot_id_mount()


def test_vsphere_live_mount_specific_host(rubrik, mocker):

    def mock_get_v1_vmware_vm():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "vm_name",
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
                    "date": "2014-01-15T09:30:06.257Z",
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

    def mock_get_v1_vmware_host():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_id",
                    "name": "host",
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
                }
            ],
            "total": 1
        }

    def mock_post_v1_vmware_vm_snapshot_id_mount():
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
    mock_get.side_effect = [mock_get_v1_vmware_vm(), mock_get_v1_vmware_vm_id(), mock_get_v1_vmware_host()]

    mock__date_time_conversion = mocker.patch('rubrik_cdm.Connect._date_time_conversion', autospec=True, spec_set=True)
    mock__date_time_conversion.return_value = "2014-01-15T09:30"

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_v1_vmware_vm_snapshot_id_mount()

    assert rubrik.vsphere_live_mount("vm_name", date="1-15-2014", time="1:30 AM",
                                     host="host") == mock_post_v1_vmware_vm_snapshot_id_mount()


def test_vsphere_instant_recovery_invalid_remove_network_devices(rubrik):
    with pytest.raises(InvalidTypeException) as error:
        rubrik.vsphere_instant_recovery("vm_name", remove_network_devices="not_a_valid_remove_network_devices")

    error_message = error.value.args[0]

    assert error_message == "The 'remove_network_devices' argument must be True or False."


def test_vsphere_instant_recovery_invalid_power_on(rubrik):
    with pytest.raises(InvalidTypeException) as error:
        rubrik.vsphere_instant_recovery("vm_name", power_on="not_a_valid_remove_network_devices")

    error_message = error.value.args[0]

    assert error_message == "The 'power_on' argument must be True or False."


def test_vsphere_instant_recovery_invalid_disable_network(rubrik):
    with pytest.raises(InvalidTypeException) as error:
        rubrik.vsphere_instant_recovery("vm_name", disable_network="not_a_valid_disable_network")

    error_message = error.value.args[0]

    assert error_message == "The 'disable_network' argument must be True or False."


def test_vsphere_instant_recovery_invalid_keep_mac_addresses(rubrik):
    with pytest.raises(InvalidTypeException) as error:
        rubrik.vsphere_instant_recovery("vm_name", keep_mac_addresses="not_a_valid_keep_mac_addresses")

    error_message = error.value.args[0]

    assert error_message == "The 'keep_mac_addresses' argument must be True or False."


def test_vsphere_instant_recovery_invalid_preserve_moid(rubrik):
    with pytest.raises(InvalidTypeException) as error:
        rubrik.vsphere_instant_recovery("vm_name", preserve_moid="not_a_valid_preserve_moid")

    error_message = error.value.args[0]

    assert error_message == "The 'preserve_moid' argument must be True or False."


def test_vsphere_instant_recovery_time_not_latest(rubrik):
    with pytest.raises(InvalidParameterException) as error:
        rubrik.vsphere_instant_recovery("vm_name", time="not_latest")

    error_message = error.value.args[0]

    assert error_message == "The date and time arguments most both be 'latest' or a specific date and time."


def test_vsphere_instant_recovery_date_not_latest(rubrik):
    with pytest.raises(InvalidParameterException) as error:
        rubrik.vsphere_instant_recovery("vm_name", date="not_latest")

    error_message = error.value.args[0]

    assert error_message == "The date and time arguments most both be 'latest' or a specific date and time."


def test_vsphere_instant_recovery_latest(rubrik, mocker):

    def mock_get_v1_vmware_vm():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "vm_name",
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

    def mock_post_v1_vmware_vm_snapshot_id_instant_recover():
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
    mock_post.return_value = mock_post_v1_vmware_vm_snapshot_id_instant_recover()

    assert rubrik.vsphere_live_mount("vm_name") == mock_post_v1_vmware_vm_snapshot_id_instant_recover()


def test_vsphere_instant_recovery_specific_date_time(rubrik, mocker):

    def mock_get_v1_vmware_vm():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "vm_name",
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
                    "date": "2014-01-15T09:30:06.257Z",
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

    def mock_post_v1_vmware_vm_snapshot_id_instant_recover():
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

    mock__date_time_conversion = mocker.patch('rubrik_cdm.Connect._date_time_conversion', autospec=True, spec_set=True)
    mock__date_time_conversion.return_value = "2014-01-15T09:30"

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_v1_vmware_vm_snapshot_id_instant_recover()

    assert rubrik.vsphere_live_mount(
        "vm_name",
        date="1-15-2014",
        time="1:30 AM") == mock_post_v1_vmware_vm_snapshot_id_instant_recover()


def test_vsphere_instant_recovery_specific_host(rubrik, mocker):

    def mock_get_v1_vmware_vm():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "vm_name",
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
                    "date": "2014-01-15T09:30:06.257Z",
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

    def mock_get_v1_vmware_host():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_id",
                    "name": "host",
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
                }
            ],
            "total": 1
        }

    def mock_post_v1_vmware_vm_snapshot_id_instant_recover():
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
    mock_get.side_effect = [mock_get_v1_vmware_vm(), mock_get_v1_vmware_vm_id(), mock_get_v1_vmware_host()]

    mock__date_time_conversion = mocker.patch('rubrik_cdm.Connect._date_time_conversion', autospec=True, spec_set=True)
    mock__date_time_conversion.return_value = "2014-01-15T09:30"

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_v1_vmware_vm_snapshot_id_instant_recover()

    assert rubrik.vsphere_live_mount("vm_name", date="1-15-2014", time="1:30 AM",
                                     host="host") == mock_post_v1_vmware_vm_snapshot_id_instant_recover()


def test__date_time_conversion(rubrik, mocker):

    def mock_get_v1_cluster_me():
        return {
            "id": "string",
            "version": "string",
            "apiVersion": "string",
            "name": "string",
            "timezone": {
                "timezone": "America/Los_Angeles"
            },
            "geolocation": {
                "address": "string"
            },
            "acceptedEulaVersion": "string",
            "latestEulaVersion": "string"
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_v1_cluster_me()

    assert rubrik._date_time_conversion("1-15-2014", "1:30 AM") == "2014-01-15T09:30"


def test_pause_snapshots_invalid_object_type(rubrik):
    with pytest.raises(InvalidParameterException) as error:
        rubrik.pause_snapshots("object_name", "not_a_valid_object_type")

    error_message = error.value.args[0]

    assert error_message == "The pause_snapshots() object_type argument must be one of the following: ['vmware']."


def test_pause_snapshots_idempotence(rubrik, mocker):

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

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_v1_vmware_vm(), mock_get_v1_vmware_vm_id()]

    assert rubrik.pause_snapshots("object_name",
                                  "vmware") == "No change required. The vmware VM 'object_name' is already paused."


def test_pause_snapshots(rubrik, mocker):

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
                "isSnappableBlackoutActive": False
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

    def mock_patch_v1_vmware_vm_id():

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
            "protectionDate": "2019-05-07T00:23:08.144Z",
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
                    "date": "2019-05-07T00:23:08.146Z",
                    "expirationDate": "2019-05-07T00:23:08.146Z",
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

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_v1_vmware_vm(), mock_get_v1_vmware_vm_id()]

    mock_patch = mocker.patch('rubrik_cdm.Connect.patch', autospec=True, spec_set=True)
    mock_patch.return_value = mock_patch_v1_vmware_vm_id()

    assert rubrik.pause_snapshots("object_name", "vmware") == mock_patch_v1_vmware_vm_id()


def test_resume_snapshots_invalid_object_type(rubrik):
    with pytest.raises(InvalidParameterException) as error:
        rubrik.resume_snapshots("object_name", "not_a_valid_object_type")

    error_message = error.value.args[0]

    assert error_message == "The resume_snapshots() object_type argument must be one of the following: ['vmware']."


def test_resume_snapshots_idempotence(rubrik, mocker):

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
                "isSnappableBlackoutActive": False
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

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_v1_vmware_vm(), mock_get_v1_vmware_vm_id()]

    assert rubrik.resume_snapshots(
        "object_name",
        "vmware") == "No change required. The 'vmware' object 'object_name' is currently not paused."


def test_resume_snapshots(rubrik, mocker):
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

    def mock_patch_v1_vmware_vm_id():

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
            "protectionDate": "2019-05-07T00:23:08.144Z",
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
                    "date": "2019-05-07T00:23:08.146Z",
                    "expirationDate": "2019-05-07T00:23:08.146Z",
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

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_v1_vmware_vm(), mock_get_v1_vmware_vm_id()]

    mock_patch = mocker.patch('rubrik_cdm.Connect.patch', autospec=True, spec_set=True)
    mock_patch.return_value = mock_patch_v1_vmware_vm_id()

    assert rubrik.resume_snapshots("object_name", "vmware") == mock_patch_v1_vmware_vm_id()


def test_begin_managed_volume_snapshot_idempotence(rubrik, mocker):

    def mock_get_internal_managed_volume():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_id",
                    "name": "name",
                    "configuredSlaDomainId": "string",
                    "configuredSlaDomainName": "string",
                    "primaryClusterId": "string",
                    "slaAssignment": "Derived",
                    "effectiveSlaDomainId": "string",
                    "effectiveSlaDomainName": "string",
                    "effectiveSlaDomainPolarisManagedId": "string",
                    "effectiveSlaSourceObjectId": "string",
                    "effectiveSlaSourceObjectName": "string",
                    "snapshotCount": 0,
                    "pendingSnapshotCount": 0,
                    "isRelic": True,
                    "applicationTag": "Oracle",
                    "numChannels": 0,
                    "volumeSize": 0,
                    "usedSize": 0,
                    "state": "ExportRequested",
                    "hostPatterns": [
                        "string"
                    ],
                    "mainExport": {
                        "isActive": True,
                        "channels": [
                            {
                                "ipAddress": "string",
                                "mountPoint": "string"
                            }
                        ],
                        "config": {
                            "hostPatterns": [
                                "string"
                            ],
                            "nodeHint": [
                                "string"
                            ],
                            "smbDomainName": "string",
                            "smbValidUsers": [
                                "string"
                            ],
                            "smbValidIps": [
                                "string"
                            ],
                            "subnet": "string",
                            "shareType": "NFS"
                        }
                    },
                    "isWritable": True,
                    "links": [
                        {
                            "href": "string",
                            "rel": "string"
                        }
                    ],
                    "isDeleted": True,
                    "shareType": "NFS",
                    "smbDomainName": "string",
                    "smbValidUsers": [
                        "string"
                    ],
                    "smbValidIps": [
                        "string"
                    ]
                }
            ],
            "total": 1
        }

    def mock_get_internal_managed_volume_id():
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
            "snapshotCount": 0,
            "pendingSnapshotCount": 0,
            "isRelic": True,
            "applicationTag": "Oracle",
            "numChannels": 0,
            "volumeSize": 0,
            "usedSize": 0,
            "state": "ExportRequested",
            "hostPatterns": [
                "string"
            ],
            "mainExport": {
                "isActive": True,
                "channels": [
                    {
                        "ipAddress": "string",
                        "mountPoint": "string"
                    }
                ],
                "config": {
                    "hostPatterns": [
                        "string"
                    ],
                    "nodeHint": [
                        "string"
                    ],
                    "smbDomainName": "string",
                    "smbValidUsers": [
                        "string"
                    ],
                    "smbValidIps": [
                        "string"
                    ],
                    "subnet": "string",
                    "shareType": "NFS"
                }
            },
            "isWritable": True,
            "links": [
                {
                    "href": "string",
                    "rel": "string"
                }
            ],
            "isDeleted": True,
            "shareType": "NFS",
            "smbDomainName": "string",
            "smbValidUsers": [
                "string"
            ],
            "smbValidIps": [
                "string"
            ]
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_internal_managed_volume(), mock_get_internal_managed_volume_id()]

    assert rubrik.begin_managed_volume_snapshot(
        "name") == "No change required. The Managed Volume 'name' is already assigned in a writeable state."


def test_begin_managed_volume_snapshot(rubrik, mocker):

    def mock_get_internal_managed_volume():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_id",
                    "name": "name",
                    "configuredSlaDomainId": "string",
                    "configuredSlaDomainName": "string",
                    "primaryClusterId": "string",
                    "slaAssignment": "Derived",
                    "effectiveSlaDomainId": "string",
                    "effectiveSlaDomainName": "string",
                    "effectiveSlaDomainPolarisManagedId": "string",
                    "effectiveSlaSourceObjectId": "string",
                    "effectiveSlaSourceObjectName": "string",
                    "snapshotCount": 0,
                    "pendingSnapshotCount": 0,
                    "isRelic": True,
                    "applicationTag": "Oracle",
                    "numChannels": 0,
                    "volumeSize": 0,
                    "usedSize": 0,
                    "state": "ExportRequested",
                    "hostPatterns": [
                        "string"
                    ],
                    "mainExport": {
                        "isActive": True,
                        "channels": [
                            {
                                "ipAddress": "string",
                                "mountPoint": "string"
                            }
                        ],
                        "config": {
                            "hostPatterns": [
                                "string"
                            ],
                            "nodeHint": [
                                "string"
                            ],
                            "smbDomainName": "string",
                            "smbValidUsers": [
                                "string"
                            ],
                            "smbValidIps": [
                                "string"
                            ],
                            "subnet": "string",
                            "shareType": "NFS"
                        }
                    },
                    "isWritable": True,
                    "links": [
                        {
                            "href": "string",
                            "rel": "string"
                        }
                    ],
                    "isDeleted": True,
                    "shareType": "NFS",
                    "smbDomainName": "string",
                    "smbValidUsers": [
                        "string"
                    ],
                    "smbValidIps": [
                        "string"
                    ]
                }
            ],
            "total": 1
        }

    def mock_get_internal_managed_volume_id():
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
            "snapshotCount": 0,
            "pendingSnapshotCount": 0,
            "isRelic": True,
            "applicationTag": "Oracle",
            "numChannels": 0,
            "volumeSize": 0,
            "usedSize": 0,
            "state": "ExportRequested",
            "hostPatterns": [
                "string"
            ],
            "mainExport": {
                "isActive": True,
                "channels": [
                    {
                        "ipAddress": "string",
                        "mountPoint": "string"
                    }
                ],
                "config": {
                    "hostPatterns": [
                        "string"
                    ],
                    "nodeHint": [
                        "string"
                    ],
                    "smbDomainName": "string",
                    "smbValidUsers": [
                        "string"
                    ],
                    "smbValidIps": [
                        "string"
                    ],
                    "subnet": "string",
                    "shareType": "NFS"
                }
            },
            "isWritable": False,
            "links": [
                {
                    "href": "string",
                    "rel": "string"
                }
            ],
            "isDeleted": True,
            "shareType": "NFS",
            "smbDomainName": "string",
            "smbValidUsers": [
                "string"
            ],
            "smbValidIps": [
                "string"
            ]
        }

    def mock_post_internal_managed_volume_id_begin_snapshot():
        return {
            "snapshotId": "string",
            "ownerId": "string"
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_internal_managed_volume(), mock_get_internal_managed_volume_id()]

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_internal_managed_volume_id_begin_snapshot()

    assert rubrik.begin_managed_volume_snapshot("name") == mock_post_internal_managed_volume_id_begin_snapshot()


def test_end_managed_volume_snapshot_idempotence(rubrik, mocker):

    def mock_get_internal_managed_volume():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_id",
                    "name": "name",
                    "configuredSlaDomainId": "string",
                    "configuredSlaDomainName": "string",
                    "primaryClusterId": "string",
                    "slaAssignment": "Derived",
                    "effectiveSlaDomainId": "string",
                    "effectiveSlaDomainName": "string",
                    "effectiveSlaDomainPolarisManagedId": "string",
                    "effectiveSlaSourceObjectId": "string",
                    "effectiveSlaSourceObjectName": "string",
                    "snapshotCount": 0,
                    "pendingSnapshotCount": 0,
                    "isRelic": True,
                    "applicationTag": "Oracle",
                    "numChannels": 0,
                    "volumeSize": 0,
                    "usedSize": 0,
                    "state": "ExportRequested",
                    "hostPatterns": [
                        "string"
                    ],
                    "mainExport": {
                        "isActive": True,
                        "channels": [
                            {
                                "ipAddress": "string",
                                "mountPoint": "string"
                            }
                        ],
                        "config": {
                            "hostPatterns": [
                                "string"
                            ],
                            "nodeHint": [
                                "string"
                            ],
                            "smbDomainName": "string",
                            "smbValidUsers": [
                                "string"
                            ],
                            "smbValidIps": [
                                "string"
                            ],
                            "subnet": "string",
                            "shareType": "NFS"
                        }
                    },
                    "isWritable": False,
                    "links": [
                        {
                            "href": "string",
                            "rel": "string"
                        }
                    ],
                    "isDeleted": True,
                    "shareType": "NFS",
                    "smbDomainName": "string",
                    "smbValidUsers": [
                        "string"
                    ],
                    "smbValidIps": [
                        "string"
                    ]
                }
            ],
            "total": 1
        }

    def mock_get_internal_managed_volume_id():
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
            "snapshotCount": 0,
            "pendingSnapshotCount": 0,
            "isRelic": True,
            "applicationTag": "Oracle",
            "numChannels": 0,
            "volumeSize": 0,
            "usedSize": 0,
            "state": "ExportRequested",
            "hostPatterns": [
                "string"
            ],
            "mainExport": {
                "isActive": True,
                "channels": [
                    {
                        "ipAddress": "string",
                        "mountPoint": "string"
                    }
                ],
                "config": {
                    "hostPatterns": [
                        "string"
                    ],
                    "nodeHint": [
                        "string"
                    ],
                    "smbDomainName": "string",
                    "smbValidUsers": [
                        "string"
                    ],
                    "smbValidIps": [
                        "string"
                    ],
                    "subnet": "string",
                    "shareType": "NFS"
                }
            },
            "isWritable": False,
            "links": [
                {
                    "href": "string",
                    "rel": "string"
                }
            ],
            "isDeleted": True,
            "shareType": "NFS",
            "smbDomainName": "string",
            "smbValidUsers": [
                "string"
            ],
            "smbValidIps": [
                "string"
            ]
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_internal_managed_volume(), mock_get_internal_managed_volume_id()]

    assert rubrik.end_managed_volume_snapshot(
        "name") == "No change required. The Managed Volume 'name' is already assigned in a read only state."


def test_end_managed_volume_snapshot_invalid_current_sla_unassigned(rubrik, mocker):

    def mock_get_internal_managed_volume():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_id",
                    "name": "name",
                    "configuredSlaDomainId": "string",
                    "configuredSlaDomainName": "string",
                    "primaryClusterId": "string",
                    "slaAssignment": "Derived",
                    "effectiveSlaDomainId": "string",
                    "effectiveSlaDomainName": "string",
                    "effectiveSlaDomainPolarisManagedId": "string",
                    "effectiveSlaSourceObjectId": "string",
                    "effectiveSlaSourceObjectName": "string",
                    "snapshotCount": 0,
                    "pendingSnapshotCount": 0,
                    "isRelic": True,
                    "applicationTag": "Oracle",
                    "numChannels": 0,
                    "volumeSize": 0,
                    "usedSize": 0,
                    "state": "ExportRequested",
                    "hostPatterns": [
                        "string"
                    ],
                    "mainExport": {
                        "isActive": True,
                        "channels": [
                            {
                                "ipAddress": "string",
                                "mountPoint": "string"
                            }
                        ],
                        "config": {
                            "hostPatterns": [
                                "string"
                            ],
                            "nodeHint": [
                                "string"
                            ],
                            "smbDomainName": "string",
                            "smbValidUsers": [
                                "string"
                            ],
                            "smbValidIps": [
                                "string"
                            ],
                            "subnet": "string",
                            "shareType": "NFS"
                        }
                    },
                    "isWritable": False,
                    "links": [
                        {
                            "href": "string",
                            "rel": "string"
                        }
                    ],
                    "isDeleted": True,
                    "shareType": "NFS",
                    "smbDomainName": "string",
                    "smbValidUsers": [
                        "string"
                    ],
                    "smbValidIps": [
                        "string"
                    ]
                }
            ],
            "total": 1
        }

    def mock_get_internal_managed_volume_id():
        return {
            "id": "string",
            "name": "string",
            "configuredSlaDomainId": "string",
            "configuredSlaDomainName": "string",
            "primaryClusterId": "string",
            "slaAssignment": "Unassigned",
            "effectiveSlaDomainId": "string",
            "effectiveSlaDomainName": "string",
            "effectiveSlaDomainPolarisManagedId": "string",
            "effectiveSlaSourceObjectId": "string",
            "effectiveSlaSourceObjectName": "string",
            "snapshotCount": 0,
            "pendingSnapshotCount": 0,
            "isRelic": True,
            "applicationTag": "Oracle",
            "numChannels": 0,
            "volumeSize": 0,
            "usedSize": 0,
            "state": "ExportRequested",
            "hostPatterns": [
                "string"
            ],
            "mainExport": {
                "isActive": True,
                "channels": [
                    {
                        "ipAddress": "string",
                        "mountPoint": "string"
                    }
                ],
                "config": {
                    "hostPatterns": [
                        "string"
                    ],
                    "nodeHint": [
                        "string"
                    ],
                    "smbDomainName": "string",
                    "smbValidUsers": [
                        "string"
                    ],
                    "smbValidIps": [
                        "string"
                    ],
                    "subnet": "string",
                    "shareType": "NFS"
                }
            },
            "isWritable": True,
            "links": [
                {
                    "href": "string",
                    "rel": "string"
                }
            ],
            "isDeleted": True,
            "shareType": "NFS",
            "smbDomainName": "string",
            "smbValidUsers": [
                "string"
            ],
            "smbValidIps": [
                "string"
            ]
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_internal_managed_volume(), mock_get_internal_managed_volume_id()]

    with pytest.raises(InvalidParameterException) as error:
        rubrik.end_managed_volume_snapshot("name")

    error_message = error.value.args[0]

    assert error_message == "The Managed Volume 'name' does not have a SLA assigned currently assigned. You must populate the sla_name argument."


def test_end_managed_volume_snapshot_invalid_current_sla_unprotected(rubrik, mocker):

    def mock_get_internal_managed_volume():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_id",
                    "name": "name",
                    "configuredSlaDomainId": "string",
                    "configuredSlaDomainName": "string",
                    "primaryClusterId": "string",
                    "slaAssignment": "Derived",
                    "effectiveSlaDomainId": "string",
                    "effectiveSlaDomainName": "string",
                    "effectiveSlaDomainPolarisManagedId": "string",
                    "effectiveSlaSourceObjectId": "string",
                    "effectiveSlaSourceObjectName": "string",
                    "snapshotCount": 0,
                    "pendingSnapshotCount": 0,
                    "isRelic": True,
                    "applicationTag": "Oracle",
                    "numChannels": 0,
                    "volumeSize": 0,
                    "usedSize": 0,
                    "state": "ExportRequested",
                    "hostPatterns": [
                        "string"
                    ],
                    "mainExport": {
                        "isActive": True,
                        "channels": [
                            {
                                "ipAddress": "string",
                                "mountPoint": "string"
                            }
                        ],
                        "config": {
                            "hostPatterns": [
                                "string"
                            ],
                            "nodeHint": [
                                "string"
                            ],
                            "smbDomainName": "string",
                            "smbValidUsers": [
                                "string"
                            ],
                            "smbValidIps": [
                                "string"
                            ],
                            "subnet": "string",
                            "shareType": "NFS"
                        }
                    },
                    "isWritable": False,
                    "links": [
                        {
                            "href": "string",
                            "rel": "string"
                        }
                    ],
                    "isDeleted": True,
                    "shareType": "NFS",
                    "smbDomainName": "string",
                    "smbValidUsers": [
                        "string"
                    ],
                    "smbValidIps": [
                        "string"
                    ]
                }
            ],
            "total": 1
        }

    def mock_get_internal_managed_volume_id():
        return {
            "id": "string",
            "name": "string",
            "configuredSlaDomainId": "string",
            "configuredSlaDomainName": "string",
            "primaryClusterId": "string",
            "slaAssignment": "string",
            "effectiveSlaDomainId": "UNPROTECTED",
            "effectiveSlaDomainName": "string",
            "effectiveSlaDomainPolarisManagedId": "string",
            "effectiveSlaSourceObjectId": "string",
            "effectiveSlaSourceObjectName": "string",
            "snapshotCount": 0,
            "pendingSnapshotCount": 0,
            "isRelic": True,
            "applicationTag": "Oracle",
            "numChannels": 0,
            "volumeSize": 0,
            "usedSize": 0,
            "state": "ExportRequested",
            "hostPatterns": [
                "string"
            ],
            "mainExport": {
                "isActive": True,
                "channels": [
                    {
                        "ipAddress": "string",
                        "mountPoint": "string"
                    }
                ],
                "config": {
                    "hostPatterns": [
                        "string"
                    ],
                    "nodeHint": [
                        "string"
                    ],
                    "smbDomainName": "string",
                    "smbValidUsers": [
                        "string"
                    ],
                    "smbValidIps": [
                        "string"
                    ],
                    "subnet": "string",
                    "shareType": "NFS"
                }
            },
            "isWritable": True,
            "links": [
                {
                    "href": "string",
                    "rel": "string"
                }
            ],
            "isDeleted": True,
            "shareType": "NFS",
            "smbDomainName": "string",
            "smbValidUsers": [
                "string"
            ],
            "smbValidIps": [
                "string"
            ]
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_internal_managed_volume(), mock_get_internal_managed_volume_id()]

    with pytest.raises(InvalidParameterException) as error:
        rubrik.end_managed_volume_snapshot("name")

    error_message = error.value.args[0]

    assert error_message == "The Managed Volume 'name' does not have a SLA assigned currently assigned. You must populate the sla_name argument."


def test_end_managed_volume_snapshot_current_sla(rubrik, mocker):

    def mock_get_internal_managed_volume():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_id",
                    "name": "name",
                    "configuredSlaDomainId": "string",
                    "configuredSlaDomainName": "string",
                    "primaryClusterId": "string",
                    "slaAssignment": "Derived",
                    "effectiveSlaDomainId": "string",
                    "effectiveSlaDomainName": "string",
                    "effectiveSlaDomainPolarisManagedId": "string",
                    "effectiveSlaSourceObjectId": "string",
                    "effectiveSlaSourceObjectName": "string",
                    "snapshotCount": 0,
                    "pendingSnapshotCount": 0,
                    "isRelic": True,
                    "applicationTag": "Oracle",
                    "numChannels": 0,
                    "volumeSize": 0,
                    "usedSize": 0,
                    "state": "ExportRequested",
                    "hostPatterns": [
                        "string"
                    ],
                    "mainExport": {
                        "isActive": True,
                        "channels": [
                            {
                                "ipAddress": "string",
                                "mountPoint": "string"
                            }
                        ],
                        "config": {
                            "hostPatterns": [
                                "string"
                            ],
                            "nodeHint": [
                                "string"
                            ],
                            "smbDomainName": "string",
                            "smbValidUsers": [
                                "string"
                            ],
                            "smbValidIps": [
                                "string"
                            ],
                            "subnet": "string",
                            "shareType": "NFS"
                        }
                    },
                    "isWritable": False,
                    "links": [
                        {
                            "href": "string",
                            "rel": "string"
                        }
                    ],
                    "isDeleted": True,
                    "shareType": "NFS",
                    "smbDomainName": "string",
                    "smbValidUsers": [
                        "string"
                    ],
                    "smbValidIps": [
                        "string"
                    ]
                }
            ],
            "total": 1
        }

    def mock_get_internal_managed_volume_id():
        return {
            "id": "string",
            "name": "string",
            "configuredSlaDomainId": "string",
            "configuredSlaDomainName": "string",
            "primaryClusterId": "string",
            "slaAssignment": "string",
            "effectiveSlaDomainId": "string",
            "effectiveSlaDomainName": "string",
            "effectiveSlaDomainPolarisManagedId": "string",
            "effectiveSlaSourceObjectId": "string",
            "effectiveSlaSourceObjectName": "string",
            "snapshotCount": 0,
            "pendingSnapshotCount": 0,
            "isRelic": True,
            "applicationTag": "Oracle",
            "numChannels": 0,
            "volumeSize": 0,
            "usedSize": 0,
            "state": "ExportRequested",
            "hostPatterns": [
                "string"
            ],
            "mainExport": {
                "isActive": True,
                "channels": [
                    {
                        "ipAddress": "string",
                        "mountPoint": "string"
                    }
                ],
                "config": {
                    "hostPatterns": [
                        "string"
                    ],
                    "nodeHint": [
                        "string"
                    ],
                    "smbDomainName": "string",
                    "smbValidUsers": [
                        "string"
                    ],
                    "smbValidIps": [
                        "string"
                    ],
                    "subnet": "string",
                    "shareType": "NFS"
                }
            },
            "isWritable": True,
            "links": [
                {
                    "href": "string",
                    "rel": "string"
                }
            ],
            "isDeleted": True,
            "shareType": "NFS",
            "smbDomainName": "string",
            "smbValidUsers": [
                "string"
            ],
            "smbValidIps": [
                "string"
            ]
        }

    def mock_post_internal_managed_volume_id_begin_snapshot():
        return {
            "id": "string",
            "date": "2019-05-07T00:59:46.025Z",
            "expirationDate": "2019-05-07T00:59:46.025Z",
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
            "links": {
                "exportLink": {
                    "href": "string",
                    "rel": "string"
                },
                "self": {
                    "href": "string",
                    "rel": "string"
                }
            }
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_internal_managed_volume(), mock_get_internal_managed_volume_id()]

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_internal_managed_volume_id_begin_snapshot()

    assert rubrik.end_managed_volume_snapshot("name") == mock_post_internal_managed_volume_id_begin_snapshot()


def test_end_managed_volume_snapshot_specific_sla(rubrik, mocker):

    def mock_get_internal_managed_volume():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string_id",
                    "name": "name",
                    "configuredSlaDomainId": "string",
                    "configuredSlaDomainName": "string",
                    "primaryClusterId": "string",
                    "slaAssignment": "Derived",
                    "effectiveSlaDomainId": "string",
                    "effectiveSlaDomainName": "string",
                    "effectiveSlaDomainPolarisManagedId": "string",
                    "effectiveSlaSourceObjectId": "string",
                    "effectiveSlaSourceObjectName": "string",
                    "snapshotCount": 0,
                    "pendingSnapshotCount": 0,
                    "isRelic": True,
                    "applicationTag": "Oracle",
                    "numChannels": 0,
                    "volumeSize": 0,
                    "usedSize": 0,
                    "state": "ExportRequested",
                    "hostPatterns": [
                        "string"
                    ],
                    "mainExport": {
                        "isActive": True,
                        "channels": [
                            {
                                "ipAddress": "string",
                                "mountPoint": "string"
                            }
                        ],
                        "config": {
                            "hostPatterns": [
                                "string"
                            ],
                            "nodeHint": [
                                "string"
                            ],
                            "smbDomainName": "string",
                            "smbValidUsers": [
                                "string"
                            ],
                            "smbValidIps": [
                                "string"
                            ],
                            "subnet": "string",
                            "shareType": "NFS"
                        }
                    },
                    "isWritable": False,
                    "links": [
                        {
                            "href": "string",
                            "rel": "string"
                        }
                    ],
                    "isDeleted": True,
                    "shareType": "NFS",
                    "smbDomainName": "string",
                    "smbValidUsers": [
                        "string"
                    ],
                    "smbValidIps": [
                        "string"
                    ]
                }
            ],
            "total": 1
        }

    def mock_get_internal_managed_volume_id():
        return {
            "id": "string",
            "name": "string",
            "configuredSlaDomainId": "string",
            "configuredSlaDomainName": "string",
            "primaryClusterId": "string",
            "slaAssignment": "string",
            "effectiveSlaDomainId": "string",
            "effectiveSlaDomainName": "string",
            "effectiveSlaDomainPolarisManagedId": "string",
            "effectiveSlaSourceObjectId": "string",
            "effectiveSlaSourceObjectName": "string",
            "snapshotCount": 0,
            "pendingSnapshotCount": 0,
            "isRelic": True,
            "applicationTag": "Oracle",
            "numChannels": 0,
            "volumeSize": 0,
            "usedSize": 0,
            "state": "ExportRequested",
            "hostPatterns": [
                "string"
            ],
            "mainExport": {
                "isActive": True,
                "channels": [
                    {
                        "ipAddress": "string",
                        "mountPoint": "string"
                    }
                ],
                "config": {
                    "hostPatterns": [
                        "string"
                    ],
                    "nodeHint": [
                        "string"
                    ],
                    "smbDomainName": "string",
                    "smbValidUsers": [
                        "string"
                    ],
                    "smbValidIps": [
                        "string"
                    ],
                    "subnet": "string",
                    "shareType": "NFS"
                }
            },
            "isWritable": True,
            "links": [
                {
                    "href": "string",
                    "rel": "string"
                }
            ],
            "isDeleted": True,
            "shareType": "NFS",
            "smbDomainName": "string",
            "smbValidUsers": [
                "string"
            ],
            "smbValidIps": [
                "string"
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

    def mock_post_internal_managed_volume_id_begin_snapshot():
        return {
            "id": "string",
            "date": "2019-05-07T00:59:46.025Z",
            "expirationDate": "2019-05-07T00:59:46.025Z",
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
            "links": {
                "exportLink": {
                    "href": "string",
                    "rel": "string"
                },
                "self": {
                    "href": "string",
                    "rel": "string"
                }
            }
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [
        mock_get_internal_managed_volume(),
        mock_get_internal_managed_volume_id(),
        mock_get_v1_sla_domain()]

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_internal_managed_volume_id_begin_snapshot()

    assert rubrik.end_managed_volume_snapshot("name", "Gold") == mock_post_internal_managed_volume_id_begin_snapshot()


def test_get_sla_objects_invalid_object_type(rubrik):
    with pytest.raises(InvalidParameterException) as error:
        rubrik.get_sla_objects("Gold", "not_a_valid_object_type")

    error_message = error.value.args[0]

    assert error_message == "The get_sla_object() object_type argument must be one of the following: ['vmware']."


def test_get_sla_objects_not_protecting_objects(rubrik, mocker):

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

    def mock_get_v1_vmware_vm():
        return {
            "hasMore": False,
            "data": [],
            "total": 0
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_v1_sla_domain(), mock_get_v1_vmware_vm()]

    with pytest.raises(InvalidParameterException) as error:
        rubrik.get_sla_objects("Gold", "vmware")

    error_message = error.value.args[0]

    assert error_message == "The SLA 'Gold' is currently not protecting any vmware objects."


def test_get_sla_objects(rubrik, mocker):

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

    def mock_get_v1_vmware_vm():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "sla_id",
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

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_v1_sla_domain(), mock_get_v1_vmware_vm()]

    assert rubrik.get_sla_objects("Gold", "vmware") == {'object_name': 'sla_id'}
