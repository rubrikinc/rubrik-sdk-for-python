""" Collection of functions that manipulate account components """
import time
def add_account_aws(self, account_id, account_name, regions):
    """Adds AWS account to Polaris
    """
    try:
        query_name = "account_add_aws"
        variables = {
            "account_id": account_id,
            "account_name": account_name,
            "regions": regions
        }
        request = self._query(None, self._graphql_mutation[query_name], variables)
        nodes = self._dump_nodes(request, query_name)
        if nodes['errorMessage']:
            raise Exception("Account {} already added".format(account_id))
    except Exception as e:
        print(e)
    else:
        _invoke_aws_stack(self, nodes, account_id)
        return 1

def _invoke_aws_stack(self, nodes, account_id):
    """Invokes AWS Cloudformation configuration for Account

    Arguments:
        nodes {Dict} -- nodes from add_account_aws
        account_it {str} -- account_id from add_acount_aws
    """
    import boto3 as boto3
    import botocore
    boto_account_id = boto3.client('sts').get_caller_identity().get('Account')
    client = boto3.client('cloudformation')

    # Check that we're using the right profile.
    try:
        if boto_account_id != account_id:
            raise Exception("Account mismatch. Are you using the proper AWS_PROFILE?")
    except Exception as e:
        print(e)

    # add ability to use local keys
    create_stack = None
    try:
        create_stack = client.create_stack(
            StackName = nodes['cloudFormationName'],
            TemplateURL = nodes['cloudFormationTemplateUrl'],
            DisableRollback = False,
            Capabilities = ['CAPABILITY_IAM'],
            EnableTerminationProtection = False
        )
    except Exception as e:
        print('Stack creation failed with error:\n  {}'.format(str(e)))

    waiter = client.get_waiter('stack_create_complete')
    try:
        waiter.wait(StackName = create_stack['StackId'])
    except botocore.exceptions.WaiterError as e:
        print(e)
    else:
        return

def get_accounts_aws(self, filter=""):
    """Retrieves AWS account information from Polaris
    """
    try:
        query_name = "accounts_aws"
        variables = {
            "filter": filter
        }
        request = self._query(None, self._graphql_query[query_name], variables)
        return self._dump_nodes(request, query_name)
    except Exception as e:
        print(e)

def get_accounts_gcp(self, filter=""):
    """Retrieves GCP account information from Polaris

    Arguments:
        filter {str} -- Search string to filter results
    """
    try:
        query_name = "accounts_gcp"
        variables = {
            "filter": filter
        }
        request = self._query(None, self._graphql_query[query_name], variables)
        return self._dump_nodes(request, query_name)
    except Exception as e:
        print(e)

def get_accounts_azure(self, filter=""):
    """Retrieves Azure account information from Polaris

    Arguments:
        filter {str} -- Search string to filter results
    """
    try:
        query_name = "accounts_azure"
        variables = {
            "filter": filter
        }
        request = self._query(None, self._graphql_query[query_name], variables)
        return self._dump_nodes(request, query_name)
    except Exception as e:
        print(e)

def get_accounts_aws_detail(self, filter = ""):
    """Retrieves deployment details for AWS from Polaris

    Arguments:
        filter {str} -- Search aws native account ID to filter results
    """
    try:
        query_name = "accounts_aws_detail"
        variables = {
            "filter": filter
        }
        request = self._query(None, self._graphql_query[query_name], variables)
        return self._dump_nodes(request, query_name)
    except Exception as e:
        print(e)

def get_account_aws_native_id(self):
    import boto3 as boto3
    try:
        boto_account_id = boto3.client('sts').get_caller_identity().get('Account')
        return boto_account_id
    except Exception as e:
        print(e)

def _disable_account_aws(self, _polaris_account_id):
    """Disables AWS Account in Polaris

    Arguments:
        aws_account_id {str} -- Account ID to disable in Polaris
    """
    try:
        _query_name = "account_disable_aws"
        _variables = {
            "polaris_account_id": _polaris_account_id
        }
        _request = self._query(None, self._graphql_mutation[_query_name], _variables)
        _monitor = self._monitor_task(self._dump_nodes(_request, _query_name))
        self._pp.pprint(_monitor)
        if _monitor['status'] == 'SUCCEEDED':
            return 1
        else:
            raise Exception("Failed to disable account")
        return _monitor
    except Exception as e:
        print(e)

def _invoke_account_delete_aws(self, polaris_account_id):
    """Invokes initiation of Delete AWS Account in Polaris

    Arguments:
        aws_account_id {str} -- Account ID to initiate delete in Polaris
    """
    try:
        query_name = "account_delete_initiate_aws"
        variables = {
            "polaris_account_id": polaris_account_id
        }
        request = self._query(None, self._graphql_mutation[query_name], variables)
        return self._dump_nodes(request, query_name)
    except Exception as e:
        print(e)


def _commit_account_delete_aws(self, polaris_account_id):
    """Commits  Delete AWS Account in Polaris

    Arguments:
        aws_account_id {str} -- Account ID to initiate delete in Polaris
    """
    try:
        query_name = "account_delete_commit_aws"
        variables = {
            "polaris_account_id": polaris_account_id
        }
        request = self._query(None, self._graphql_mutation[query_name], variables)
        return self._dump_nodes(request, query_name)
    except Exception as e:
        print(e)

def _destroy_aws_stack(self, stack_region, stack_name):
    import boto3, botocore
    client = boto3.client('cloudformation', region_name = stack_region)
    try:
        self.delete_stack = client.delete_stack(StackName = stack_name)
    except Exception as e:
        print('Stack deletion failed with error:\n  {}').format(str(e))

    waiter = client.get_waiter('stack_delete_complete')

    try:
        waiter.wait(StackName = stack_name)
    except botocore.exceptions.WaiterError as e:
        print('Failed to delete stack: {}').format(stack_name)
        print('{}'.format(e))
    else:
        return

def delete_account_aws(self):
    import re
    try:
        aws_account_id = self.get_account_aws_native_id()
        polaris_account_info = self.get_accounts_aws_detail(aws_account_id)['awsCloudAccounts'][0]
        polaris_account_id = polaris_account_info['awsCloudAccount']['id']
        disable_account = self._disable_account_aws(polaris_account_id)
        self._invoke_account_delete_aws(polaris_account_id)
        for feature_details in polaris_account_info['featureDetails']:
            if feature_details['feature'] == "CLOUD_NATIVE_PROTECTION":
                stack_name = None
                if match := re.search(r'\/(.*)\/', feature_details['stackArn']):
                    stack_name = match.group(1)
                for stack_region in feature_details['awsRegions']:
                    stack_region = (re.sub('_', '-', stack_region)).lower()
                    self._destroy_aws_stack(stack_region, stack_name)
        commit_delete = self._commit_account_delete_aws(polaris_account_id)
        return 1
    except Exception as e:
        print(e)


