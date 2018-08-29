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
