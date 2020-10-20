""" Collection of functions that manipulate account components """


def add_account_aws(self, regions = [], all = False, profiles = [], aws_access_key_id = None, aws_secret_access_key = None):
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
        self._add_account_aws(regions=regions, aws_id = aws_access_key_id, aws_secret = aws_secret_access_key)
    elif all or profiles:
        for profile in self._get_aws_profiles():
            if profile in profiles or all:
                self._add_account_aws(profile = profile, regions = regions)
                #TODO: Should add above into a queque for threaded provisioning

def _add_account_aws(self, regions = [], profile = '', aws_id = None, aws_secret = None, _account_id = '', _account_name = None):
    if profile:
        _aws_account_id, _aws_account_name = self.get_account_aws_native_id(profile = profile)
    elif aws_id and aws_secret:
        _aws_account_id, _aws_account_name = self.get_account_aws_native_id(aws_id = aws_id, aws_secret = aws_secret)
    _account_name_list = []
    if _aws_account_id:
        _account_name_list.append(_aws_account_id)
    else:
        return #TODO: Raise error message in return stack (FDSE-848)
    if _aws_account_name:
        _account_name_list.append(_aws_account_name)
    if profile:
        _account_name_list.append(profile)
    try:
        _query_name = "account_add_aws"
        _variables = {
            "account_id": _aws_account_id,
            "account_name": " : ".join(_account_name_list),
            "regions": regions
        }
        _request = self._query(None, self._graphql_query[_query_name], _variables)
        _nodes = self._dump_nodes(_request, _query_name)
        if _nodes['errorMessage']:
            raise Exception("Account {} already added".format(_aws_account_id))
    except Exception as e:
        print(e)
    else:
        if profile:
            _invoke_aws_stack(self, _nodes, _aws_account_id, regions = regions, profile=profile)
        elif aws_id and aws_secret:
            _invoke_aws_stack(self, _nodes, _aws_account_id, regions = regions, aws_id = aws_id, aws_secret = aws_secret)

def _get_aws_profiles(self):
    import boto3
    return boto3.session.Session().available_profiles

def _invoke_aws_stack(self, _nodes, _account_id, regions = [], profile = '', aws_id = None, aws_secret = None):
    """Invokes AWS Cloudformation configuration for Account

    Arguments:
        nodes {dict} -- nodes from add_account_aws
        account_id {str} -- account_id from add_acount_aws
    """
    import boto3 as boto3
    import botocore
    if profile:
        boto3.setup_default_session(profile_name=profile)
    elif aws_id and aws_secret:
        boto3.setup_default_session(aws_access_key_id = aws_id, aws_secret_access_key = aws_secret)
    for region in regions:
        _boto_account_id = boto3.client('sts').get_caller_identity().get('Account')
        _client = boto3.client('cloudformation', region_name = region)

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
    return

def get_accounts_aws(self, filter=""):
    """Retrieves AWS account information from Polaris

    Arguments:
        filter {str} -- Search string to filter results

    Returns:
        list -- List of AWS accounts in Polaris
    """
    try:
        _query_name = "accounts_aws"
        _variables = {
            "filter": filter
        }
        _request = self._query(None, self._graphql_query[_query_name], _variables)
        return self._dump_nodes(_request, _query_name)
    except Exception as e:
        print(e)

