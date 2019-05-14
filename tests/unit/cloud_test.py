import pytest
from rubrik_cdm.exceptions import InvalidParameterException, CDMVersionException, InvalidTypeException
from rubrik_cdm import Connect


def test_aws_s3_cloudout_invalid_aws_region(rubrik):

    with pytest.raises(InvalidParameterException) as error:
        rubrik.aws_s3_cloudout(
            "awsbucketname",
            "archive_name",
            "not_a_valid_aws_region",
            "aws_region",
            "aws_access_key",
            "aws_secret_key")

    error_message = error.value.args[0]

    assert error_message == "The `aws_region` must be one of the following: ['ap-south-1', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'ca-central-1', 'cn-north-1', 'cn-northwest-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'sa-east-1', 'us-gov-west-1', 'us-west-1', 'us-east-1', 'us-east-2', 'us-west-2']"


def test_aws_s3_cloudout_invalid_storage_class(rubrik):

    with pytest.raises(InvalidParameterException) as error:
        rubrik.aws_s3_cloudout(
            "awsbucketname",
            "archive_name",
            "ap-south-1",
            "aws_access_key",
            "aws_secret_key",
            "kms_master_key_id",
            "rsa_key",
            "not_a_valid_storage_class")

    error_message = error.value.args[0]

    assert error_message == "The `storage_class` must be one of the following: ['standard', 'standard_ia', 'reduced_redundancy', 'onezone_ia']"


@pytest.mark.parametrize('archive_name', ["_", "/", "*", "?", "%", ".", ":", "|", "<", ">"])
def test_aws_s3_cloudout_invalid_aws_bucket_name(rubrik, archive_name):

    with pytest.raises(InvalidParameterException) as error:
        rubrik.aws_s3_cloudout(archive_name)

    error_message = error.value.args[0]

    assert error_message == r"The `aws_bucket_name` may not contain any of the following characters: _\/*?%.:|<>"


def test_aws_s3_cloudout_missing_aws_region(rubrik):

    with pytest.raises(InvalidParameterException) as error:
        rubrik.aws_s3_cloudout("awsbucketname")

    error_message = error.value.args[0]

    assert error_message == "`aws_region` has not been provided."


def test_aws_s3_cloudout_missing_aws_access_key(rubrik):

    with pytest.raises(InvalidParameterException) as error:
        rubrik.aws_s3_cloudout("awsbucketname", "archive_name", "ap-south-1")

    error_message = error.value.args[0]

    assert error_message == "`aws_access_key` has not been provided."


def test_aws_s3_cloudout_missing_aws_secret_key(rubrik):

    with pytest.raises(InvalidParameterException) as error:
        rubrik.aws_s3_cloudout("awsbucketname", "archive_name", "ap-south-1", "aws_access_key")

    error_message = error.value.args[0]

    assert error_message == "`aws_secret_key` has not been provided."


def test_aws_s3_cloudout_missing_kms_and_rsa(rubrik):

    with pytest.raises(InvalidParameterException) as error:
        rubrik.aws_s3_cloudout(
            "awsbucketname",
            "archive_name",
            "ap-south-1",
            "aws_access_key",
            "aws_secret_key")

    error_message = error.value.args[0]

    assert error_message == "You must populated either `kms_master_key_id` or `rsa_key`."


def test_aws_s3_cloudout_both_kms_and_rsa_populated(rubrik):

    with pytest.raises(InvalidParameterException) as error:
        rubrik.aws_s3_cloudout(
            "awsbucketname",
            "archive_name",
            "ap-south-1",
            "aws_access_key",
            "aws_secret_key",
            "kms_master_key_id",
            "rsa_key")

    error_message = error.value.args[0]

    assert error_message == "Both `kms_master_key_id` or `rsa_key` have been populated. You may only use one."


