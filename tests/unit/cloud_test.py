import pytest
from rubrik_cdm.exceptions import InvalidParameterException, CDMVersionException
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