def get_accounts_gcp(self, filter=""):
    """Retrieves GCP account information from Polaris

    Arguments:
        filter {str} -- Search string to filter results
    
    Returns:
        list -- List of GCP accounts in Polaris
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

def get_accounts_azure(self, filter=""):
    """Retrieves Azure account information from Polaris

    Arguments:
        filter {str} -- Search string to filter results

    Returns:
        list -- List of Azure accounts in Polaris
    """
    try:
        _query_name = "accounts_azure"
        _variables = {
            "filter": filter
        }
        _request = self._query(None, self._graphql_query[_query_name], _variables)
        return self._dump_nodes(_request, _query_name)
    except Exception as e:
        print(e)

def get_accounts_aws_detail(self, filter=""):
    """Retrieves deployment details for AWS from Polaris

    Arguments:
        filter {str} -- Search AWS native account ID to filter results

    Returns:
        list -- List of AWS account details
    """
    try:
        _query_name = "accounts_aws_detail"
        _variables = {
            "filter": filter
        }
        _request = self._query(None, self._graphql_query[_query_name], _variables)
        return self._dump_nodes(_request, _query_name)
    except Exception as e:
        print(e)

def get_account_aws_native_id(self, profile = '', aws_id = None, aws_secret = None):
    """Returns AWS Account ID from local config
    
    Returns:
        str -- AWS Account ID, AWS Account Name (if applicable)
    """
    
    import boto3 as boto3
    from botocore.exceptions import ClientError
    try:
        if profile:
            boto3.setup_default_session(profile_name = profile)
        elif aws_id and aws_secret:
            boto3.setup_default_session(aws_access_key_id=aws_id, aws_secret_access_key=aws_secret)
        _boto_account_id = boto3.client('sts').get_caller_identity().get('Account')
        _boto_account_name = None
        try:
            _boto_account_name = boto3.client('organizations').describe_account(AccountId=_boto_account_id).get('Account').get('Name')
        except ClientError as e:
            if e.response['Error']['Code'] == 'AWSOrganizationsNotInUseException':
                pass
            else:
                print("Unexpected error: %s" % e)
        else:
            _boto_account_name = None
    except Exception as e:
        print("{} : {}".format(profile, e))
    return _boto_account_id, _boto_account_name;

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

def _destroy_aws_stack(self, _stack_region, _stack_name, profile = '', aws_id = None, aws_secret = None):
    """Commits  Destroy cloudformation stack (Rubrik)

    Arguments:
        stack_region {string} -- Single region name from Polaris
        stack_name {string} -- Single stack name from Polaris
    """
    import boto3, botocore
    if profile:
        boto3.setup_default_session(profile_name=profile)
    elif aws_id and aws_secret:
        boto3.setup_default_session(aws_access_key_id=aws_id, aws_secret_access_key=aws_secret)
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

def delete_account_aws(self, profiles = [], all = False, aws_access_key_id = None, aws_secret_access_key = None):
    """Commits  Delete AWS Account in Polaris, relies on local .aws
    
    Arguments:
        all {bool} -- If true import all available profiles (Default: False)
        profiles {list} -- List of explicit profiles to add
    """
    if aws_access_key_id and aws_secret_access_key:
        self._delete_account_aws(aws_id = aws_access_key_id, aws_secret = aws_secret_access_key)
    elif all or profiles:
        for profile in self._get_aws_profiles():
            if profile in profiles or all:
                self._delete_account_aws(profile = profile)

def _delete_account_aws(self, profile = '', aws_id = None, aws_secret = None):
    import re
    try:
        _account_id = None
        if profile:
            _account_id = self.get_account_aws_native_id(profile = profile)[0]
        elif aws_id and aws_secret:
            _account_id = self.get_account_aws_native_id(aws_id=aws_id, aws_secret=aws_secret)[0]
        _polaris_account_info = self.get_accounts_aws_detail(_account_id)['awsCloudAccounts'][0]
        #todo: Add exception if account does not exist in polaris
        _polaris_account_id = _polaris_account_info['awsCloudAccount']['id']
        _disable_account = self._disable_account_aws(_polaris_account_id)
        self._invoke_account_delete_aws(_polaris_account_id)
        for _feature_details in _polaris_account_info['featureDetails']:
            if _feature_details['feature'] == "CLOUD_NATIVE_PROTECTION":
                _stack_name = None
                if match := re.search(r'\/(.*)\/', _feature_details['stackArn']): # Here is the :=
                    _stack_name = match.group(1)
                for _stack_region in _feature_details['awsRegions']:
                    _stack_region = (re.sub('_', '-', _stack_region)).lower()
                    #todo: HERE
                    self._destroy_aws_stack(_stack_region, _stack_name, profile = profile, aws_id = aws_id, aws_secret = aws_secret)
        commit_delete = self._commit_account_delete_aws(_polaris_account_id)
        return
    except Exception as e:
        print("{}: {}".format("_delete_account_aws", e))

def _update_account_aws(self):
    _polaris_account_info = self.get_accounts_aws_detail(self.get_account_aws_native_id())['awsCloudAccounts'][0]
    self._pp.pprint(_polaris_account_info)