def test_aws_s3_cloudout_idempotence(rubrik, mocker):

    def mock_get_internal_archive_object_store():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "polarisManagedId": "string",
                    "definition": {
                        "objectStoreType": "S3",
                        "name": "archive_name",
                        "accessKey": "aws_access_key",
                        "bucket": "awsbucketname",
                        "defaultRegion": "ap-south-1",
                        "isComputeEnabled": True,
                        "isConsolidationEnabled": True,
                        "defaultComputeNetworkConfig": {
                            "subnetId": "string",
                            "vNetId": "string",
                            "securityGroupId": "string",
                            "resourceGroupId": "string"
                        },
                        "storageClass": "STANDARD",
                        "encryptionType": "RSA_KEY_ENCRYPTION"
                    },

                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_archive_object_store()

    assert rubrik.aws_s3_cloudout("awsbucketname", "archive_name", "ap-south-1", "aws_access_key", "aws_secret_key", None, "rsa_key") \
        == "No change required. The 'archive_name' archival location is already configured on the Rubrik cluster."


def test_aws_s3_cloudout_archive_name_already_exsits(rubrik, mocker):

    def mock_get_internal_archive_object_store():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "polarisManagedId": "string",
                    "definition": {
                        "objectStoreType": "S3",
                        "name": "archive_name",
                        "accessKey": "string",
                        "bucket": "string",
                        "defaultRegion": "string",
                        "isComputeEnabled": True,
                        "isConsolidationEnabled": True,
                        "defaultComputeNetworkConfig": {
                            "subnetId": "string",
                            "vNetId": "string",
                            "securityGroupId": "string",
                            "resourceGroupId": "string"
                        },
                        "storageClass": "STANDARD",
                        "encryptionType": "RSA_KEY_ENCRYPTION"
                    },

                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_archive_object_store()

    with pytest.raises(InvalidParameterException) as error:
        rubrik.aws_s3_cloudout(
            "awsbucketname",
            "archive_name",
            "ap-south-1",
            "aws_access_key",
            "aws_secret_key",
            None,
            "rsa_key")

    error_message = error.value.args[0]

    assert error_message == "Archival location with name 'archive_name' already exists. Please enter a unique `archive_name`."


