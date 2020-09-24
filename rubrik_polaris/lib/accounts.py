""" Collection of functions that manipulate account components """

def add_account_aws(self, _account_id, _account_name, _regions):
    """Adds AWS account to Polaris

    Arguments:
        _account_id {string} -- AWS account id to add
        _account_name {str} -- Friendly name for account in Polaris
        _regions {list} -- List of AWS regions to configure
    """
    try:
        _query_name = "account_add_aws"
        _variables = {
            "account_id": _account_id,
            "account_name": _account_name,
            "regions": _regions
        }
        _request = self._query(None, self._graphql_query[_query_name], _variables)
        _nodes = self._dump_nodes(_request, _query_name)
        if _nodes['errorMessage']:
            raise Exception("Account {} already added".format(_account_id))
    except Exception as e:
        print(e)
    else:
        _invoke_aws_stack(self, _nodes, _account_id)
        return 1

def _invoke_aws_stack(self, _nodes, _account_id):
    """Invokes AWS Cloudformation configuration for Account

    Arguments:
        nodes {dict} -- nodes from add_account_aws
        account_it {str} -- account_id from add_acount_aws
    """
    import boto3 as boto3
    import botocore
    _boto_account_id = boto3.client('sts').get_caller_identity().get('Account')
    _client = boto3.client('cloudformation')

    # Check that we're using the right profile.
    try:
        if _boto_account_id != _account_id:
            raise Exception("Account mismatch. Are you using the proper AWS_PROFILE?")
    except Exception as e:
        print(e)

    # add ability to use local keys
    _create_stack = None
    try:
        _create_stack = _client.create_stack(
            StackName = _nodes['cloudFormationName'],
            TemplateURL = _nodes['cloudFormationTemplateUrl'],
            DisableRollback = False,
            Capabilities = ['CAPABILITY_IAM'],
            EnableTerminationProtection = False
        )
    except Exception as e:
        print('Stack creation failed with error:\n  {}'.format(str(e)))

    _waiter = _client.get_waiter('stack_create_complete')
    try:
        _waiter.wait(StackName = _create_stack['StackId'])
    except botocore.exceptions.WaiterError as e:
        print(e)
    else:
        return

def get_accounts_aws(self, _filter=""):
    """Retrieves AWS account information from Polaris

    Arguments:
        filter {str} -- Search string to filter results
    """
    try:
        _query_name = "accounts_aws"
        _variables = {
            "filter": _filter
        }
        _request = self._query(None, self._graphql_query[_query_name], _variables)
        return self._dump_nodes(_request, _query_name)
    except Exception as e:
        print(e)

def get_accounts_gcp(self, _filter=""):
    """Retrieves GCP account information from Polaris

    Arguments:
        filter {str} -- Search string to filter results
    """
    try:
        _query_name = "accounts_gcp"
        _variables = {
            "filter": filter
        }
        _request = self._query(None, self._graphql_query[_query_name], _variables)
        return self._dump_nodes(_request, _query_name)
    except Exception as e:
        print(e)

def get_accounts_azure(self, _filter=""):
    """Retrieves Azure account information from Polaris

    Arguments:
        filter {str} -- Search string to filter results
    """
    try:
        _query_name = "accounts_azure"
        _variables = {
            "filter": _filter
        }
        _request = self._query(None, self._graphql_query[_query_name], _variables)
        return self._dump_nodes(_request, _query_name)
    except Exception as e:
        print(e)

def get_accounts_aws_detail(self, _filter = ""):
    """Retrieves deployment details for AWS from Polaris

    Arguments:
        filter {str} -- Search aws native account ID to filter results
    """
    try:
        _query_name = "accounts_aws_detail"
        _variables = {
            "filter": _filter
        }
        _request = self._query(None, self._graphql_query[_query_name], _variables)
        return self._dump_nodes(_request, _query_name)
    except Exception as e:
        print(e)

def get_account_aws_native_id(self):
    """Returns AWS Account ID from local config"""
    import boto3 as boto3
    try:
        _boto_account_id = boto3.client('sts').get_caller_identity().get('Account')
        return _boto_account_id
    except Exception as e:
        print(e)

def _disable_account_aws(self, _polaris_account_id):
    """Disables AWS Account in Polaris

    Arguments:
        _polaris_account_id {str} -- Account ID to disable in Polaris
    """
    try:
        _query_name = "account_disable_aws"
        _variables = {
            "polaris_account_id": _polaris_account_id
        }
        _request = self._query(None, self._graphql_query[_query_name], _variables)
        _monitor = self._monitor_task(self._dump_nodes(_request, _query_name))
        if _monitor['status'] == 'SUCCEEDED':
            return 1
        else:
            raise Exception("Failed to disable account")
        return _monitor
    except Exception as e:
        print(e)

def _invoke_account_delete_aws(self, _polaris_account_id):
    """Invokes initiation of Delete AWS Account in Polaris

    Arguments:
        polaris_account_id {str} -- Account ID to initiate delete in Polaris
    """
    try:
        _query_name = "account_delete_initiate_aws"
        _variables = {
            "polaris_account_id": _polaris_account_id
        }
        _request = self._query(None, self._graphql_query[_query_name], _variables)
        return self._dump_nodes(_request, _query_name)
    except Exception as e:
        print(e)


def _commit_account_delete_aws(self, _polaris_account_id):
    """Commits  Delete AWS Account in Polaris

    Arguments:
        polaris_account_id {str} -- Account ID to commit delete in Polaris
    """
    try:
        _query_name = "account_delete_commit_aws"
        _variables = {
            "polaris_account_id": _polaris_account_id
        }
        _request = self._query(None, self._graphql_query[_query_name], _variables)
        return self._dump_nodes(_request, _query_name)
    except Exception as e:
        print(e)

def _destroy_aws_stack(self, _stack_region, _stack_name):
    """Commits  Destroy cloudformation stack (Rubrik)

    Arguments:
        stack_region {string} -- Single region name from Polaris
        stack_name {string} -- Single stack name from Polaris
    """
    import boto3, botocore
    _client = boto3.client('cloudformation', region_name = _stack_region)
    try:
        self.delete_stack = _client.delete_stack(StackName = _stack_name)
    except Exception as e:
        print('Stack deletion failed with error:\n  {}').format(str(e))

    _waiter = _client.get_waiter('stack_delete_complete')

    try:
        _waiter.wait(StackName = _stack_name)
    except botocore.exceptions.WaiterError as e:
        print('Failed to delete stack: {}').format(_stack_name)
        print('{}'.format(e))
    else:
        return

def delete_account_aws(self):
    """Commits  Delete AWS Account in Polaris, relies on local .aws"""
    import re
    try:
        _polaris_account_info = self.get_accounts_aws_detail(self.get_account_aws_native_id())['awsCloudAccounts'][0]
        _polaris_account_id = _polaris_account_info['awsCloudAccount']['id']
        _disable_account = self._disable_account_aws(_polaris_account_id)
        self._invoke_account_delete_aws(_polaris_account_id)
        for _feature_details in _polaris_account_info['featureDetails']:
            if _feature_details['feature'] == "CLOUD_NATIVE_PROTECTION":
                _stack_name = None
                if match := re.search(r'\/(.*)\/', _feature_details['stackArn']):
                    _stack_name = match.group(1)
                for _stack_region in _feature_details['awsRegions']:
                    _stack_region = (re.sub('_', '-', _stack_region)).lower()
                    self._destroy_aws_stack(_stack_region, _stack_name)
        commit_delete = self._commit_account_delete_aws(_polaris_account_id)
        return 1
    except Exception as e:
        print(e)


