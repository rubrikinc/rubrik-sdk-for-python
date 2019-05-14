# Copyright 2018 Rubrik, Inc.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

"""
This module contains the Rubrik SDK Cloud class.
"""

import os
import re
from .api import Api
from .exceptions import InvalidParameterException, CDMVersionException, InvalidTypeException


class Cloud(Api):
    """This class contains methods for the managment of Cloud related functionality on the Rubrik cluster."""

    def aws_s3_cloudout(self, aws_bucket_name, archive_name='default', aws_region=None, aws_access_key=None, aws_secret_key=None, kms_master_key_id=None, rsa_key=None, storage_class='standard', timeout=180):  # pylint: ignore
        """Add a new AWS S3 archival location to the Rubrik cluster.

        Arguments:
            aws_bucket_name {str} -- The name of the AWS S3 bucket you wish to use as an archive target. The bucket name will automatically have all whitespace removed, all letters lowercased, and can not contain any of the following characters: `_\/*?%.:\|<>`.

        Keyword Arguments:
            aws_region {str} -- The name of the AWS region where the bucket is located. If set to the default `None` keyword argument, we will look for a `AWS_DEFAULT_REGION` environment variable to pull the value from. (default: {None}) (choices: {ap-south-1, ap-northeast-2, ap-southeast-1, ap-southeast-2, ap-northeast-1, ca-central-1, cn-north-1, cn-northwest-1, eu-central-1, eu-west-1, eu-west-2, eu-west-3, sa-east-1, us-gov-west-1, us-west-1, us-east-1, us-east-2, us-west-2})
            aws_access_key {str} -- The access key of a AWS account with the required permissions. If set to the default `None` keyword argument, we will look for a `AWS_ACCESS_KEY_ID` environment variable to pull the value from. (default: {None})
            aws_secret_key {str} -- The secret key of a AWS account with the required permissions. If set to the default `None` keyword argument, we will look for a `AWS_SECRET_ACCESS_KEY` environment variable to pull the value from. (default: {None})
            kms_master_key_id {str} -- The AWS KMS master key ID that will be used to encrypt the archive data. If set to the default `None` keyword argument, you will need to provide a `rsa_key` instead. (default: {None})
            rsa_key {str} -- The RSA key that will be used to encrypt the archive data. A key can be generated through `openssl genrsa -out rubrik_encryption_key.pem 2048`. If set to the default `None` keyword argument, you will need to provide a `kms_master_key_id` instead.  (default: {None})
            archive_name {str} -- The name of the archive location used in the Rubrik GUI. If set to 'default' the following naming convention will be used: "AWS:S3:`aws_bucket_name`" (default: {'default'})
            storage_class {str} -- The AWS storage class you wish to use. (default: {'standard'}) (choices: {standard, 'standard_ia, reduced_redundancy, onezone_ia})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {180})


        Returns:
            str -- No change required. The '`name`' archival location is already configured on the Rubrik cluster.
            dict -- The full API response for `POST /internal/archive/object_store'`.
        """

        valid_aws_regions = [
            'ap-south-1',
            'ap-northeast-2',
            'ap-southeast-1',
            'ap-southeast-2',
            'ap-northeast-1',
            'ca-central-1',
            'cn-north-1',
            'cn-northwest-1',
            'eu-central-1',
            'eu-west-1',
            'eu-west-2',
            'eu-west-3',
            'sa-east-1',
            'us-gov-west-1',
            'us-west-1',
            'us-east-1',
            'us-east-2',
            'us-west-2']

        valid_storage_classes = [
            'standard',
            'standard_ia',
            'reduced_redundancy',
            'onezone_ia']

        if re.compile(r'[_\/*?%.:|<>]').findall(aws_bucket_name):
            raise InvalidParameterException(
                r"The `aws_bucket_name` may not contain any of the following characters: _\/*?%.:|<>")

        if aws_region is None:
            aws_region = os.environ.get('AWS_DEFAULT_REGION')
            if aws_region is None:
                raise InvalidParameterException("`aws_region` has not been provided.")

        if aws_access_key is None:
            aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
            if aws_access_key is None:
                raise InvalidParameterException("`aws_access_key` has not been provided.")

        if aws_secret_key is None:
            aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
            if aws_secret_key is None:
                raise InvalidParameterException("`aws_secret_key` has not been provided.")

        if aws_region not in valid_aws_regions:
            raise InvalidParameterException('The `aws_region` must be one of the following: {}'.format(
                valid_aws_regions))

        if storage_class not in valid_storage_classes:
            raise InvalidParameterException('The `storage_class` must be one of the following: {}'.format(
                valid_storage_classes))
        else:
            storage_class = storage_class.upper()

        if archive_name == 'default':
            archive_name = 'AWS:S3:{}'.format(aws_bucket_name.lower().strip())

        if kms_master_key_id is None and rsa_key is None:
            raise InvalidParameterException(
                "You must populated either `kms_master_key_id` or `rsa_key`.")
        elif kms_master_key_id is not None and rsa_key is not None:
            raise InvalidParameterException(
                "Both `kms_master_key_id` or `rsa_key` have been populated. You may only use one.")

        archives_on_cluster = self.get('internal', '/archive/object_store', timeout=timeout)

        config = {}
        config['name'] = archive_name
        config['bucket'] = aws_bucket_name.lower().strip()
        config['defaultRegion'] = aws_region
        config['storageClass'] = storage_class
        config['accessKey'] = aws_access_key
        config['secretKey'] = aws_secret_key
        if kms_master_key_id:
            config['kmsMasterKeyId'] = kms_master_key_id
        elif rsa_key:
            config['pemFileContent'] = rsa_key
        config['objectStoreType'] = 'S3'

        # Create a new dictionary that includes only the values returned by
        # archives_on_cluster
        redacted_archive_definition = {}
        redacted_archive_definition['objectStoreType'] = 'S3'
        redacted_archive_definition['name'] = archive_name
        redacted_archive_definition['accessKey'] = aws_access_key
        redacted_archive_definition['bucket'] = aws_bucket_name.lower().strip()
        redacted_archive_definition['defaultRegion'] = aws_region
        redacted_archive_definition['storageClass'] = storage_class

        for archive in archives_on_cluster['data']:
            # If present, remove the Cloud On Configuration for comparison
            archive_definition = archive['definition']
            for value in ["encryptionType", "defaultComputeNetworkConfig",
                          "isComputeEnabled", "isConsolidationEnabled"]:
                try:
                    del archive_definition[value]
                except BaseException:
                    pass

            if archive_definition == redacted_archive_definition:
                return "No change required. The '{}' archival location is already configured on the Rubrik cluster.".format(
                    archive_name)
            if archive['definition']['objectStoreType'] == 'S3' and archive['definition']['name'] == archive_name:
                raise InvalidParameterException(
                    "Archival location with name '{}' already exists. Please enter a unique `archive_name`.".format(archive_name))

        self.log("aws_s3_cloudout: Creating the AWS S3 archive location.")
        return self.post('internal', '/archive/object_store', config, timeout)

    def update_aws_s3_cloudout(self, current_archive_name, new_archive_name=None, aws_access_key=None, aws_secret_key=None, storage_class=None, timeout=180):  # pylint: ignore
        """Update an AWS S3 archival location on the Rubrik cluster.

        Keyword Arguments:
            current_archive_name {str} -- The name of the current archive to be updated.
            new_archive_name {str} -- Desired name for the updated archive location. If set to default `None` keyword argument, no change will be made. (default: {None})
            aws_access_key {str} -- The access key of a AWS account with the required permissions. If set to the default `None` keyword argument, no change will be made. (default: {None})
            aws_secret_key {str} -- The secret key of a AWS account with the required permissions. If set to the default `None` keyword argument, no change will be made. (default: {None})
            storage_class {str} -- The AWS storage class you wish to use. If set to the default `None` keyword argument, no change will be made. (default: {None}) (choices: {standard, 'standard_ia, reduced_redundancy, onezone_ia})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {180})


        Returns:
            dict -- The full API response for `PATCH /internal/archive/object_store/{id}'`.
        """

        valid_storage_classes = [
            'standard',
            'standard_ia',
            'reduced_redundancy',
            'onezone_ia']

        if storage_class is not None and storage_class not in valid_storage_classes:
            raise InvalidParameterException(
                'The `storage_class` must be one of the following: {}'.format(valid_storage_classes))

        update_config = None

        self.log("update_aws_s3_cloudout: Searching the Rubrik cluster for S3 archival locations named {}.".format(
            current_archive_name))
        archives_on_cluster = self.get('internal', '/archive/object_store', timeout=timeout)

        for archive in archives_on_cluster['data']:
            # If present, remove the Cloud On Configuration for comparison
            archive_definition = archive['definition']
            try:
                del archive_definition['defaultComputeNetworkConfig']
            except BaseException:
                pass
            if archive['definition']['objectStoreType'] == 'S3' and archive['definition']['name'] == current_archive_name:
                self.log("update_aws_s3_cloudout: Found matching S3 archival location named {}.".format(current_archive_name))
                update_config = archive_definition
                archive_id = archive['id']

        if update_config is None:
            raise InvalidParameterException(
                "No S3 archival location with name '{}' exists.".format(current_archive_name))

        if new_archive_name:
            update_config['name'] = new_archive_name

        if aws_access_key:
            update_config['accessKey'] = aws_access_key

        if aws_secret_key:
            update_config['secretKey'] = aws_secret_key

        if storage_class:
            update_config['storageClass'] = storage_class.upper()

        self.log("update_aws_s3_cloudout: Updating the AWS S3 archive location named {}.".format(current_archive_name))
        return self.patch('internal', '/archive/object_store/{}'.format(archive_id), update_config, timeout)

    def aws_s3_cloudon(self, archive_name, vpc_id, subnet_id, security_group_id, timeout=30):
        """Enable CloudOn for an exsiting AWS S3 archival location.

        Arguments:
            archive_name {str} -- The name of the archive location used in the Rubrik GUI.

        Keyword Arguments:
            vpc_id {str} -- The AWS VPC ID used by Rubrik cluster to launch a temporary Rubrik instance in AWS for instantiation.
            subnet_id {str} -- The AWS Subnet ID used by Rubrik cluster to launch a temporary Rubrik instance in AWS for instantiation.
            security_group_id {str} -- The AWS Security Group ID used by Rubrik cluster to launch a temporary Rubrik instance in AWS for instantiation.
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {30})

        Returns:
            str -- No change required. The '`name`' archival location is already configured on the Rubrik cluster.
            dict -- The full API response for `PATCH /internal/archive/object_store/{id}`.
        """

        self.log("aws_s3_cloudon: Searching the Rubrik cluster for archival locations.")
        archives_on_cluster = self.get('internal', '/archive/object_store', timeout=timeout)

        config = {}
        config['defaultComputeNetworkConfig'] = {}
        config['defaultComputeNetworkConfig']['subnetId'] = subnet_id
        config['defaultComputeNetworkConfig']['vNetId'] = vpc_id
        config['defaultComputeNetworkConfig']['securityGroupId'] = security_group_id

        for archive in archives_on_cluster['data']:
            if archive['definition']['objectStoreType'] == 'S3' and archive['definition']['name'] == archive_name:
                # If present, remove the Cloud On configuration for proper
                # comparison
                try:
                    if archive['definition']['defaultComputeNetworkConfig'] == config['defaultComputeNetworkConfig']:
                        return "No change required. The '{}' archival location is already configured for CloudOn.".format(
                            archive_name)
                except KeyError:
                    self.log("aws_s3_cloudon: Updating the archive location for CloudOn.")
                    return self.patch('internal', "/archive/object_store/{}".format(archive['id']), config, timeout)

        raise InvalidParameterException(
            "The Rubrik cluster does not have an archive location named '{}'.".format(archive_name))

    def azure_cloudout(self, container, azure_access_key, storage_account_name, rsa_key, archive_name='default', instance_type='default', timeout=180):  # pylint: ignore
        """Add a new Azure archival location to the Rubrik cluster.

        Arguments:
            container {str} -- The name of the Azure storage container you wish to use as an archive. The container name will automatically be lowercased and can not contain any of the following characters: `_\/*?%.:\|<>`.
            azure_access_key {str} -- The access key for the Azure storage account.
            storage_account_name {str} -- The name of the Storage Account that the `container` belongs to.
            rsa_key {str} -- The RSA key that will be used to encrypt the archive data. A key can be generated through `openssl genrsa -out rubrik_encryption_key.pem 2048`.

        Keyword Arguments:
            archive_name {str} -- The name of the archive location used in the Rubrik GUI. If set to `default`, the following naming convention will be used: "Azure:`container`" (default: {'default'})
            instance_type {str} -- The Cloud Platform type of the archival location. (default: {'default'}) (choices: {'default', 'china', 'germany', 'government'})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {180})

        Returns:
            str -- No change required. The '`name`' archival location is already configured on the Rubrik cluster.
            dict -- The full API response for `POST /internal/archive/object_store`.
        """

        container = container.lower()

        if re.compile(r'[_\/*?%.:|<>]').findall(container):
            raise InvalidParameterException(
                r"The `container` may not contain any of the following characters: _\/*?%.:|<>")

        valid_instance_types = ['default', 'china', 'germany', 'government']

        if instance_type not in valid_instance_types:
            raise InvalidParameterException('The `instance_type` argument must be one of the following: {}'.format(
                valid_instance_types))

        if archive_name == 'default':
            archive_name = 'Azure:{}'.format(container)

        self.log("azure_cloudout: Searching the Rubrik cluster for archival locations.")
        archives_on_cluster = self.get('internal', '/archive/object_store', timeout=timeout)

        config = {}
        config['name'] = archive_name
        config['bucket'] = container
        config['accessKey'] = storage_account_name
        config['secretKey'] = azure_access_key
        config['pemFileContent'] = rsa_key
        config['objectStoreType'] = 'Azure'
        if instance_type == 'government':
            config['endpoint'] = 'core.usgovcloudapi.net'
        elif instance_type == 'germany':
            config['endpoint'] = 'core.cloudapi.de'
        elif instance_type == 'china':
            config['endpoint'] = 'core.chinacloudapi.cn'

        # Create a new dictionary that includes only the values returned by
        # archives_on_cluster
        redacted_archive_definition = {}
        redacted_archive_definition['objectStoreType'] = 'Azure'
        redacted_archive_definition['name'] = archive_name
        redacted_archive_definition['accessKey'] = storage_account_name
        redacted_archive_definition['bucket'] = container
        if instance_type == 'government':
            redacted_archive_definition['endpoint'] = 'core.usgovcloudapi.net'
        elif instance_type == 'germany':
            redacted_archive_definition['endpoint'] = 'core.cloudapi.de'
        elif instance_type == 'china':
            redacted_archive_definition['endpoint'] = 'core.chinacloudapi.cn'

        for archive in archives_on_cluster['data']:
            # If present, remove the Cloud On Configuration for comparison
            archive_definition = archive['definition']
            for value in ["encryptionType", "defaultComputeNetworkConfig",
                          "isComputeEnabled", "isConsolidationEnabled", "azureComputeSummary"]:
                try:
                    del archive_definition[value]
                except BaseException:
                    pass

            if archive_definition == redacted_archive_definition:
                return "No change required. The '{}' archival location is already configured on the Rubrik cluster.".format(
                    archive_name)

            if archive_definition['objectStoreType'] == 'Azure' and archive_definition['name'] == archive_name:
                raise InvalidParameterException("Archival location with name '{}' already exists. Please enter a unique `name`.".format(
                    archive_name))

        self.log("azure_cloudout: Creating the Azure archive location.")
        return self.post('internal', '/archive/object_store', config)

    def azure_cloudon(self, archive_name, container, storage_account_name, application_id, application_key, tenant_id, region, virtual_network_id, subnet_name, security_group_id, timeout=30):  # pylint: ignore
        """Enable CloudOn for an exsiting AWS S3 archival location.

        Arguments:
            archive_name {str} -- The name of the archive location used in the Rubrik GUI.
            container {str} -- The name of the Azure storage container being used as the archive target. The container name will automatically be lowercased and can not contain any of the following characters: `_\/*?%.:\|<>`.
            storage_account_name {str} -- The name of the Storage Account that the `container` belongs to.
            application_id {str} -- The ID of the application registered in Azure Active Directory.
            application_key {str} -- The key of the application registered in Azure Active Directory.
            tenant_id {str} -- The tenant ID, also known as the directory ID, found under the Azure Active Directory properties.
            region {str} -- The name of the Azure region where the `container` is located. (choices: {westus, westus2, centralus, eastus, eastus2, northcentralus, southcentralus, westcentralus, canadacentral, canadaeast, brazilsouth, northeurope, westeurope, uksouth, ukwest, eastasia, southeastasia, japaneast, japanwest, australiaeast australiasoutheast, centralindia, southindia, westindia, koreacentral, koreasouth})
            virtual_network_id {str} -- The Azure virtual network ID used by Rubrik cluster to launch a temporary Rubrik instance in Azure for instantiation.
            subnet_name {str} -- The Azure subnet name used by Rubrik cluster to launch a temporary Rubrik instance in Azure for instantiation.
            security_group_id {str} -- The Azure Security Group ID used by Rubrik cluster to launch a temporary Rubrik instance in Azure for instantiation.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {30})


        Returns:
            str -- No change required. The '`archive_name`' archival location is already configured for CloudOn.
            dict -- The full API response for `PATCH /internal/archive/object_store/{id}`.
        """

        valid_regions = [
            "westus",
            "westus2",
            "centralus",
            "eastus",
            "eastus2",
            "northcentralus",
            "southcentralus",
            "westcentralus",
            "canadacentral",
            "canadaeast",
            "brazilsouth",
            "northeurope",
            "westeurope",
            "uksouth",
            "ukwest",
            "eastasia",
            "southeastasia",
            "japaneast",
            "japanwest",
            "australiaeast",
            "australiasoutheast",
            "centralindia",
            "southindia",
            "westindia",
            "koreacentral",
            "koreasouth"]

        if region not in valid_regions:
            raise InvalidParameterException('The `region` must be one of the following: {}'.format(valid_regions))

        self.log("azure_cloudon: Searching the Rubrik cluster for archival locations.")
        archives_on_cluster = self.get('internal', '/archive/object_store', timeout=timeout)

        config = {}
        config['name'] = archive_name
        config['objectStoreType'] = 'Azure'
        config['isComputeEnabled'] = True

        config['azureComputeSummary'] = {}
        config['azureComputeSummary']["tenantId"] = tenant_id
        config['azureComputeSummary']["subscriptionId"] = virtual_network_id.split("/")[2]
        config['azureComputeSummary']["clientId"] = application_id
        config['azureComputeSummary']["region"] = region
        config['azureComputeSummary']["generalPurposeStorageAccountName"] = storage_account_name
        config['azureComputeSummary']["containerName"] = container

        config['azureComputeSecret'] = {}
        config['azureComputeSecret']["clientSecret"] = application_key
        config['defaultComputeNetworkConfig'] = {}
        config['defaultComputeNetworkConfig']['subnetId'] = subnet_name
        config['defaultComputeNetworkConfig']['vNetId'] = virtual_network_id
        config['defaultComputeNetworkConfig']['securityGroupId'] = security_group_id

        redacted_archive_definition = {}
        redacted_archive_definition['name'] = archive_name
        redacted_archive_definition['objectStoreType'] = "Azure"
        redacted_archive_definition['accessKey'] = storage_account_name
        redacted_archive_definition['bucket'] = container
        redacted_archive_definition['isComputeEnabled'] = True

        redacted_archive_definition['azureComputeSummary'] = {}
        redacted_archive_definition['azureComputeSummary']["tenantId"] = tenant_id
        redacted_archive_definition['azureComputeSummary']["subscriptionId"] = virtual_network_id.split("/")[2]
        redacted_archive_definition['azureComputeSummary']["clientId"] = application_id
        redacted_archive_definition['azureComputeSummary']["region"] = region
        redacted_archive_definition['azureComputeSummary']["generalPurposeStorageAccountName"] = storage_account_name
        redacted_archive_definition['azureComputeSummary']["containerName"] = container

        redacted_archive_definition['defaultComputeNetworkConfig'] = {}
        redacted_archive_definition['defaultComputeNetworkConfig']['subnetId'] = subnet_name
        redacted_archive_definition['defaultComputeNetworkConfig']['vNetId'] = virtual_network_id
        redacted_archive_definition['defaultComputeNetworkConfig']['securityGroupId'] = security_group_id

        for archive in archives_on_cluster['data']:

            archive_definition = archive['definition']
            for value in ["isConsolidationEnabled", "encryptionType"]:
                try:
                    del archive_definition[value]
                except BaseException:
                    pass

            try:
                del archive_definition["azureComputeSummary"]["environment"]
            except BaseException:
                pass

            try:
                del archive_definition["defaultComputeNetworkConfig"]["resourceGroupId"]
            except BaseException:
                pass

            if archive['definition']['objectStoreType'] == 'Azure' and archive['definition']['name'] == archive_name:

                if archive['definition'] == redacted_archive_definition:

                    return "No change required. The '{}' archival location is already configured for CloudOn.".format(
                        archive_name)
                else:
                    self.log("azure_cloudon: Updating the archive location for CloudOn.")
                    return self.patch('internal', "/archive/object_store/{}".format(archive['id']), config, timeout)

        raise InvalidParameterException(
            "The Rubrik cluster does not have an archive location named '{}'.".format(archive_name))

    def add_aws_native_account(self, aws_account_name, aws_access_key=None, aws_secret_key=None, aws_regions=None, regional_bolt_network_configs=None, timeout=30):  # pylint: ignore
        """Add a new AWS account to EC2 native protection on the Rubrik cluster.

        Arguments:
            aws_account_name {str} -- The name of the AWS account you wish to protect. This is the name that will be displayed in the Rubrik UI.

        Keyword Arguments:
            aws_access_key {str} -- The access key of a AWS account with the required permissions. If set to the default `None` keyword argument, we will look for a `AWS_ACCESS_KEY_ID` environment variable to pull the value from. (default: {None})
            aws_secret_key {str} -- The secret key of a AWS account with the required permissions. If set to the default `None` keyword argument, we will look for a `AWS_SECRET_ACCESS_KEY` environment variable to pull the value from. (default: {None})
            aws_regions {list} -- List of AWS regions to protect in this AWS account. If set to the default `None` keyword argument, we will look for a `AWS_DEFAULT_REGION` environment variable to pull the value from. (default: {None}) (choices: {ap-south-1, ap-northeast-3, ap-northeast-2, ap-southeast-1, ap-southeast-2, ap-northeast-1, ca-central-1, cn-north-1, cn-northwest-1, eu-central-1, eu-west-1, eu-west-2, eu-west-3, us-west-1, us-east-1, us-east-2, us-west-2})
            regional_bolt_network_configs {list of dicts} -- List of dicts containing per region bolt network configs. (ex. dict format: {"region": "aws-region-name", "vNetId": "aws-vpc-id", "subnetId": "aws-subnet-id", "securityGroupId": "aws-subnet-id"}) (default: {None})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {30})


        Returns:
            str -- No change required. Cloud native source with access key `aws_access_key` is already configured on the Rubrik cluster.
            dict -- The full API response for `POST /internal/aws/account'`.
        """

        valid_aws_regions = [
            'ap-south-1',
            'ap-northeast-3',
            'ap-northeast-2',
            'ap-southeast-1',
            'ap-southeast-2',
            'ap-northeast-1',
            'ca-central-1',
            'cn-north-1',
            'cn-northwest-1',
            'eu-central-1',
            'eu-west-1',
            'eu-west-2',
            'eu-west-3',
            'us-west-1',
            'us-east-1',
            'us-east-2',
            'us-west-2']

        # verify we are on cdm 4.2 or newer, required for cloud native
        # protection
        if self.minimum_installed_cdm_version(4.2) is False:
            raise CDMVersionException(4.2)

        # check for regions and credentials in environment variables if not
        # provided explicitly
        if aws_regions is None:
            aws_regions = [os.environ.get('AWS_DEFAULT_REGION')]
            if aws_regions == [None]:
                raise InvalidParameterException("`aws_region` has not been provided.")

        if aws_access_key is None:
            aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
            if aws_access_key is None:
                raise InvalidParameterException("`aws_access_key` has not been provided.")

        if aws_secret_key is None:
            aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
            if aws_secret_key is None:
                raise InvalidParameterException("`aws_secret_key` has not been provided.")

        # verify supplied regions are in the supported list of regions for
        # cloud native protection
        if any(aws_region not in valid_aws_regions for aws_region in aws_regions):
            raise InvalidParameterException(
                'The list `aws_regions` may only contain the following values: {}'.format(valid_aws_regions))

        # verify that our regional_bolt_network_configs are either None or in a
        # list
        if isinstance(regional_bolt_network_configs, list) is False and regional_bolt_network_configs is not None:
            raise InvalidTypeException("`regional_bolt_network_configs` must be a list if defined.")

        if regional_bolt_network_configs is not None:

            # verify our list of bolt_network_configs only contains dicts
            for bolt_network_config in regional_bolt_network_configs:
                if isinstance(bolt_network_config, dict) is False:
                    raise InvalidTypeException("The `regional_bolt_network_configs` list can only contain dicts.")

                # verify that all the required paramteters are provided in all
                # regional_bolt_network_configs
                if any(requiredkey not in bolt_network_config for requiredkey in [
                        'region',
                        'vNetId',
                        'subnetId',
                        'securityGroupId']):
                    raise InvalidParameterException(
                        "Each `regional_bolt_network_config` dict must contain the following keys: 'region', 'vNetId', 'subnetId', 'securityGroupId'.")

        self.log("aws_native_account: Searching the Rubrik cluster for cloud native sources.")
        cloud_native_on_cluster = self.get('internal', '/aws/account', timeout=timeout)

        for cloud_source in cloud_native_on_cluster['data']:

            # verify a cloud native source with this name does not exist
            # already
            self.log("aws_native_account: Validating no conflict with `{}`".format(cloud_source['id']))
            if cloud_source['name'] == aws_account_name:
                raise InvalidParameterException("Cloud native source with name '{}' already exists. Please enter a unique `aws_account_name`.".format(
                    aws_account_name))

            # idempotent return if a cloud native source with this access key
            # already exists
            cloud_source_detail = self.get('internal', '/aws/account/{}'.format(cloud_source['id']), timeout=timeout)
            if cloud_source_detail['accessKey'] == aws_access_key:
                return "No change required. Cloud native source with access key '{}' is already configured on the Rubrik cluster.".format(
                    aws_access_key)

        # build the config for our API call
        config = {}
        config['name'] = aws_account_name
        config['accessKey'] = aws_access_key
        config['secretKey'] = aws_secret_key
        config['regions'] = aws_regions

        # only include bolt configs if they were supplied
        if regional_bolt_network_configs is not None:
            config['regionalBoltNetworkConfigs'] = regional_bolt_network_configs

        # make the API call, return the result
        self.log("aws_native_account: Creating the cloud native source.")
        return self.post('internal', '/aws/account', config, timeout)

    def update_aws_native_account(self, aws_account_name, config, timeout=15):
        """Update an exsiting AWS account used for EC2 native protection on the Rubrik cluster.

        Arguments:
            aws_account_name {str} -- The name of the AWS account you wish to update. This is the name that is displayed in the Rubrik UI.

        Keyword Arguments:
            config {dict} -- The configuration to use to update the AWS account. Full example values can be found in the Rubrik API Playground for the PATCH /aws/account/{id} endpoint
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})


        Returns:
            dict -- The full API response for `PATCH /aws/account/{id}`.
        """
        # verify we are on cdm 4.2 or newer, required for cloud native
        # protection
        if self.minimum_installed_cdm_version(4.2) is False:
            raise CDMVersionException(4.2)

        if not isinstance(config, dict):
            raise InvalidTypeException("The 'config' argument must be a dictionary.")

        self.log("update_aws_native_account: Checking the Rubrik cluster for the AWS Native Account.")
        account_id = self.object_id(aws_account_name, "aws_native", timeout=timeout)

        self.log("update_aws_native_account: Updating the AWS Native Account.")
        return self.patch("internal", "/aws/account/{}".format(account_id), config)