def test_aws_s3_cloudout(rubrik, mocker):

    def mock_get_internal_archive_object_store():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "polarisManagedId": "string",
                    "definition": {
                        "objectStoreType": "S3",
                        "name": "string",
                        "accessKey": "aws_access_key",
                        "bucket": "awsbucketname",
                        "defaultRegion": "ap-south-1",
                        "isComputeEnabled": True,
                        "isConsolidationEnabled": True,
                        "defaultComputeNetworkConfig": {
                            "subnetId": "string",
                            "vNetId": "string",
                            "securityGroupId": "string",
                            "resourceGroupId": "string"
                        },
                        "storageClass": "STANDARD",
                        "encryptionType": "RSA_KEY_ENCRYPTION"
                    },

                }
            ],
            "total": 1
        }

    def mock_post_internal_archive_object_store():
        return {
            "jobInstanceId": "string"
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_archive_object_store()

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_internal_archive_object_store()

    assert rubrik.aws_s3_cloudout("awsbucketname", "archive_name", "ap-south-1", "aws_access_key", "aws_secret_key", None, "rsa_key") \
        == mock_post_internal_archive_object_store()


def test_update_aws_s3_cloudout_invalid_storage_class(rubrik):

    with pytest.raises(InvalidParameterException) as error:
        rubrik.update_aws_s3_cloudout("current_archive_name", storage_class="not_a_valid_storage_class")

    error_message = error.value.args[0]

    assert error_message == "The `storage_class` must be one of the following: ['standard', 'standard_ia', 'reduced_redundancy', 'onezone_ia']"


def test_update_aws_s3_cloudout_current_archive_name_not_found(rubrik, mocker):

    def mock_get_internal_archive_object_store():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "polarisManagedId": "string",
                    "definition": {
                        "objectStoreType": "S3",
                        "name": "string",
                        "accessKey": "aws_access_key",
                        "bucket": "awsbucketname",
                        "defaultRegion": "ap-south-1",
                        "isComputeEnabled": True,
                        "isConsolidationEnabled": True,
                        "defaultComputeNetworkConfig": {
                            "subnetId": "string",
                            "vNetId": "string",
                            "securityGroupId": "string",
                            "resourceGroupId": "string"
                        },
                        "storageClass": "STANDARD",
                        "encryptionType": "RSA_KEY_ENCRYPTION"
                    },

                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_archive_object_store()

    with pytest.raises(InvalidParameterException) as error:
        rubrik.update_aws_s3_cloudout("current_archive_name")

    error_message = error.value.args[0]

    assert error_message == "No S3 archival location with name 'current_archive_name' exists."


def test_update_aws_s3_cloudout(rubrik, mocker):

    def mock_get_internal_archive_object_store():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "polarisManagedId": "string",
                    "definition": {
                        "objectStoreType": "S3",
                        "name": "current_archive_name",
                        "accessKey": "aws_access_key",
                        "bucket": "awsbucketname",
                        "defaultRegion": "ap-south-1",
                        "isComputeEnabled": True,
                        "isConsolidationEnabled": True,
                        "defaultComputeNetworkConfig": {
                            "subnetId": "string",
                            "vNetId": "string",
                            "securityGroupId": "string",
                            "resourceGroupId": "string"
                        },
                        "storageClass": "STANDARD",
                        "encryptionType": "RSA_KEY_ENCRYPTION"
                    },

                }
            ],
            "total": 1
        }

    def mock_patch_internal_archive_object_store():
        return {
            "jobInstanceId": "string"
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_archive_object_store()

    mock_patch = mocker.patch('rubrik_cdm.Connect.patch', autospec=True, spec_set=True)
    mock_patch.return_value = mock_patch_internal_archive_object_store()

    assert rubrik.update_aws_s3_cloudout("current_archive_name", "new_archive_name", "aws_access_key", "aws_secret_key", "standard") \
        == mock_patch_internal_archive_object_store()


def test_aws_s3_cloudon_idempotence(rubrik, mocker):

    def mock_get_internal_archive_object_store():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "polarisManagedId": "string",
                    "definition": {
                        "objectStoreType": "S3",
                        "name": "archive_name",
                        "accessKey": "aws_access_key",
                        "bucket": "awsbucketname",
                        "defaultRegion": "ap-south-1",
                        "isComputeEnabled": True,
                        "isConsolidationEnabled": True,
                        "defaultComputeNetworkConfig": {
                            "subnetId": "subnet_id",
                            "vNetId": "vpc_id",
                            "securityGroupId": "security_group_id",
                        },
                        "storageClass": "STANDARD",
                        "encryptionType": "RSA_KEY_ENCRYPTION"
                    },

                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_archive_object_store()

    assert rubrik.aws_s3_cloudon("archive_name", "vpc_id", "subnet_id", "security_group_id") \
        == "No change required. The 'archive_name' archival location is already configured for CloudOn."


def test_aws_s3_cloudon_archive_name_not_found(rubrik, mocker):

    def mock_get_internal_archive_object_store():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "polarisManagedId": "string",
                    "definition": {
                        "objectStoreType": "S3",
                        "name": "string",
                        "accessKey": "aws_access_key",
                        "bucket": "awsbucketname",
                        "defaultRegion": "ap-south-1",
                        "isComputeEnabled": True,
                        "isConsolidationEnabled": True,
                        "storageClass": "STANDARD",
                        "encryptionType": "RSA_KEY_ENCRYPTION"
                    },

                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_archive_object_store()

    with pytest.raises(InvalidParameterException) as error:
        rubrik.aws_s3_cloudon("archive_name", "vpc_id", "subnet_id", "security_group_id")

    error_message = error.value.args[0]

    assert error_message == "The Rubrik cluster does not have an archive location named 'archive_name'."


def test_aws_s3_cloudon(rubrik, mocker):

    def mock_get_internal_archive_object_store():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "polarisManagedId": "string",
                    "definition": {
                        "objectStoreType": "S3",
                        "name": "archive_name",
                        "accessKey": "aws_access_key",
                        "bucket": "awsbucketname",
                        "defaultRegion": "ap-south-1",
                        "isComputeEnabled": True,
                        "isConsolidationEnabled": True,
                        "storageClass": "STANDARD",
                        "encryptionType": "RSA_KEY_ENCRYPTION"
                    },

                }
            ],
            "total": 1
        }

    def mock_patch_internal_archive_object_store():
        return {
            "jobInstanceId": "string"
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_archive_object_store()

    mock_patch = mocker.patch('rubrik_cdm.Connect.patch', autospec=True, spec_set=True)
    mock_patch.return_value = mock_patch_internal_archive_object_store()

    assert rubrik.aws_s3_cloudon("archive_name", "vpc_id", "subnet_id", "security_group_id") \
        == mock_patch_internal_archive_object_store()


@pytest.mark.parametrize('container', ["_", "/", "*", "?", "%", ".", ":", "|", "<", ">"])
def test_azure_cloudout_invalid_container(rubrik, container):

    with pytest.raises(InvalidParameterException) as error:
        rubrik.azure_cloudout(container, "azure_access_key", "storage_account_name", "rsa_key")

    error_message = error.value.args[0]

    assert error_message == r"The `container` may not contain any of the following characters: _\/*?%.:|<>"


def test_azure_cloudout_invalid_instance_type(rubrik):

    with pytest.raises(InvalidParameterException) as error:
        rubrik.azure_cloudout("container", "azure_access_key", "storage_account_name",
                              "rsa_key", instance_type="not_a_valid_instance_type")

    error_message = error.value.args[0]

    assert error_message == "The `instance_type` argument must be one of the following: ['default', 'china', 'germany', 'government']"


def test_azure_cloudout_idempotence(rubrik, mocker):

    def mock_get_internal_archive_object_store():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "polarisManagedId": "string",
                    "definition": {
                        "objectStoreType": "Azure",
                        "name": "archive_name",
                        "accessKey": "storage_account_name",
                        "bucket": "container",
                        "isComputeEnabled": True,
                        "isConsolidationEnabled": True,
                        "encryptionType": "RSA_KEY_ENCRYPTION"
                    },

                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_archive_object_store()

    assert rubrik.azure_cloudout("container", "azure_access_key", "storage_account_name", "rsa_key", "archive_name") \
        == "No change required. The 'archive_name' archival location is already configured on the Rubrik cluster."


def test_azure_cloudout_invalid_archive_name(rubrik, mocker):

    def mock_get_internal_archive_object_store():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "polarisManagedId": "string",
                    "definition": {
                        "objectStoreType": "Azure",
                        "name": "archive_name",
                        "accessKey": "string",
                        "bucket": "string",
                        "isComputeEnabled": True,
                        "isConsolidationEnabled": True,
                        "encryptionType": "RSA_KEY_ENCRYPTION"
                    },

                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_archive_object_store()

    with pytest.raises(InvalidParameterException) as error:
        rubrik.azure_cloudout("container", "azure_access_key", "storage_account_name", "rsa_key", "archive_name")

    error_message = error.value.args[0]

    assert error_message == "Archival location with name 'archive_name' already exists. Please enter a unique `name`."


def test_azure_cloudout(rubrik, mocker):

    def mock_get_internal_archive_object_store():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "polarisManagedId": "string",
                    "definition": {
                        "objectStoreType": "Azure",
                        "name": "string",
                        "accessKey": "storage_account_name",
                        "bucket": "container",
                        "isComputeEnabled": True,
                        "isConsolidationEnabled": True,
                        "encryptionType": "RSA_KEY_ENCRYPTION"
                    },

                }
            ],
            "total": 1
        }

    def mock_patch_internal_archive_object_store():
        return {
            "jobInstanceId": "string"
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_archive_object_store()

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_patch_internal_archive_object_store()

    assert rubrik.azure_cloudout("container", "azure_access_key", "storage_account_name",
                                 "rsa_key", "archive_name") == mock_patch_internal_archive_object_store()


def test_azure_cloudon_invalid_region(rubrik):

    with pytest.raises(InvalidParameterException) as error:
        rubrik.azure_cloudon(
            "archive_name",
            "container",
            "storage_account_name",
            "application_id",
            "application_key",
            "tenant_id",
            "not_a_valid_region",
            "virtual_network_id",
            "subnet_name",
            "security_group_id")

    error_message = error.value.args[0]

    assert error_message == "The `region` must be one of the following: ['westus', 'westus2', 'centralus', 'eastus', 'eastus2', 'northcentralus', 'southcentralus', 'westcentralus', 'canadacentral', 'canadaeast', 'brazilsouth', 'northeurope', 'westeurope', 'uksouth', 'ukwest', 'eastasia', 'southeastasia', 'japaneast', 'japanwest', 'australiaeast', 'australiasoutheast', 'centralindia', 'southindia', 'westindia', 'koreacentral', 'koreasouth']"


def test_azure_cloudon_idempotence(rubrik, mocker):

    def mock_get_internal_archive_object_store():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "polarisManagedId": "string",
                    "definition": {
                        "objectStoreType": "Azure",
                        "name": "archive_name",
                        "accessKey": "storage_account_name",
                        "bucket": "container",
                        "isComputeEnabled": True,
                        "isConsolidationEnabled": True,
                        "defaultComputeNetworkConfig": {
                            "subnetId": "subnet_name",
                            "vNetId": "/subscriptions/89b90dec-a6e1-4q9e-bc12-23138bb3cee4/resourceGroups/PythonSDK/providers/Microsoft.Network/virtualNetworks/pythonsdk",
                            "securityGroupId": "security_group_id",
                            "resourceGroupId": "string"
                        },
                        "azureComputeSummary": {
                            "tenantId": "tenant_id",
                            "subscriptionId": "89b90dec-a6e1-4q9e-bc12-23138bb3cee4",
                            "clientId": "application_id",
                            "region": "westus",
                            "generalPurposeStorageAccountName": "storage_account_name",
                            "containerName": "container",
                            "environment": "AZURE"
                        },
                        "encryptionType": "RSA_KEY_ENCRYPTION"
                    },


                }
            ],
            "total": 1
        }

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_archive_object_store()

    assert rubrik.azure_cloudon(
        "archive_name",
        "container",
        "storage_account_name",
        "application_id",
        "application_key",
        "tenant_id",
        "westus",
        "/subscriptions/89b90dec-a6e1-4q9e-bc12-23138bb3cee4/resourceGroups/PythonSDK/providers/Microsoft.Network/virtualNetworks/pythonsdk",
        "subnet_name",
        "security_group_id") == "No change required. The 'archive_name' archival location is already configured for CloudOn."


