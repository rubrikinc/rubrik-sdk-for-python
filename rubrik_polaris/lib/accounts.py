""" Collection of functions that manipulate account components """

def add_account_aws(self, account_id, account_name, regions):
    """Adds AWS account to Polaris
    """
    query_name = "account_add_aws"
    variables = {
        "account_id": account_id,
        "account_name": account_name,
        "regions": regions
    }
    request = self.query(None, self.graphql_mutation[query_name], variables)
    return self._dump_nodes(request, query_name)

def get_accounts_aws(self, filter=""):
    """Retrieves AWS account information from Polaris
    """
    query_name = "accounts_aws"
    variables = {
        "filter": filter
    }
    request = self.query(None, self.graphql_query[query_name], variables)
    return self._dump_nodes(request, query_name)


def get_accounts_gcp(self, filter=""):
    """Retrieves GCP account information from Polaris

    Arguments:
        filter {str} -- Search string to filter results
    """
    query_name = "accounts_gcp"
    variables = {
        "filter": filter
    }
    request = self.query(None, self.graphql_query[query_name], variables)
    return self._dump_nodes(request, query_name)


def get_accounts_azure(self, filter=""):
    """Retrieves Azure account information from Polaris

    Arguments:
        filter {str} -- Search string to filter results
    """
    query_name = "accounts_azure"
    variables = {
        "filter": filter
    }
    request = self.query(None, self.graphql_query[query_name], variables)
    return self._dump_nodes(request, query_name)