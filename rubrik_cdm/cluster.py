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
    """This class contains methods related to the managment of the Rubrik cluster itself.
    """

    def cluster_version(self, timeout=15):
        """Retrieves the software version of the Rubrik cluster.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            str -- The version of CDM installed on the Rubrik cluster.
        """

        self.log('cluster_version: Getting the software version of the Rubrik cluster.')
        return self.get('v1', '/cluster/me/version', timeout)['version']

    def cluster_node_ip(self, timeout=15):
        """Retrive the IP Address for each node in the Rubrik cluster.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            list -- A list that contains the IP Address for each node in the Rubrik cluster.
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
            object_name {str} -- The name of the object you wish to grant the `end_user` authorization to.
            end_user {str} -- The name of the end user you wish to grant authorization to.

        Keyword Arguments:
            object_type {str} -- The Rubrik object type you wish to backup. (default: {vmware}) (choices: {vmware})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            str -- No change required. The End User "`end_user`" is already authorized to interact with the "`object_name`" VM.
            dict -- The API response from `POST /internal/authorization/role/end_user`.
        """

        valid_object_type = ['vmware']

        if object_type not in valid_object_type:
            sys.exit("Error: The end_user_authorization() object_type argument must be one of the following: {}.".format(
                valid_object_type))

        self.log("end_user_authorization: Searching the Rubrik cluster for the vSphere VM '{}'.".format(object_name))
        vm_id = self.object_id(object_name, object_type)

        self.log("end_user_authorization: Searching the Rubrik cluster for the End User '{}'.".format(end_user))
        user = self.get('internal', '/user?username={}'.format(end_user))

        if not user:
            sys.exit('The Rubrik cluster does not contain a End User account named "{}".'.format(end_user))
        else:
            user_id = user[0]['id']

        self.log("end_user_authorization: Searching the Rubrik cluster for the End User '{}' authorizations.".format(end_user))
        user_authorization = self.get('internal', '/authorization/role/end_user?principals={}'.format(user_id))

        authorized_objects = user_authorization['data'][0]['privileges']['restore']

        if vm_id in authorized_objects:
            return 'No change required. The End User "{}" is already authorized to interact with the "{}" VM.'.format(end_user, object_name)
        else:
            config = {}
            config['principals'] = [user_id]
            config['privileges'] = {"restore": [vm_id]}

            return self.post('internal', '/authorization/role/end_user', config, timeout=timeout)

    def add_vcenter(self, vcenter_ip, vcenter_username, vcenter_password, vm_linking=True, ca_certificate=None, timeout=30):
        """Add a new vCenter to the Rubrik cluster.

        Arguments:
            vcenter_ip {str} -- The IP address or FQDN of the vCenter you wish to add.
            vcenter_username {str} -- The vCenter username used for authentication.
            vcenter_password {str} -- The vCenter password used for authentication.

        Keyword Arguments:
            vm_linking {bool} -- Automatically link discovered virtual machines (i.e VM Linking). (default: {True})
            ca_certificate {str} -- CA certificiate used to perform TLS certificate validation (default: {None})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {30})

        Returns:
            str -- No change required. The vCenter '`vcenter_ip`' has already been added to the Rubrik cluster.
            tuple -- The full API response for `POST /v1/vmware/vcenter` and the job status URL which can be used to monitor progress of the adding the vCenter to the Rubrik cluster. (api_response, job_status_url)
        """

        self.log("add_vcenter: Searching the Rubrik cluster for the vCenter '{}'.".format(vcenter_ip))
        current_vcenter = self.get("v1", "/vmware/vcenter?primary_cluster_id=local")

        for vcenter in current_vcenter["data"]:
            if vcenter["hostname"] == vcenter_ip:
                return "No change required. The vCenter '{}' has already been added to the Rubrik cluster.".format(vcenter_ip)

        config = {}
        config["hostname"] = vcenter_ip
        config["username"] = vcenter_username
        config["password"] = vcenter_password
        if vm_linking is True:
            config["conflictResolutionAuthz"] = "AllowAutoConflictResolution"
        elif vm_linking is False:
            config["conflictResolutionAuthz"] = "NoConflictResolution"
        if ca_certificate is not None:
            config["caCerts"] = ca_certificate

        self.log("add_vcenter: Adding vCenter '{}' to the Rubrik cluster.".format(vcenter_ip))
        add_vcenter = self.post("v1", "/vmware/vcenter", config, timeout)

        return add_vcenter, add_vcenter['links'][0]['href']

    def cluster_timezone(self, timezone):
        """Configure the Rubrik cluster timezone.

        Arguments:
            timezone {str} -- The timezone you wish the Rubrik cluster to use. (choices: {America/Anchorage, America/Araguaina, America/Barbados, America/Chicago, America/Denver, America/Los_Angeles, America/Mexico_City, America/New_York, America/Noronha, America/Phoenix, America/Toronto, America/Vancouver, Asia/Bangkok, Asia/Dhaka, Asia/Dubai, Asia/Hong_Kong, Asia/Karachi, Asia/Kathmandu, Asia/Kolkata, Asia/Magadan, Asia/Singapore, Asia/Tokyo, Atlantic/Cape_Verde, Australia/Perth, Australia/Sydney, Europe/Amsterdam, Europe/Athens, Europe/London, Europe/Moscow, Pacific/Auckland, Pacific/Honolulu, Pacific/Midway, UTC})

        Returns:
            str -- No change required. The Rubrik cluster is already configured with '`timezone`' as it's timezone.
            dict -- The full API response for `PATCH /v1//cluster/me'`
        """

        valid_timezones = ['America/Anchorage', 'America/Araguaina', 'America/Barbados', 'America/Chicago', 'America/Denver', 'America/Los_Angeles', 'America/Mexico_City', 'America/New_York', 'America/Noronha', 'America/Phoenix', 'America/Toronto', 'America/Vancouver', 'Asia/Bangkok', 'Asia/Dhaka', 'Asia/Dubai',
                           'Asia/Hong_Kong', 'Asia/Karachi', 'Asia/Kathmandu', 'Asia/Kolkata', 'Asia/Magadan', 'Asia/Singapore', 'Asia/Tokyo', 'Atlantic/Cape_Verde', 'Australia/Perth', 'Australia/Sydney', 'Europe/Amsterdam', 'Europe/Athens', 'Europe/London', 'Europe/Moscow', 'Pacific/Auckland', 'Pacific/Honolulu', 'Pacific/Midway', 'UTC']

        if timezone not in valid_timezones:
            sys.exit("Error: The timezone argument must be one of the following: {}.".format(valid_timezones))

        self.log("cluster_timezone: Determing the current cluster timezone")
        cluster_summary = self.get("v1", "/cluster/me")

        if cluster_summary["timezone"]["timezone"] == timezone:
            return "No change required. The Rubrik cluster is already configured with '{}' as it's timezone.".format(timezone)

        config = {}
        config["timezone"] = {}
        config["timezone"]["timezone"] = timezone

        self.log("cluster_timezone: Configuring the Rubrik cluster timezone")
        return self.patch("v1", "/cluster/me", config)

    def cluster_ntp(self, ntp_server):
        """Configure the Rubrik cluster timezone.

        Arguments:
            ntp_server {list} -- A list of the NTP server(s) you wish to configure the Rubrik cluster to use.

        Returns:
            str -- No change required. The NTP server(s) `ntp_server` has already been added to the Rubrik cluster.
            dict -- {'status_code': 204}
        """

        if isinstance(ntp_server, list) is False:
            sys.exit("Error: The 'ntp_server' argument must be a list object.")

        self.log("cluster_ntp: Determing the current cluster NTP settings")
        cluster_ntp = self.get("internal", "/cluster/me/ntp_server")

        if sorted(cluster_ntp["data"]) == sorted(ntp_server):
            return "No change required. The NTP server(s) {} has already been added to the Rubrik cluster.".format(ntp_server)

        self.log("cluster_ntp: Adding the NTP server(s) '{}' to the Rubrik cluster.".format(ntp_server))
        return self.post("internal", "/cluster/me/ntp_server", ntp_server)