def test_update_aws_native_account_minimum_installed_cdm_version_not_met(rubrik, mocker):

    def mock_self_cluster_version():
        return "4.0.1-1280"

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = mock_self_cluster_version()

    with pytest.raises(CDMVersionException) as error:
        rubrik.update_aws_native_account("aws_account_name", {})


def test_update_aws_native_account_invalid_config(rubrik, mocker):

    def mock_self_cluster_version():
        return "4.2.1-1280"

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = mock_self_cluster_version()

    with pytest.raises(InvalidTypeException) as error:
        rubrik.update_aws_native_account("aws_account_name", "not_a_dictionary")

    error_message = error.value.args[0]

    assert error_message == "The 'config' argument must be a dictionary."


def test_update_aws_native_account(rubrik, mocker):

    def mock_self_cluster_version():
        return "4.2.1-1280"

    def mock_get_internal_aws_account_name():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "aws_account_name",
                    "primaryClusterId": "string",
                    "status": "Connected"
                }
            ],
            "total": 1
        }

    def mock_patch_internal_aws_account_id():
        return {
            "name": "string",
            "accessKey": "string",
            "regions": [
                "string"
            ],
            "regionalBoltNetworkConfigs": [
                {
                    "region": "string",
                    "vNetId": "string",
                    "subnetId": "string",
                    "securityGroupId": "string"
                }
            ],
            "disasterRecoveryArchivalLocationId": "string",
            "id": "string",
            "configuredSlaDomainId": "string",
            "configuredSlaDomainName": "string",
            "primaryClusterId": "string"
        }

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = mock_self_cluster_version()

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_aws_account_name()

    mock_patch = mocker.patch('rubrik_cdm.Connect.patch', autospec=True, spec_set=True)
    mock_patch.return_value = mock_patch_internal_aws_account_id()

    assert rubrik.update_aws_native_account("aws_account_name", {}) == \
        mock_patch_internal_aws_account_id()


