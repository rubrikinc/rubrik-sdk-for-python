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

import os
import pprint
import urllib3

from .exceptions import InvalidParameterException


class PolarisClient:
    # Public
    from .lib.common.polaris import get_sla_domains, submit_on_demand, submit_assign_sla, get_task_status
    from .lib.common.polaris import get_snapshots
    from .lib.accounts import get_accounts_azure, get_accounts_gcp
    from .lib.accounts import get_accounts_aws, get_accounts_aws_detail, get_account_aws_native_id
    from .lib.accounts import add_account_aws, delete_account_aws
    from .lib.compute import get_object_ids_azure, get_object_ids_ec2, get_object_ids_gce
    from .lib.compute import get_instances_azure, get_instances_ec2, get_instances_gce
    from .lib.compute import submit_restore_ec2, submit_restore_azure, submit_restore_gce

    # Private
    from .lib.common.connection import _query, _get_access_token
    from .lib.compute import _submit_instance_restore
    from .lib.common.monitor import _monitor_job, _monitor_threader, _monitor_task
    from .lib.common.graphql import _dump_nodes, _get_query_names_from_graphql_query
    from .lib.accounts import _invoke_account_delete_aws, _invoke_aws_stack, _commit_account_delete_aws
    from .lib.accounts import _destroy_aws_stack, _disable_account_aws, _get_aws_profiles, _add_account_aws, _delete_account_aws


    def __init__(self, _domain=None, _username=None, _password=None, **kwargs):
        from .lib.common.graphql import _build_graphql_maps

        self._pp = pprint.PrettyPrinter(indent=4)

        # Set credentials
        self._domain = self._get_cred('rubrik_polaris_domain', _domain)
        self._username = self._get_cred('rubrik_polaris_username', _username)
        self._password = self._get_cred('rubrik_polaris_password', _password)

        if not (self._domain and self._username and self._password):
            raise Exception('Error: Required credentials are missing! Please pass in username, password and domain, directly or through the OS environment.')

        # Set base variables
        self._kwargs = kwargs
        self._data_path = "{}/graphql/".format(os.path.dirname(os.path.realpath(__file__)))

        # Switch off SSL checks if needed
        if 'insecure' in self._kwargs and self._kwargs['insecure']:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Adjust Polaris domain if a custom root is defined
        if 'root_domain' in self._kwargs and self._kwargs['root_domain'] is not None:
            self._baseurl = "https://{}.{}/api/graphql".format(self._domain, self._kwargs['root_domain'])
        else:
            self._baseurl = "https://{}.my.rubrik.com/api/graphql".format(self._domain)

        # Get Auth Token and assemble header
        self._access_token = self._get_access_token()
        del(self._username, self._password)
        self._headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self._access_token
        }

        # Get graphql content
        (self._graphql_query, self._graphql_file_type_map) = _build_graphql_maps(self)

    def _get_cred(self, env_key, override=None):
        cred = None

        if env_key in os.environ:
            cred = os.environ[env_key]

        if override:
            cred = override

        return cred
