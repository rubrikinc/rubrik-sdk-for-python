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
This module contains the Rubrik SDK Physical class.
"""

import sys
from .api import Api

_API = Api


class Physical(_API):
    """This class contains methods related to the managment of the Physical objects in the Rubrik Cluster.
    """

    def add_physical_host(self, hostname, timeout=60):
        """Add a physical host from the Rubrik Cluster.

        Arguments:
            hostname {str} -- The hostname or IP Address of the physical host you wish to add to the Rubrik Cluster.

        Keyword Arguments:
            timeout {int} -- The timeout value for the API call that adds the physical host to the Rubrik Cluster. (default: {60})

        Returns:
            str -- If the physical host is already present on the Rubrik Cluster, a message to that effect will be retuned.
            dict -- The response returned by the API call
        """

        self.log('Searching the Rubrik Cluster for the current hosts.')
        current_hosts = self.get('v1', '/host')

        for host in current_hosts['data']:
            if host['hostname'] == hostname:
                host_present = True
                return "The host '{}' is already connected to the Rubrik Cluster.".format(hostname)

        config = {}
        config['hostname'] = hostname
        config['hasAgent'] = True

        self.log("Adding the host '{}' to the Rubrik Cluster.".format(hostname))
        add_host = self.post('v1', '/host', config, timeout)

        return add_host

    def delete_physical_host(self, hostname, timeout=120):
        """Delete a physical host from the Rubrik Cluster.

        Arguments:
            hostname {str} -- The hostname or IP Address of the physical host you wish to remove from the Rubrik Cluster.

        Keyword Arguments:
            timeout {int} -- The timeout value for the API call that deletes the physical host from the Rubrik Cluster. (default: {120})

        Returns:
            str -- If the physical host is not present on the Rubrik Cluster, a message to that effect will be retuned.
            dict -- The response returned by the API call.
        """

        self.log('Searching the Rubrik Cluster for the current hosts.')
        current_hosts = self.get('v1', '/host')

        host_present = False

        for host in current_hosts['data']:
            if host['hostname'] == hostname:
                host_present = True
                host_id = host['id']
                break

        if host_present is False:
            return "The host '{}' is not connected to the Rubrik Cluster.".format(hostname)

        self.log("Deleting the host '{}' from the Rubrik Cluster.".format(hostname))
        delete_host = self.delete('v1', '/host/{}'.format(host_id), timeout)

        return delete_host