def test_add_aws_native_account_minimum_installed_cdm_version_not_met(rubrik, mocker):

    def mock_self_cluster_version():
        return "4.0.1-1280"

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = mock_self_cluster_version()

    with pytest.raises(CDMVersionException) as error:
        rubrik.add_aws_native_account(
            "aws_account_name",
            "aws_access_key",
            "aws_secret_key",
            ["not_a_valid_region"],
            {})


def test_add_aws_native_account_missing_aws_region(rubrik, mocker):

    def mock_self_cluster_version():
        return "4.2.1-1280"

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = mock_self_cluster_version()

    with pytest.raises(InvalidParameterException) as error:
        rubrik.add_aws_native_account("aws_account_name")

    error_message = error.value.args[0]

    assert error_message == "`aws_region` has not been provided."


def test_add_aws_native_account_missing_aws_access_key(rubrik, mocker):

    def mock_self_cluster_version():
        return "4.2.1-1280"

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = mock_self_cluster_version()

    with pytest.raises(InvalidParameterException) as error:
        rubrik.add_aws_native_account("aws_account_name", aws_regions=["ap-south-1"])

    error_message = error.value.args[0]

    assert error_message == "`aws_access_key` has not been provided."


def test_add_aws_native_account_missing_aws_secret_key(rubrik, mocker):

    def mock_self_cluster_version():
        return "4.2.1-1280"

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = mock_self_cluster_version()

    with pytest.raises(InvalidParameterException) as error:
        rubrik.add_aws_native_account("aws_account_name", "aws_access_key", aws_regions=["ap-south-1"])

    error_message = error.value.args[0]

    assert error_message == "`aws_secret_key` has not been provided."


