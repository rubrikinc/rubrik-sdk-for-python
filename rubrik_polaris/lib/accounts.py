# Copyright 2020 Rubrik, Inc.
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
Collection of functions that manipulate account components.
"""


def add_account_aws(self, regions=[], all=False, profiles=[], aws_access_key_id=None, aws_secret_access_key=None):
    """Adds AWS account to Polaris

    Arguments:
        regions {list} -- List of AWS regions to configure
        all {bool} -- If true import all available profiles (Default: False)
        profiles {list} -- List of explicit profiles to add
        aws_access_key_id {str} -- AWS Access Key ID
        aws_secret_access_key {str} -- AWS Access Key Secret

    Returns:
        bool -- `True` if the account was added successfully, otherwise `False`.
    """
    if aws_access_key_id and aws_secret_access_key:
        self._add_account_aws(regions=regions, aws_id=aws_access_key_id, aws_secret=aws_secret_access_key)
    elif all or profiles:
        for profile in self._get_aws_profiles():
            if profile in profiles or (all and profile != 'default'):
                self._add_account_aws(profile = profile, regions = regions)
                #TODO: Should add above into a queque for threaded provisioning


def _add_account_aws(self, regions=[], profile='', aws_id=None, aws_secret=None):
    aws_account_id = None
    aws_account_name = None

    if profile:
        aws_account_id, aws_account_name = self.get_account_aws_native_id(profile=profile)
    elif aws_id and aws_secret:
        aws_account_id, aws_account_name = self.get_account_aws_native_id(aws_id=aws_id, aws_secret=aws_secret)

    account_name_list = []
    if aws_account_id:
        account_name_list.append(aws_account_id)
    else:
        return # TODO: Raise error message in return stack (FDSE-848)

    if aws_account_name:
        account_name_list.append(aws_account_name)
    if profile:
        account_name_list.append(profile)

    try:
        query_name = "accounts_aws_add"
        variables = {
            "account_id": aws_account_id,
            "account_name": " : ".join(account_name_list),
            "regions": regions
        }
        request = self._query(query_name, variables)
        nodes = self._dump_nodes(request)
        if nodes['errorMessage']:
            raise Exception("Account {} already added".format(aws_account_id))
    except Exception:
        raise

    else:
        if profile:
            _invoke_aws_stack(self, nodes, aws_account_id, regions=regions, profile=profile)
        elif aws_id and aws_secret:
            _invoke_aws_stack(self, nodes, aws_account_id, regions=regions, aws_id=aws_id, aws_secret=aws_secret)


def _get_aws_profiles(self):
    import boto3
    return boto3.session.Session().available_profiles


def _invoke_aws_stack(self, nodes, account_id, regions=[], profile='', aws_id=None, aws_secret=None):
    """Invokes AWS Cloudformation configuration for Account

    Arguments:
        nodes {dict} -- nodes from add_account_aws
        account_id {str} -- account_id from add_account_aws
    """
    import boto3 as boto3
    from botocore.exceptions import WaiterError

    if profile:
        boto3.setup_default_session(profile_name=profile)
    elif aws_id and aws_secret:
        boto3.setup_default_session(aws_access_key_id=aws_id, aws_secret_access_key=aws_secret)

    for region in regions:
        boto_account_id = boto3.client('sts').get_caller_identity().get('Account')
        client = boto3.client('cloudformation', region_name=region)

        if boto_account_id != account_id:
            raise Exception("Account mismatch. Are you using the proper AWS_PROFILE?")

        # Add ability to use local keys
        try:
            create_stack = client.create_stack(
                StackName=nodes['cloudFormationName'],
                TemplateURL=nodes['cloudFormationTemplateUrl'],
                DisableRollback=False,
                Capabilities=['CAPABILITY_IAM'],
                EnableTerminationProtection=False
            )
        except Exception as e:
            raise Exception('Stack creation failed with error:\n {}'.format(str(e)))

        waiter = client.get_waiter('stack_create_complete')
        try:
            waiter.wait(StackName=create_stack['StackId'])
        except WaiterError:
            raise


def get_accounts_aws(self, filter=""):
    """Retrieves AWS account information from Polaris

    Arguments:
        filter {str} -- Search string to filter results

    Returns:
        list -- List of AWS accounts in Polaris
    """
    try:
        query_name = "accounts_aws"
        variables = {
            "filter": filter
        }
        request = self._query(query_name, variables)
        return self._dump_nodes(request)
    except Exception:
        raise


def get_accounts_gcp(self, filter=""):
    """Retrieves GCP account information from Polaris

    Arguments:
        filter {str} -- Search string to filter results
    
    Returns:
        list -- List of GCP accounts in Polaris
    """
    try:
        query_name = "accounts_gcp"
        variables = {
            "filter": filter
        }
        request = self._query(query_name, variables)
        return self._dump_nodes(request)
    except Exception:
        raise


def get_accounts_azure(self, filter=""):
    """Retrieves Azure account information from Polaris

    Arguments:
        filter {str} -- Search string to filter results

    Returns:
        list -- List of Azure accounts in Polaris
    """
    try:
        query_name = "accounts_azure"
        variables = {
            "filter": filter
        }
        request = self._query(query_name, variables)
        return self._dump_nodes(request)
    except Exception:
        raise


def get_accounts_aws_detail(self, filter=""):
    """Retrieves deployment details for AWS from Polaris

    Arguments:
        filter {str} -- Search AWS native account ID to filter results

    Returns:
        list -- List of AWS account details
    """
    try:
        query_name = "accounts_aws_detail"
        variables = {
            "filter": filter
        }
        request = self._query(query_name, variables)
        return self._dump_nodes(request)
    except Exception:
        raise


def get_account_aws_native_id(self, profile='', aws_id=None, aws_secret=None):
    """Returns AWS Account ID from local config
    
    Returns:
        str -- AWS Account ID, AWS Account Name (if applicable)
    """
    import boto3 as boto3
    from botocore.exceptions import ClientError
    from rubrik_polaris.exceptions import PolarisException

    try:
        if profile:
            boto3.setup_default_session(profile_name = profile)
        elif aws_id and aws_secret:
            boto3.setup_default_session(aws_access_key_id=aws_id, aws_secret_access_key=aws_secret)
        try:
            _boto_account_id = boto3.client('sts').get_caller_identity().get('Account')
        except ClientError as e:
            print("Boto Error: {}".format(e))
        _boto_account_name = None
        try:
            boto_account_name = boto3.client('organizations').describe_account(AccountId=boto_account_id).get('Account').get('Name')
        except ClientError as e:
            if e.response['Error']['Code'] == 'AWSOrganizationsNotInUseException':
                pass
            else:
                raise PolarisException("Unexpected error: %s" % e)
        return boto_account_id, boto_account_name
    except PolarisException:
        raise


def _disable_account_aws(self, polaris_account_id):
    """Disables AWS Account in Polaris

    Arguments:
        polaris_account_id {str} -- Account ID to disable in Polaris
    """
    try:
        query_name = "accounts_aws_disable"
        variables = {
            "polaris_account_id": polaris_account_id
        }
        request = self._query(query_name, variables)

        monitor = self._monitor_task(self._dump_nodes(request))
        if monitor['status'] != 'SUCCEEDED':
            raise Exception("Failed to disable account")
    except Exception:
        raise


def _invoke_account_delete_aws(self, polaris_account_id):
    """Invokes initiation of Delete AWS Account in Polaris

    Arguments:
        polaris_account_id {str} -- Account ID to initiate delete in Polaris
    """
    try:
        query_name = "accounts_aws_delete_initiate"
        variables = {
            "polaris_account_id": polaris_account_id
        }
        request = self._query(query_name, variables)
        return self._dump_nodes(request)
    except Exception:
        raise


def _commit_account_delete_aws(self, polaris_account_id):
    """Commits  Delete AWS Account in Polaris

    Arguments:
        polaris_account_id {str} -- Account ID to commit delete in Polaris
    """
    try:
        query_name = "accounts_aws_delete_commit"
        variables = {
            "polaris_account_id": polaris_account_id
        }
        request = self._query(query_name, variables)
        return self._dump_nodes(request)
    except Exception:
        raise


def _destroy_aws_stack(self, stack_region, stack_name, profile='', aws_id=None, aws_secret=None):
    """Commits  Destroy cloudformation stack (Rubrik)

    Arguments:
        stack_region {string} -- Single region name from Polaris
        stack_name {string} -- Single stack name from Polaris
    """
    import boto3
    from botocore.exceptions import WaiterError

    if profile:
        boto3.setup_default_session(profile_name=profile)
    elif aws_id and aws_secret:
        boto3.setup_default_session(aws_access_key_id=aws_id, aws_secret_access_key=aws_secret)

    client = boto3.client('cloudformation', region_name=stack_region)
    try:
        self.delete_stack = client.delete_stack(StackName=stack_name)
    except Exception as e:
        print('Stack deletion failed with error:\n  {}'.format(str(e)))

    waiter = client.get_waiter('stack_delete_complete')

    try:
        waiter.wait(StackName=stack_name)
    except WaiterError as e:
        raise Exception('Failed to delete stack: {}\n{}'.format(stack_name, e))
    else:
        return


def delete_account_aws(self, profiles=[], all=False, aws_access_key_id=None, aws_secret_access_key=None):
    """Commits  Delete AWS Account in Polaris, relies on local .aws
    
    Arguments:
        all {bool} -- If true import all available profiles (Default: False)
        profiles {list} -- List of explicit profiles to add
        aws_access_key_id {str} -- AWS Access Key ID
        aws_secret_access_key {str} -- AWS Access Key Secret
    """
    if aws_access_key_id and aws_secret_access_key:
        self._delete_account_aws(aws_id=aws_access_key_id, aws_secret=aws_secret_access_key)
    elif all or profiles:
        for profile in self._get_aws_profiles():
            if profile in profiles or (all and profile != 'default'):
                self._delete_account_aws(profile = profile)


def _delete_account_aws(self, profile='', aws_id=None, aws_secret=None):
    import re

    try:
        account_id = None
        if profile:
            account_id = self.get_account_aws_native_id(profile=profile)[0]
        elif aws_id and aws_secret:
            account_id = self.get_account_aws_native_id(aws_id=aws_id, aws_secret=aws_secret)[0]

        polaris_account_info = self.get_accounts_aws_detail(account_id)['awsCloudAccounts'][0]
        # TODO: Add exception if account does not exist in polaris
        polaris_account_id = polaris_account_info['awsCloudAccount']['id']
        self._disable_account_aws(polaris_account_id)
        self._invoke_account_delete_aws(polaris_account_id)

        for feature_details in polaris_account_info['featureDetails']:
            if feature_details['feature'] == "CLOUD_NATIVE_PROTECTION":
                stack_name = None
                if match := re.search(r'/(.*)/', feature_details['stackArn']):
                    stack_name = match.group(1)
                for stack_region in feature_details['awsRegions']:
                    stack_region = (re.sub('_', '-', stack_region)).lower()
                    self._destroy_aws_stack(stack_region, stack_name, profile=profile, aws_id=aws_id, aws_secret=aws_secret)

        self._commit_account_delete_aws(polaris_account_id)
    except Exception as e:
        raise Exception("{}: {}".format("_delete_account_aws", e))


def update_account_aws(self, regions=[], all=False, profiles=[], aws_access_key_id=None, aws_secret_access_key=None):
    """Updates AWS account if configured in Polaris

    Arguments:
        all {bool} -- If true import all available profiles (Default: False)
        profiles {list} -- List of explicit profiles to add
        aws_access_key_id {str} -- AWS Access Key ID
        aws_secret_access_key {str} -- AWS Access Key Secret

    Returns:
        bool -- `True` if the account was added successfully, otherwise `False`.
    """
    if aws_access_key_id and aws_secret_access_key:
        self._update_account_aws(aws_id=aws_access_key_id, aws_secret=aws_secret_access_key)
    elif all or profiles:
        for profile in self._get_aws_profiles():
            if profile in profiles or (all and profile != 'default'):
                self._update_account_aws(profile=profile)

def _update_account_aws_initiate(self, _feature, _polaris_account_id):
    try:
        _query_name = "accounts_aws_update_initiate"
        _variables = {
            "polaris_account_id": _polaris_account_id,
            "aws_native_protection_feature": [_feature]
        }
        self._pp.pprint(_variables)
        _request = self._query(_query_name, _variables)
        return self._dump_nodes(_request, _query_name)
    except Exception as e:
        print(e)

def _update_account_aws(self, profile=None, aws_id=None, aws_secret=None,  _aws_account_id = '', _aws_account_name = None):
    if profile:
        _aws_account_id, _aws_account_name = self.get_account_aws_native_id(profile = profile)
    elif aws_id and aws_secret:
        _aws_account_id, _aws_account_name = self.get_account_aws_native_id(aws_id = aws_id, aws_secret = aws_secret)
    if _aws_account_id  == '':
        return
    else:
        _polaris_account_info = self.get_accounts_aws_detail(_aws_account_id)['awsCloudAccounts']
        if not _polaris_account_info:
            return
        for _feature in _polaris_account_info[0]['featureDetails']:
            if _feature['feature'] == "CLOUD_NATIVE_PROTECTION":
                if _feature['status'] == 'MISSING_PERMISSIONS':
                    _update_info = self._update_account_aws_initiate(_feature['feature'], _polaris_account_info[0]['awsCloudAccount']['id'])
                    self._pp.pprint(_update_info)
                if _feature['status'] == 'DISCONNECTED':
                    print("account needs to be recreated")
