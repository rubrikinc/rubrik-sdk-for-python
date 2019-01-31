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

        self.log(
            'cluster_version: Getting the software version of the Rubrik cluster.')
        return self.get('v1', '/cluster/me/version', timeout=timeout)['version']

    def cluster_node_ip(self, timeout=15):
        """Retrive the IP Address for each node in the Rubrik cluster.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            list -- A list that contains the IP Address for each node in the Rubrik cluster.
        """

        self.log('cluster_node_ip: Generating a list of all Cluster Node IPs.')
        api_request = self.get('internal', '/cluster/me/node', timeout=timeout)

        node_ip_list = []

        for node in api_request['data']:
            node_ip_list.append(node["ipAddress"])

        return node_ip_list

    def cluster_node_name(self, timeout=15):
        """Retrive the name of each node in the Rubrik cluster.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            list -- A list that contains the name of each node in the Rubrik cluster.
        """

        self.log('cluster_node_ip: Generating a list of all Cluster')
        api_request = self.get('internal', '/cluster/me/node', timeout=timeout)

        node_ip_name = []

        for node in api_request['data']:
            node_ip_name.append(node["id"])

        return node_ip_name

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
            dict -- The full API response from `POST /internal/authorization/role/end_user`.
        """

        valid_object_type = ['vmware']

        if object_type not in valid_object_type:
            sys.exit("Error: The end_user_authorization() object_type argument must be one of the following: {}.".format(
                valid_object_type))

        self.log("end_user_authorization: Searching the Rubrik cluster for the vSphere VM '{}'.".format(
            object_name))
        vm_id = self.object_id(object_name, object_type, timeout=timeout)

        self.log(
            "end_user_authorization: Searching the Rubrik cluster for the End User '{}'.".format(end_user))
        user = self.get(
            'internal', '/user?username={}'.format(end_user), timeout=timeout)

        if not user:
            sys.exit(
                'The Rubrik cluster does not contain a End User account named "{}".'.format(end_user))
        else:
            user_id = user[0]['id']

        self.log(
            "end_user_authorization: Searching the Rubrik cluster for the End User '{}' authorizations.".format(end_user))
        user_authorization = self.get(
            'internal', '/authorization/role/end_user?principals={}'.format(user_id), timeout=timeout)

        authorized_objects = user_authorization['data'][0]['privileges']['restore']

        if vm_id in authorized_objects:
            return 'No change required. The End User "{}" is already authorized to interact with the "{}" VM.'.format(
                end_user, object_name)
        else:
            config = {}
            config['principals'] = [user_id]
            config['privileges'] = {"restore": [vm_id]}

            return self.post(
                'internal',
                '/authorization/role/end_user',
                config,
                timeout=timeout)

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

        self.log(
            "add_vcenter: Searching the Rubrik cluster for the vCenter '{}'.".format(vcenter_ip))
        current_vcenter = self.get(
            "v1", "/vmware/vcenter?primary_cluster_id=local", timeout=timeout)

        for vcenter in current_vcenter["data"]:
            if vcenter["hostname"] == vcenter_ip:
                return "No change required. The vCenter '{}' has already been added to the Rubrik cluster.".format(
                    vcenter_ip)

        config = {}
        config["hostname"] = vcenter_ip
        config["username"] = vcenter_username
        config["password"] = vcenter_password
        if vm_linking:
            config["conflictResolutionAuthz"] = "AllowAutoConflictResolution"
        elif vm_linking is False:
            config["conflictResolutionAuthz"] = "NoConflictResolution"
        if ca_certificate is not None:
            config["caCerts"] = ca_certificate

        self.log(
            "add_vcenter: Adding vCenter '{}' to the Rubrik cluster.".format(vcenter_ip))
        add_vcenter = self.post("v1", "/vmware/vcenter", config, timeout)

        return add_vcenter, add_vcenter['links'][0]['href']

    def configure_timezone(self, timezone, timeout=15):
        """Configure the Rubrik cluster timezone.

        Arguments:
            timezone {str} -- The timezone you wish the Rubrik cluster to use. (choices: {America/Anchorage, America/Araguaina, America/Barbados, America/Chicago, America/Denver, America/Los_Angeles, America/Mexico_City, America/New_York, America/Noronha, America/Phoenix, America/Toronto, America/Vancouver, Asia/Bangkok, Asia/Dhaka, Asia/Dubai, Asia/Hong_Kong, Asia/Karachi, Asia/Kathmandu, Asia/Kolkata, Asia/Magadan, Asia/Singapore, Asia/Tokyo, Atlantic/Cape_Verde, Australia/Perth, Australia/Sydney, Europe/Amsterdam, Europe/Athens, Europe/London, Europe/Moscow, Pacific/Auckland, Pacific/Honolulu, Pacific/Midway, UTC})

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            str -- No change required. The Rubrik cluster is already configured with '`timezone`' as it's timezone.
            dict -- The full API response for `PATCH /v1//cluster/me'`
        """

        valid_timezones = [
            'America/Anchorage',
            'America/Araguaina',
            'America/Barbados',
            'America/Chicago',
            'America/Denver',
            'America/Los_Angeles',
            'America/Mexico_City',
            'America/New_York',
            'America/Noronha',
            'America/Phoenix',
            'America/Toronto',
            'America/Vancouver',
            'Asia/Bangkok',
            'Asia/Dhaka',
            'Asia/Dubai',
            'Asia/Hong_Kong',
            'Asia/Karachi',
            'Asia/Kathmandu',
            'Asia/Kolkata',
            'Asia/Magadan',
            'Asia/Singapore',
            'Asia/Tokyo',
            'Atlantic/Cape_Verde',
            'Australia/Perth',
            'Australia/Sydney',
            'Europe/Amsterdam',
            'Europe/Athens',
            'Europe/London',
            'Europe/Moscow',
            'Pacific/Auckland',
            'Pacific/Honolulu',
            'Pacific/Midway',
            'UTC']

        if timezone not in valid_timezones:
            sys.exit("Error: The timezone argument must be one of the following: {}.".format(
                valid_timezones))

        self.log("cluster_timezone: Determing the current cluster timezone")
        cluster_summary = self.get("v1", "/cluster/me", timeout=timeout)

        if cluster_summary["timezone"]["timezone"] == timezone:
            return "No change required. The Rubrik cluster is already configured with '{}' as it's timezone.".format(
                timezone)

        config = {}
        config["timezone"] = {}
        config["timezone"]["timezone"] = timezone

        self.log("cluster_timezone: Configuring the Rubrik cluster timezone")
        return self.patch("v1", "/cluster/me", config, timeout)

    def configure_ntp(self, ntp_server, timeout=15):
        """Configure connection information for the NTP servers used by the Rubrik cluster for time synchronization.

        Arguments:
            ntp_server {list} -- A list of the NTP server(s) you wish to configure the Rubrik cluster to use.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            str -- No change required. The NTP server(s) `ntp_server` has already been added to the Rubrik cluster.
            dict -- {'status_code': 204}
        """

        if isinstance(ntp_server, list) is False:
            sys.exit("Error: The 'ntp_server' argument must be a list object.")

        self.log("cluster_ntp: Determing the current cluster NTP settings")
        cluster_ntp = self.get("internal", "/cluster/me/ntp_server", timeout=timeout)

        if sorted(cluster_ntp["data"]) == sorted(ntp_server):
            return "No change required. The NTP server(s) {} has already been added to the Rubrik cluster.".format(
                ntp_server)

        self.log(
            "cluster_ntp: Adding the NTP server(s) '{}' to the Rubrik cluster.".format(ntp_server))
        return self.post("internal", "/cluster/me/ntp_server", ntp_server, timeout)

    def configure_syslog(self, syslog_ip, protocol, port=514, timeout=15):
        """Configure the Rubrik cluster syslog settings.

        Arguments:
            syslog_ip {str} -- The IP address or hostname of the syslog server you wish to add to the Rubrik cluster.
            protocol {str} -- The protocol to use when making the connection to the syslog server. (choices: {TCP, UDP})

        Keyword Arguments:
            port {int} -- The port to use when making the connection to the syslog server. (default: {514})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            str -- No change required. The Rubrik cluster is already configured to use the syslog server '`syslog_hostname`' on port '`port`' using the '`protocol`' protocol.
            dict -- The full API response for `POST /internal/syslog'`
        """

        valid_protocols = ["TCP", "UDP"]

        if protocol not in valid_protocols:
            sys.exit("Error: The protocol argument must be one of the following: {}.".format(
                valid_protocols))

        self.log("cluster_syslog: Getting the current cluster syslog settings")
        syslog = self.get("internal", "/syslog", timeout=timeout)

        config = {}
        config["hostname"] = syslog_ip
        config["protocol"] = protocol
        # convert to an int in case the user provides a string
        config["port"] = int(port)

        if syslog["total"] != 0:

            current_syslog_config = syslog["data"][0]
            # remove the id key from the syslog config for comparison
            del current_syslog_config["id"]

            if current_syslog_config == config:
                return "No change required. The Rubrik cluster is already configured to use the syslog server '{}' on port '{}' using the '{}' protocol.".format(
                    syslog_hostname, port, protocol)

            self.log("cluster_syslog: Clearing the existing syslog configuration.")
            self.delete("internal", "/syslog/1")

        self.log("cluster_syslog: Configuring the syslog settings.")
        return self.post("internal", "/syslog", config, timeout)

    def configure_vlan(self, vlan, netmask, ips, timeout=15):
        """Configure VLANs on the Rubrik cluster.

        Arguments:
            vlan {int} -- The VLAN ID you wish to configure.
            netmask {str} -- The netmask of the VLAN ID you wish to configure.
            ips {list or dict} -- The `ips` argument can either be a list or a dictionary. The list should contain an IP, in the relevant VLAN, for each node in the cluster. These IPs will be sorted, from lowest to highest, and then automatically associated with a node name based on alphabetical order. If you would like more finite control over the assignment you can use a dict with `node_name:ip` as it's key pairs.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            str -- No change required. The Rubrik cluster is already configured with the provided VLAN information.
            dict -- The full API response for `POST /internal/cluster/me/vlan'`
        """

        if isinstance(ips, list):
            self.log("cluster_vlan: Generating a list of all Cluster Node IPs.")
            node_names = self.cluster_node_name()

            if len(node_names) != len(ips):
                sys.exit("Error: The Rubrik cluster has {} nodes but you provided {} IP addresses. There must be a 1 to 1 relationship between nodes and IPs.".format(
                    str(len(node_names)), str(len(ips))))

            node_names = sorted(node_names)
            interfaces = sorted(ips)

            node_ip_combined = {}
            for i in range(0, len(node_names)):
                node_ip_combined[node_names[i]] = interfaces[i]
            print(node_ip_combined)
        elif isinstance(ips, dict):
            node_ip_combined = ips
        else:
            sys.exit(
                "Error: The interfaces argument must be either a list of IPs or a dictionary with node_name:ip as the key, value pairs.")

        self.log("cluster_vlan: Getting the current VLAN configurations.")
        current_vlans = self.get("internal", "/cluster/me/vlan", timeout=timeout)
        if current_vlans["total"] != 0:
            current_vlans = current_vlans["data"][0]

        interface_node_ip = [{'node': key, 'ip': val}
                             for key, val in node_ip_combined.items()]

        config = {}
        config["vlan"] = int(vlan)
        config["netmask"] = netmask
        config["interfaces"] = interface_node_ip

        if current_vlans == config:
            return "No change required. The Rubrik cluster is already configured with the provided VLAN information."

        self.log("cluster_vlan: Configuring the VLANs.")
        return self.post("internal", "/cluster/me/vlan", config, timeout)

    def configure_dns_servers(self, server_ip, timeout=15):
        """Configure the DNS Servers on the Rubrik cluster.

        Arguments:
            server_ip {list} -- The DNS Server IPs you wish to add to the Rubrik cluster.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            str -- No change required. The Rubrik cluster is already configured with the provided DNS servers.
            dict -- The full API response for `POST /internal/cluster/me/dns_nameserver'`
        """

        if isinstance(server_ip, list) is False:
            sys.exit("Error: The 'server_ip' argument must be a list")

        self.log(
            "cluster_dns_servers: Generating a list of DNS servers configured on the Rubrik cluster.")
        current_dns_servers = self.get(
            "internal", "/cluster/me/dns_nameserver", timeout=timeout)

        if sorted(current_dns_servers["data"]) == sorted(server_ip):
            return "No change required. The Rubrik cluster is already configured with the provided DNS servers."

        return self.post(
            "internal",
            "/cluster/me/dns_nameserver",
            server_ip,
            timeout)

    def configure_search_domain(self, search_domain, timeout=15):
        """Configure the DNS search domains on the Rubrik cluster.

        Arguments:
            search_domain {list} -- The DNS search domains you wish to add to the Rubrik cluster.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            str -- No change required. The Rubrik cluster is already configured with the provided DNS search domains.
            dict -- The full API response for `POST /internal/cluster/me/dns_search_domain'`
        """

        if isinstance(search_domain, list) is False:
            sys.exit("Error: The 'server_ip' argument must be a list")

        self.log(
            "cluster_dns_servers: Generating a list of DNS servers configured on the Rubrik cluster.")
        current_dns_search_domains = self.get(
            "internal", "/cluster/me/dns_search_domain", timeout=timeout)

        if sorted(current_dns_search_domains["data"]) == sorted(search_domain):
            return "No change required. The Rubrik cluster is already configured with the provided DNS servers."

        return self.post(
            "internal",
            "/cluster/me/dns_search_domain",
            search_domain,
            timeout)

    def configure_smtp_settings(self, hostname, port, from_email, smtp_username, smtp_password, encryption="NONE", timeout=15):
        """The Rubrik cluster uses email to send all notifications to local Rubrik cluster user accounts that have the Admin role. To do this the Rubrik cluster transfers the email messages to an SMTP server for delivery.
        This function will configure the Rubrik cluster with account information for the SMTP server to permit the Rubrik cluster to use the SMTP server for sending outgoing email.

        Arguments:
            hostname {str} -- Hostname of the SMTP server.
            port {int} -- Incoming port on the SMTP server. Normally port 25, port 465, or port 587, depending upon the type of encryption used.
            from_email {str} --  The email address assigned to the account on the SMTP server
            smtp_username {str} -- The username assigned to the account on the SMTP server
            smtp_password {str} -- The password associated with the username

        Keyword Arguments:
            encryption {str} --  The encryption protocol that the SMTP server requires for incoming SMTP connections (default: {"NONE"}) (choices: {NONE, SSL, STARTTLS})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            str -- No change required. The Rubrik cluster is already configured with the provided SMTP settings.
            dict -- The full API response for `POST /internal/smtp_instance'`
            dict -- The full API response for `PATCH /internal/smtp_instance/{id}'`
        """

        valid_encryption = ['SSL', 'STARTTLS', 'NONE']

        if encryption not in valid_encryption:
            sys.exit("Error: cluster_smtp_settings() encryption argument must be one of the following: {}.".format(
                valid_encryption))

        self.log(
            "cluster_smtp_settings: Determing the current SMTP settings on the Rubrik cluster.")
        current_smtp_settings = self.get("internal", "/smtp_instance", timeout=timeout)

        config = {}
        config["smtpHostname"] = hostname
        config["smtpPort"] = int(port)
        config["smtpSecurity"] = encryption
        config["smtpUsername"] = smtp_username
        config["fromEmailId"] = from_email

        if current_smtp_settings["total"] == 0:
            config["smtpPassword"] = smtp_password
            self.log("cluster_smtp_settings: Configuring the SMTP settings.")
            return self.post("internal", "/smtp_instance", config, timeout)
        else:
            current_smtp_settings = current_smtp_settings["data"][0]
            # Save the SMTP ID in case of PATCH and then delete for comparison
            smtp_id = current_smtp_settings["id"]
            del current_smtp_settings["id"]

            if current_smtp_settings == config:
                return "No change required. The Rubrik cluster is already configured with the provided SMTP settings."

            self.log("cluster_smtp_settings: Updating the SMTP settings.")
            return self.patch(
                "internal",
                "/smtp_instance/{}".format(smtp_id),
                config,
                timeout)

    def refresh_vcenter(self, vcenter_ip, wait_for_completion=True, timeout=15):
        """Refresh the metadata for the specified vCenter Server.

        Arguments:
            vcenter_ip {str} -- The IP address or FQDN of the vCenter you wish to refesh.


        Keyword Arguments:
            wait_for_completion {bool} -- Flag to determine if the function should wait for the refresh to complete before completing. (default: {True})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            dict -- When wait_for_completion is False, the full API response for `POST /v1/vmware/vcenter/{id}/refresh`
            dict -- When wait_for_completion is True, the full API response of the job status
        """

        self.log(
            "refresh_vcenter: Searching the Rubrik cluster for the provided vCenter Server.")
        vcenter_id = self.object_id(vcenter_ip, "vcenter", timeout=timeout)

        self.log("refresh_vcenter: Refresh vCenter.")

        api_request = self.post(
            "v1", "/vmware/vcenter/{}/refresh".format(vcenter_id), timeout)

        if wait_for_completion:
            return self.job_status(api_request["links"][0]["href"])

        return self.post("v1", "/vmware/vcenter/{}/refresh".format(vcenter_id), timeout)