def test_add_aws_native_account_invalid_aws_regionss(rubrik, mocker):

    def mock_self_cluster_version():
        return "4.2.1-1280"

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = mock_self_cluster_version()

    with pytest.raises(InvalidParameterException) as error:
        rubrik.add_aws_native_account(
            "aws_account_name",
            "aws_access_key",
            "aws_secret_key",
            ["not_a_valid_region"],
            {})

    error_message = error.value.args[0]

    assert error_message == "The list `aws_regions` may only contain the following values: ['ap-south-1', 'ap-northeast-3', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'ca-central-1', 'cn-north-1', 'cn-northwest-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'us-west-1', 'us-east-1', 'us-east-2', 'us-west-2']"


def test_add_aws_native_account_invalid_regional_bolt_network_configs_list(rubrik, mocker):

    def mock_self_cluster_version():
        return "4.2.1-1280"

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = mock_self_cluster_version()

    with pytest.raises(InvalidTypeException) as error:
        rubrik.add_aws_native_account(
            "aws_account_name",
            "aws_access_key",
            "aws_secret_key",
            ["ap-south-1"],
            "not_a_valid_regional_bolt_config")

    error_message = error.value.args[0]

    assert error_message == "`regional_bolt_network_configs` must be a list if defined."


def test_add_aws_native_account_invalid_regional_bolt_network_configs_list_dict(rubrik, mocker):

    def mock_self_cluster_version():
        return "4.2.1-1280"

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = mock_self_cluster_version()

    with pytest.raises(InvalidTypeException) as error:
        rubrik.add_aws_native_account(
            "aws_account_name",
            "aws_access_key",
            "aws_secret_key",
            ["ap-south-1"],
            ["not_a_valid_regional_bolt_config"])

    error_message = error.value.args[0]

    assert error_message == "The `regional_bolt_network_configs` list can only contain dicts."


def test_add_aws_native_account_invalid_regional_bolt_network_configs_list_dict_value(rubrik, mocker):

    def mock_self_cluster_version():
        return "4.2.1-1280"

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = mock_self_cluster_version()

    with pytest.raises(InvalidParameterException) as error:
        rubrik.add_aws_native_account(
            "aws_account_name",
            "aws_access_key",
            "aws_secret_key",
            ["ap-south-1"],
            [{"not_a_valid_key": "string"}])

    error_message = error.value.args[0]

    assert error_message == "Each `regional_bolt_network_config` dict must contain the following keys: 'region', 'vNetId', 'subnetId', 'securityGroupId'."


