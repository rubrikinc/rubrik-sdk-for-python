# Copyright 2018 Rubrik, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License prop
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module contains the Rubrik SDK Cluster class.
"""

import sys
import os
import re
from .api import Api

_API = Api


class Cluster(_API):
    """This class contains methods related to the managment of the Rubrik Cluster itself.
    """

    def cluster_version(self, timeout=15):
        """Retrieves the software version of the Rubrik Cluster.

        Keyword Arguments:
            timeout {int} -- The response timeout value, in seconds, of the API call. (default: {15})

        Returns:
            dict -- Software version running on the Rubrik Cluster
        """
        self.log('cluster_version: Getting the software version of the Rubrik Cluster.')
        api_request = self.get('v1', '/cluster/me/version', timeout)
        return api_request

    def cluster_node_ip(self, timeout=15):
        """Retrive the IP Address for each node in the Rubrik Cluster.

        Keyword Arguments:
            timeout {int} -- The response timeout value, in seconds, of the API call. (default: {15})

        Returns:
            list -- A list that contains the IP Address for each node in the Rubrik Cluster.
        """

        self.log('cluster_node_ip: Generating a list of all Cluster Node IPs.')
        api_request = self.get('internal', '/cluster/me/node', timeout)

        node_ip_list = []

        for node in api_request['data']:
            node_ip_list.append(node["ipAddress"])

        return node_ip_list

    def end_user_authorization(self, object_name, end_user, object_type='vmware', timeout=15):
        """Grant an End User authorization to the provided object.

        Arguments:
            object_name {str} -- The name of the object you wish to grant authorization to.
            end_user {str} -- The name of the end user you wish to grant authorization to.

        Keyword Arguments:
            object_type {str} -- The Rubrik object type you wish to backup. `vmware` is currently the only supported option. (choices: {vmware}) (default: {vmware}) 
            timeout {int} -- The timeout value for the API call that grants the End User authoriauthorizationation. (default: {15})

        Returns:
            str -- If the End User is already authorized to interact with the provided object name the following is returned: The End User "{`end_user`}" is already authorized to interact with the "{`object_name`}" VM.
            dict -- The full response for the `/internal//authorization/role/end_user` API endpoint. 
        """

        valid_object_type = ['vmware']

        if object_type not in valid_object_type:
            sys.exit("Error: The end_user_authorization() object_type argument must be one of the following: {}.".format(
                valid_object_type))

        self.log("end_user_authorization: Searching the Rubrik Cluster for the vSphere VM '{}'.".format(object_name))
        vm_id = self.object_id(object_name, object_type)

        self.log("end_user_authorization: Searching the Rubrik Cluster for the End User '{}'.".format(end_user))
        user = self.get('internal', '/user?username={}'.format(end_user))
        if not user:
            sys.exit('The Rubrik Cluster does not contain a End User Account named "{}".'.format(end_user))
        else:
            user_id = user[0]['id']

        self.log("end_user_authorization: Searching the Rubrik Cluster for the End User '{}' authorizations.".format(end_user))
        user_authorization = self.get('internal', '/authorization/role/end_user?principals={}'.format(user_id))

        authorized_objects = user_authorization['data'][0]['privileges']['restore']

        if vm_id in authorized_objects:
            return 'The End User "{}" is already authorized to interact with the "{}" VM.'.format(end_user, object_name)
        else:
            config = {}
            config['principals'] = [user_id]
            config['privileges'] = {"restore": [vm_id]}

            return self.post('internal', '/authorization/role/end_user', config, timeout=timeout)

    def add_archive_aws_s3(self, aws_bucket_name, aws_region=None, aws_access_key=None, aws_secret_key=None, kms_master_key_id=None, rsa_key=None, name='default', storage_class='standard', vpc_id=None, subnet_id=None, security_group_id=None):
        """Add a new AWS S3 archive target to the Rubrik Cluster and optionally configure the required Cloud On options.

        Arguments:
            aws_bucket_name {str} -- The name of the AWS S3 bucket you wish to use. The bucket name will automatically have all whitespace removed and all letters will be lowercased. The bucket name may not contain any of the following characters: `_\/*?%.:|<>`

        Keyword Arguments:
            aws_region {str} -- The name of the AWS region where the bucket is located. If set to the default `None` value we will look for a `AWS_DEFAULT_REGION` environment variable to pull the value from. (default: {None}) (choices: {'ap-south-1', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'ca-central-1', 'cn-north-1', 'cn-northwest-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'sa-east-1', 'us-gov-west-1' 'us-west-1' 'us-east-1', 'us-east-2', 'us-west-2'})
            aws_access_key {str} -- The access key of account with the required permissions. If set to the default `None` value we will look for a `AWS_ACCESS_KEY_ID` environment variable to pull the value from. (default: {None})
            aws_secret_key {str} -- The secret key of account with the required permissions. If set to the default `None` value we will look for a `AWS_SECRET_ACCESS_KEY` environment variable to pull the value from. (default: {None})
            kms_master_key_id {str} -- The AWS master key Id that will be used to encrypt the archive data. If set to the default `None` value you will need to provide a `rsa_key` instead. (default: {None})
            rsa_key {str} -- The RSA key that will be used to encrypt the archive data. A key can be generated through `openssl genrsa -out rubrik_encryption_key.pem 2048`. If set to the default `None` value you will need to provide a `kms_master_key_id` instead.  (default: {None})
            name {str} -- The name of the archive location used in the Rubrik GUI. If set to default the following naming convention will be used: AWS:S3:{`aws_bucket_name`} (default: {'default'})
            storage_class {str} -- The storage class you wish to use. (default: {'standard'}) (choices: {'standard', 'standard_ia', 'reduced_redundancy'})
            vpc_id {str} -- The VPC Id used for Cloud On. When a value has been provided you must also provide a value for `subnet_id` and `security_group_id` (default: {None})
            subnet_id {str} -- The Subnet id used for Cloud On. When a value has been provided you must also provide a value for `vpc_id` and `security_group_id` (default: {None})
            security_group_id {str} -- The Security Group Id used for Cloud On. When a value has been provided you must also provide a value for `vpc_id` and `subnet_id` (default: {None})

        Returns:
            str -- No change required. The '`name`' archival location is already configured on the Rubrik Cluster.
            dict -- The full API response for `POST /internal/archive/object_store'.
        """

        valid_aws_regions = ['ap-south-1', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'ca-central-1', 'cn-north-1',
                             'cn-northwest-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'sa-east-1', 'us-gov-west-1' 'us-west-1' 'us-east-1', 'us-east-2', 'us-west-2']

        valid_storage_classes = ['standard', 'standard_ia', 'reduced_redundancy']

        if all([vpc_id, subnet_id, security_group_id]) == False and any([vpc_id, subnet_id, security_group_id]) == True:
            sys.exit("Error: You must populate a value for each of the following variables or leave them as the default `None` value: 'vpc_id', 'subnet_id', 'security_group_id'.")

        if re.compile(r'[_\/*?%.:|<>]').findall(aws_bucket_name):
            sys.exit("Error: The `aws_bucket_name` may not contain any of the following characters: _\/*?%.:|<>")

        if aws_region is None:
            aws_region = os.environ.get('AWS_DEFAULT_REGION')
            if aws_region is None:
                sys.exit("Error: `aws_region` has not been provided.")

        if aws_access_key is None:
            aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
            if aws_access_key is None:
                sys.exit("Error: `aws_access_key` has not been provided.")

        if aws_secret_key is None:
            aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
            if aws_secret_key is None:
                sys.exit("Error: `aws_secret_key` has not been provided.")

        if aws_region not in valid_aws_regions:
            sys.exit('Error: The `aws_region` must be one of the following: {}'.format(valid_aws_regions))

        if storage_class not in valid_storage_classes:
            sys.exit('Error: The `storage_class` must be one of the following: {}'.format(valid_storage_classes))
        else:
            storage_class = storage_class.upper()

        if name == 'default':
            name = 'AWS:S3:{}'.format(aws_bucket_name.lower().strip())

        if kms_master_key_id is None and rsa_key is None:
            sys.exit("Error: You must populated either `kms_master_key_id` or `rsa_key`.")
        elif kms_master_key_id is not None and rsa_key is not None:
            sys.exit("Error: Both `kms_master_key_id` or `rsa_key` have been populated. You may only use one.")

        self.log("add_aws_s3_archive: Searching the Rubrik Cluster for archival locations.")
        current_s3_archive = self.get('internal', '/archive/object_store')

        config = {}
        config['name'] = name
        config['bucket'] = aws_bucket_name.lower().strip()
        config['defaultRegion'] = aws_region
        config['storageClass'] = storage_class
        config['accessKey'] = aws_access_key
        config['secretKey'] = aws_secret_key
        if kms_master_key_id:
            config['kmsMasterKeyId'] = kms_master_key_id
        elif rsa_key:
            config['pemFileContent'] = rsa_key
        if all([vpc_id, subnet_id, security_group_id]):
            config['defaultComputeNetworkConfig'] = {}
            config['defaultComputeNetworkConfig']['subnetId'] = subnet_id
            config['defaultComputeNetworkConfig']['vNetId'] = vpc_id
            config['defaultComputeNetworkConfig']['securityGroupId'] = security_group_id

        config['objectStoreType'] = 'S3'

        user_archive_definition = {}
        user_archive_definition['objectStoreType'] = 'S3'
        user_archive_definition['name'] = name
        user_archive_definition['accessKey'] = aws_access_key
        user_archive_definition['bucket'] = aws_bucket_name.lower().strip()
        user_archive_definition['defaultRegion'] = aws_region
        user_archive_definition['storageClass'] = storage_class
        if all([vpc_id, subnet_id, security_group_id]):
            user_archive_definition['defaultComputeNetworkConfig'] = {}
            user_archive_definition['defaultComputeNetworkConfig']['subnetId'] = subnet_id
            user_archive_definition['defaultComputeNetworkConfig']['vNetId'] = vpc_id
            user_archive_definition['defaultComputeNetworkConfig']['securityGroupId'] = security_group_id

        for archive in current_s3_archive['data']:
            if archive['definition'] == user_archive_definition:
                return "No change required. The '{}' archival location is already configured on the Rubrik Cluster.".format(name)
            if archive['definition']['objectStoreType'] == 'S3' and archive['definition']['name'] == name:
                sys.exit("Error: Archival location with name '{}' already exists. Please enter a unique `name`.".format(name))

        self.log("add_aws_s3_archive: Creating the AWS S3 archive location.")
        return self.post('internal', '/archive/object_store', config)

    def add_archive_azure(self, container, azure_access_key, storage_account_name, rsa_key, application_id=None, application_key=None, tenant_id=None, region=None, virtual_network_id=None, subnet_name=None, security_group_id=None, name='default', instance_type='default'):
        """Add a new Azure archive target to the Rubrik Cluster and optionally configure the required Cloud On options.

        Arguments:
            container {str} -- The name of the Azure storage container you wish to use as an archive.
            azure_access_key {str} -- The access key for the storage account.
            storage_account_name {str} -- The name of the Storage Account that the `container` belongs to.
            rsa_key {str} -- The RSA key that will be used to encrypt the archive data. A key can be generated through `openssl genrsa -out rubrik_encryption_key.pem 2048`.

        Keyword Arguments:
            name {str} -- The name of the archive location used in the Rubrik GUI. If set to default the following naming convention will be used: Azure:`container` (default: {'default'}) (default: {'default'})
            instance_type {str} -- The Cloud Platform type of the archival location. (default: {'default'}) (choices: {'default', 'china', 'germany', 'government'})
            application_id {str} -- The Id of the application registered in Azure Active Directory. Only required when configuring Cloud On. (default: {None})
            application_key {str} -- The key of the application registered in Azure Active Directory. Only required when configuring Cloud On. (default: {None})
            tenant_id {str} -- The tenant Id, also known as the directory Id found under the Azure Active Directory properties. Only required when configuring Cloud On. (default: {None})
            region {str} -- The name of the Azure region where the `container` is located. Only required when configuring Cloud On. (default: {None}) (choices: {"westus", "westus2", "centralus", "eastus", "eastus2", "northcentralus", "southcentralus", "westcentralus", "canadacentral", "canadaeast", "brazilsouth", "northeurope", "westeurope", "uksouth", "ukwest", "eastasia", "southeastasia", "japaneast", "japanwest", "australiaeast", "australiasoutheast", "centralindia", "southindia", "westindia", "koreacentral", "koreasouth"})
            virtual_network_id {str} -- The virtual network Id used for Cloud On. (default: {None})
            subnet_name {str} -- The subnet name used for Cloud On. (default: {None})
            security_group_id {str} -- The security group Id used for Cloud On. (default: {None})

        Returns:
            str -- No change required. The '`name`' archival location is already configured on the Rubrik Cluster."
            dict -- The full API response for `POST /internal/archive/object_store'.
        """

        container = container.lower()

        valid_instance_types = ['default', 'china', 'germany', 'government']

        valid_regions = ["westus", "westus2", "centralus", "eastus", "eastus2", "northcentralus", "southcentralus", "westcentralus", "canadacentral", "canadaeast", "brazilsouth", "northeurope", "westeurope",
                         "uksouth", "ukwest", "eastasia", "southeastasia", "japaneast", "japanwest", "australiaeast", "australiasoutheast", "centralindia", "southindia", "westindia", "koreacentral", "koreasouth"]

        cloud_on_properties = [application_id, application_key, tenant_id,
                               region, virtual_network_id, subnet_name, security_group_id]

        if region not in valid_regions:
            sys.exit('Error: The `region` must be one of the following: {}'.format(valid_regions))

        if all(cloud_on_properties) == False and any(cloud_on_properties) == True:
            sys.exit("Error: You must populate a value for each of the following keyword arguments or leave them as the default `None` value: application_id, application_key, tenant_id, subscription, region, virtual_network_id, subnet_name, security_group_id")

        if instance_type not in valid_instance_types:
            sys.exit('Error: The `instance_type` argument must be one of the following: {}'.format(valid_instance_types))

        if re.compile(r'[_\/*?%.:|<>]').findall(container):
            sys.exit("Error: The `container` may not contain any of the following characters: _\/*?%.:|<>")

        if name == 'default':
            name = 'Azure:{}'.format(container)

        self.log("add_azure_archive: Searching the Rubrik Cluster for archival locations.")
        current_s3_archive = self.get('internal', '/archive/object_store')

        config = {}
        config['name'] = name
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
        if all(cloud_on_properties):
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

        user_archive_definition = {}
        user_archive_definition['objectStoreType'] = 'Azure'
        user_archive_definition['name'] = name
        user_archive_definition['accessKey'] = storage_account_name
        user_archive_definition['bucket'] = container
        if instance_type == 'government':
            user_archive_definition['endpoint'] = 'core.usgovcloudapi.net'
        elif instance_type == 'germany':
            user_archive_definition['endpoint'] = 'core.cloudapi.de'
        elif instance_type == 'china':
            user_archive_definition['endpoint'] = 'core.chinacloudapi.cn'
        if all(cloud_on_properties):
            user_archive_definition['isComputeEnabled'] = True
            user_archive_definition['azureComputeSummary'] = {}
            user_archive_definition['azureComputeSummary']["tenantId"] = tenant_id
            user_archive_definition['azureComputeSummary']["subscriptionId"] = virtual_network_id.split("/")[2]
            user_archive_definition['azureComputeSummary']["clientId"] = application_id
            user_archive_definition['azureComputeSummary']["region"] = region
            user_archive_definition['azureComputeSummary']["generalPurposeStorageAccountName"] = storage_account_name
            user_archive_definition['azureComputeSummary']["containerName"] = container
            user_archive_definition['defaultComputeNetworkConfig'] = {}
            user_archive_definition['defaultComputeNetworkConfig']['subnetId'] = subnet_name
            user_archive_definition['defaultComputeNetworkConfig']['vNetId'] = virtual_network_id
            user_archive_definition['defaultComputeNetworkConfig']['securityGroupId'] = security_group_id

        for archive in current_s3_archive['data']:
            if archive['definition'] == user_archive_definition:
                return "No change required. The '{}' archival location is already configured on the Rubrik Cluster.".format(name)
            if archive['definition']['objectStoreType'] == 'Azure' and archive['definition']['name'] == name:
                sys.exit("Error: Archival location with name '{}' already exists. Please enter a unique `name`.".format(name))

        self.log("add_azure_archive: Creating the Azure archive location.")
        return self.post('internal', '/archive/object_store', config)