def test_add_aws_native_account_invalid_aws_account_name(rubrik, mocker):

    def mock_self_cluster_version():
        return "4.2.1-1280"

    def mock_get_internal_aws_account_name():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "aws_account_name",
                    "primaryClusterId": "string",
                    "status": "Connected"
                }
            ],
            "total": 1
        }

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = mock_self_cluster_version()

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.return_value = mock_get_internal_aws_account_name()

    with pytest.raises(InvalidParameterException) as error:
        rubrik.add_aws_native_account(
            "aws_account_name",
            "aws_access_key",
            "aws_secret_key",
            ["ap-south-1"],
            [{"region": "string", "vNetId": "string", "subnetId": "string", "securityGroupId": "string"}])

    error_message = error.value.args[0]

    assert error_message == "Cloud native source with name 'aws_account_name' already exists. Please enter a unique `aws_account_name`."


def test_add_aws_native_account_idempotence(rubrik, mocker):

    def mock_self_cluster_version():
        return "4.2.1-1280"

    def mock_get_internal_aws_account_name():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "string",
                    "primaryClusterId": "string",
                    "status": "Connected"
                }
            ],
            "total": 1
        }

    def mock_get_internal_aws_account_id():
        return {
            "name": "string",
            "accessKey": "aws_access_key",
            "regions": [
                "string"
            ],
            "regionalBoltNetworkConfigs": [
                {
                    "region": "string",
                    "vNetId": "string",
                    "subnetId": "string",
                    "securityGroupId": "string"
                }
            ],
            "disasterRecoveryArchivalLocationId": "string",
            "id": "string",
            "configuredSlaDomainId": "string",
            "configuredSlaDomainName": "string",
            "primaryClusterId": "string"
        }

    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = mock_self_cluster_version()

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_internal_aws_account_name(), mock_get_internal_aws_account_id()]

    assert rubrik.add_aws_native_account("aws_account_name",
                                         "aws_access_key",
                                         "aws_secret_key",
                                         ["ap-south-1"],
                                         [{"region": "string",
                                           "vNetId": "string",
                                           "subnetId": "string",
                                           "securityGroupId": "string"}]) == "No change required. Cloud native source with access key 'aws_access_key' is already configured on the Rubrik cluster."


def test_add_aws_native_account(rubrik, mocker):

    def mock_self_cluster_version():
        return "4.2.1-1280"

    def mock_get_internal_aws_account_name():
        return {
            "hasMore": True,
            "data": [
                {
                    "id": "string",
                    "name": "string",
                    "primaryClusterId": "string",
                    "status": "Connected"
                }
            ],
            "total": 1
        }

    def mock_get_internal_aws_account_id():
        return {
            "name": "string",
            "accessKey": "string",
            "regions": [
                "string"
            ],
            "regionalBoltNetworkConfigs": [
                {
                    "region": "string",
                    "vNetId": "string",
                    "subnetId": "string",
                    "securityGroupId": "string"
                }
            ],
            "disasterRecoveryArchivalLocationId": "string",
            "id": "string",
            "configuredSlaDomainId": "string",
            "configuredSlaDomainName": "string",
            "primaryClusterId": "string"
        }

    def mock_post_internal_aws_account():
        return {
            "id": "string",
            "status": "string",
            "progress": 0,
            "startTime": "2019-05-03T16:15:38.827Z",
            "endTime": "2019-05-03T16:15:38.827Z",
            "nodeId": "string",
            "error": {
                "message": "string"
            },
            "links": [
                {
                    "href": "string",
                    "rel": "string"
                }
            ]
        }
    mock_cluster_version = mocker.patch('rubrik_cdm.Connect.cluster_version', autospec=True, spec_set=True)
    mock_cluster_version.return_value = mock_self_cluster_version()

    mock_get = mocker.patch('rubrik_cdm.Connect.get', autospec=True, spec_set=True)
    mock_get.side_effect = [mock_get_internal_aws_account_name(), mock_get_internal_aws_account_id()]

    mock_post = mocker.patch('rubrik_cdm.Connect.post', autospec=True, spec_set=True)
    mock_post.return_value = mock_post_internal_aws_account()

    assert rubrik.add_aws_native_account("aws_account_name",
                                         "aws_access_key",
                                         "aws_secret_key",
                                         ["ap-south-1"],
                                         [{"region": "string",
                                           "vNetId": "string",
                                           "subnetId": "string",
                                           "securityGroupId": "string"}]) == mock_post_internal_aws_account()
