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
This module contains the Rubrik SDK Cluster class.
"""

import sys
from .api import Api
from .exceptions import InvalidParameterException, CDMVersionException, InvalidTypeException
import inspect


class Cluster(Api):
    """This class contains methods related to the management of the Rubrik cluster itself.
    """

    def configure_cluster_location(self, location, timeout=15):
        """Configure cluster geolocation. Overwrites previously set value if different.

        Arguments:
            location {str} -- Geolocation of the cluster.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            str -- If already configured with the same, the location is returned
            dict -- The full API response from `PATCH /cluster/me`.
        """

        self.function_name = inspect.currentframe().f_code.co_name

        if not isinstance(location, str):
            raise InvalidParameterException(
                'The configure_cluster_location() function requires the location to be specified as string.')

        self.log(
            "configure_cluster_location: Determing the current cluster location.")

        cluster_summary = self.get("v1", "/cluster/me", timeout=timeout)

        if cluster_summary["geolocation"]["address"] == location:
            return "No change required. The Rubrik cluster is already configured with '{}' as its location.".format(
                location)

        config = {}
        config["geolocation"] = {}
        config["geolocation"]["address"] = location

        self.log(
            "configure_cluster_location: Configuring the Rubrik cluster location.")

        return self.patch("v1", "/cluster/me", config, timeout)

    def configure_replication_private(self, username, password, target_ip, ca_certificate=None, timeout=30):
        """Configure replication partner as specified by user using PRIVATE NETWORK (direct connection).

        Arguments:
            username {str} -- Username for the TARGET cluster
            password {str} -- Password for the TARGET cluster
            target_ip {str} -- Address of one of the nodes of the TARGET cluster

        Keyword Arguments:
            ca_certificate {str} -- CA certificiate used to perform TLS certificate validation (default: {None})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {30})

        Returns:
            dict -- The full API response from `POST /internal/replication/target`.
        """

        self.function_name = inspect.currentframe().f_code.co_name

        config = {}

        config['replicationSetup'] = 'Private Network'
        config['targetClusterAddress'] = target_ip
        config['username'] = username
        config['password'] = password

        if ca_certificate is not None:
            config["caCerts"] = ca_certificate

        self.log(
            "configure_replication: Adding cluster '{}' as private network replication target.".format(target_ip))

        return self.post("internal", "/replication/target", config, timeout)

    def configure_replication_nat(self, username, password, source_gateway, target_gateway, ca_certificate=None, timeout=30):  # pylint: ignore
        """Configure replication partner as specified by user using NAT gateways.

        Arguments:
            username {str} -- Username for the TARGET cluster
            password {str} -- Password for the TARGET cluster
            source_gateway {list} -- Specification of source NAT gateway specified as [str IP, [list of portnumber(s)]]
            target_gateway {list} -- Specification of source NAT gateway specified as [str IP, [list of portnumber(s)]]

        Keyword Arguments:
            ca_certificate {str} -- CA certificiate used to perform TLS certificate validation (default: {None})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {30})

        Returns:
            dict -- The full API response from `POST /internal/replication/target`.
        """

        self.function_name = inspect.currentframe().f_code.co_name

        config = {}

        # Source/Target gateway need to be specified as [str IP, [list of portnumber(s)]]
        source_check = isinstance(
            source_gateway,
            list) and len(source_gateway) == 2 and isinstance(
            source_gateway[1],
            list) and len(
            source_gateway[1]) > 0
        target_check = isinstance(
            target_gateway,
            list) and len(target_gateway) == 2 and isinstance(
            target_gateway[1],
            list) and len(
            target_gateway[1]) > 0

        if not source_check or not target_check:
            raise InvalidParameterException(
                'The configure_replication() source and target gateways need to be defined as: ["IP STRING", [LIST OF PORT NUMBER(S)]].')

        config['targetGateway'] = {}
        config['sourceGateway'] = {}

        config['replicationSetup'] = 'NAT'
        config['sourceGateway']['address'] = source_gateway[0]
        config['sourceGateway']['ports'] = source_gateway[1]
        config['targetGateway']['address'] = target_gateway[0]
        config['targetGateway']['ports'] = target_gateway[1]
        config['username'] = username
        config['password'] = password

        if ca_certificate is not None:
            config["caCerts"] = ca_certificate

        self.log("configure_replication: Adding cluster behind '{}' as NAT replication target.".format(
            target_gateway))

        return self.post("internal", "/replication/target", config, timeout)

    def cluster_version(self, timeout=15):
        """Retrieves the software version of the Rubrik cluster.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            str -- The version of CDM installed on the Rubrik cluster.
        """

        if self.function_name == "":
            self.function_name = inspect.currentframe().f_code.co_name

        self.log(
            'cluster_version: Getting the software version of the Rubrik cluster.')
        return self.get('v1', '/cluster/me/version', timeout=timeout)['version']

    def minimum_installed_cdm_version(self, cluster_version, timeout=15):
        """Determine if the Rubrik cluster is running the provided CDM `cluster_version` or later. If the cluster is running an earlier release
        of CDM, `False` is returned. If the cluster is running the provided `cluster_version`, or a later release, `True` is returned.

        Arguments:
            cluster_version {float} -- The minimum required version of Rubrik CDM you wish ensure is running.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})
        """
        if self.function_name == "":
            self.function_name = inspect.currentframe().f_code.co_name

        if float(self.cluster_version(timeout)[:3]) < float(cluster_version):
            return False

        return True

    def cluster_node_ip(self, timeout=15):
        """Retrieve the IP Address for each node in the Rubrik cluster.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            list -- A list that contains the IP Address for each node in the Rubrik cluster.
        """

        self.function_name = inspect.currentframe().f_code.co_name

        self.log('cluster_node_ip: Generating a list of all Cluster Node IPs.')
        api_request = self.get('internal', '/cluster/me/node', timeout=timeout)

        node_ip_list = []

        for node in api_request['data']:
            node_ip_list.append(node["ipAddress"])

        return node_ip_list

    def cluster_node_name(self, timeout=15):
        """Retrieve the name of each node in the Rubrik cluster.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            list -- A list that contains the name of each node in the Rubrik cluster.
        """

        self.function_name = inspect.currentframe().f_code.co_name

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

        self.function_name = inspect.currentframe().f_code.co_name

        valid_object_type = ['vmware']

        if object_type not in valid_object_type:
            raise InvalidParameterException("The end_user_authorization() object_type argument must be one of the following: {}.".format(
                valid_object_type))

        self.log("end_user_authorization: Searching the Rubrik cluster for the vSphere VM '{}'.".format(
            object_name))
        vm_id = self.object_id(object_name, object_type, timeout=timeout)

        self.log(
            "end_user_authorization: Searching the Rubrik cluster for the End User '{}'.".format(end_user))
        user = self.get(
            'internal', '/user?username={}'.format(end_user), timeout=timeout)

        if not user:
            raise InvalidParameterException(
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

    def add_vcenter(self, vcenter_ip, vcenter_username, vcenter_password, vm_linking=True, ca_certificate=None, timeout=30):  # pylint: ignore
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

        self.function_name = inspect.currentframe().f_code.co_name

        self.log("add_vcenter: Searching the Rubrik cluster for the vCenter '{}'.".format(
            vcenter_ip))
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

        self.function_name = inspect.currentframe().f_code.co_name

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
            raise InvalidParameterException("The timezone argument must be one of the following: {}.".format(
                valid_timezones))

        self.log("cluster_timezone: Determing the current cluster timezone")
        cluster_summary = self.get("v1", "/cluster/me", timeout=timeout)

        if cluster_summary["timezone"]["timezone"] == timezone:
            return "No change required. The Rubrik cluster is already configured with '{}' as its timezone.".format(
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

        self.function_name = inspect.currentframe().f_code.co_name

        if isinstance(ntp_server, list) is False:
            raise InvalidTypeException(
                "The 'ntp_server' argument must be a list object.")

        self.log("cluster_ntp: Determing the current cluster NTP settings")
        cluster_ntp = self.get(
            "internal", "/cluster/me/ntp_server", timeout=timeout)

        cdm_v5_check = self.minimum_installed_cdm_version("5.0")

        if cdm_v5_check is True:
            current_ntp_servers = []
            for ntp in cluster_ntp["data"]:
                current_ntp_servers.append(ntp["server"])
        else:
            current_ntp_servers = cluster_ntp["data"]

        if sorted(current_ntp_servers) == sorted(ntp_server):
            return "No change required. The NTP server(s) {} has already been added to the Rubrik cluster.".format(
                ntp_server)

        self.log("cluster_ntp: Adding the NTP server(s) '{}' to the Rubrik cluster.".format(
            ntp_server))

        if cdm_v5_check is True:
            config = []
            for ntp in ntp_server:
                config.append({
                    "server": ntp
                })
        else:
            config = ntp_server

        return self.post("internal", "/cluster/me/ntp_server", config, timeout)

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

        self.function_name = inspect.currentframe().f_code.co_name

        valid_protocols = ["TCP", "UDP"]

        if protocol not in valid_protocols:
            raise InvalidParameterException("The protocol argument must be one of the following: {}.".format(
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
                    syslog_ip, port, protocol)

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

        self.function_name = inspect.currentframe().f_code.co_name

        if isinstance(ips, list):
            self.log("cluster_vlan: Generating a list of all Cluster Node IPs.")
            node_names = self.cluster_node_name()

            if len(node_names) != len(ips):
                raise InvalidParameterException("The Rubrik cluster has {} nodes but you provided {} IP addresses. There must be a 1 to 1 relationship between nodes and IPs.".format(
                    str(len(node_names)), str(len(ips))))

            node_names = sorted(node_names)
            interfaces = sorted(ips)

            node_ip_combined = {}
            for i in range(0, len(node_names)):
                node_ip_combined[node_names[i]] = interfaces[i]
        elif isinstance(ips, dict):
            node_ip_combined = ips
        else:
            raise InvalidParameterException(
                "The interfaces argument must be either a list of IPs or a dictionary with node_name:ip as the key, value pairs.")

        self.log("cluster_vlan: Getting the current VLAN configurations.")
        current_vlans = self.get(
            "internal", "/cluster/me/vlan", timeout=timeout)
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

        self.function_name = inspect.currentframe().f_code.co_name

        if isinstance(server_ip, list) is False:
            raise InvalidTypeException(
                "The 'server_ip' argument must be a list")

        self.log(
            "cluster_dns_servers: Generating a list of DNS servers configured on the Rubrik cluster.")
        current_dns_servers = self.get(
            "internal", "/cluster/me/dns_nameserver", timeout=timeout)

        if sorted(current_dns_servers) == sorted(server_ip):
            return "No change required. The Rubrik cluster is already configured with the provided DNS servers."

        return self.post("internal", "/cluster/me/dns_nameserver", server_ip, timeout)

    def configure_login_banner(self, banner, timeout=15):
        """Configure the Login Banner Text on the Rubrik cluster.

        Arguments:
            banner {str} -- The Login Banner Text you wish to see when the Rubrik cluster login page loads.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            str -- No change required. The Rubrik cluster is already configured with the login banner text '`banner`'.
            dict -- The full API response for `PUT /internal/cluster/me/login_banner'`
        """

        self.function_name = inspect.currentframe().f_code.co_name

        self.log(
            "configure_login_banner: Retrieving the current login banner of the Rubrik cluster.")
        current_login_banner = self.get(
            "internal", "/cluster/me/login_banner", timeout=timeout)

        config = {}
        config["loginBanner"] = banner

        if config == current_login_banner:
            return "No change required. The Rubrik cluster is already configured with the login banner text '`banner`'."

        self.log(
            "configure_login_banner: Setting the login banner of the Rubrik cluster.")
        return self.put("internal", "/cluster/me/login_banner", config, timeout)

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

        self.function_name = inspect.currentframe().f_code.co_name

        if isinstance(search_domain, list) is False:
            raise InvalidTypeException(
                "The 'server_ip' argument must be a list")

        self.log(
            "cluster_dns_servers: Generating a list of DNS servers configured on the Rubrik cluster.")
        current_dns_search_domains = self.get(
            "internal", "/cluster/me/dns_search_domain", timeout=timeout)

        if sorted(current_dns_search_domains) == sorted(search_domain):
            return "No change required. The Rubrik cluster is already configured with the provided DNS Search Domains."

        return self.post("internal", "/cluster/me/dns_search_domain", search_domain, timeout)

    def configure_smtp_settings(self, hostname, port, from_email, smtp_username, smtp_password, encryption="NONE", timeout=15):  # pylint: ignore
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
            dict -- The full API response for `POST /internal/smtp_instance`
            dict -- The full API response for `PATCH /internal/smtp_instance/{id}`
        """
        self.function_name = inspect.currentframe().f_code.co_name

        valid_encryption = ['SSL', 'STARTTLS', 'NONE']

        if encryption not in valid_encryption:
            raise InvalidParameterException("cluster_smtp_settings() encryption argument must be one of the following: {}.".format(
                valid_encryption))

        self.log(
            "cluster_smtp_settings: Determing the current SMTP settings on the Rubrik cluster.")
        current_smtp_settings = self.get(
            "internal", "/smtp_instance", timeout=timeout)

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
            return self.patch("internal", "/smtp_instance/{}".format(smtp_id), config, timeout)

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

        self.function_name = inspect.currentframe().f_code.co_name

        self.log(
            "refresh_vcenter: Searching the Rubrik cluster for the provided vCenter Server.")
        vcenter_id = self.object_id(vcenter_ip, "vcenter", timeout=timeout)

        self.log("refresh_vcenter: Refresh vCenter.")
        api_request = self.post(
            "v1", "/vmware/vcenter/{}/refresh".format(vcenter_id), timeout)

        if wait_for_completion:
            return self.job_status(api_request["links"][0]["href"])

        return api_request

    def refresh_ahv(self, nutanix_ahv_cluster, wait_for_completion=True, timeout=15):
        """Refresh the metadata for the specified Nutanix AHV cluster.

        Arguments:
            nutanix_ahv_cluster {str} -- The name of the AHV cluster you wish to refresh.


        Keyword Arguments:
            wait_for_completion {bool} -- Flag to determine if the function should wait for the refresh to complete before completing. (default: {True})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            dict -- When wait_for_completion is False, the full API response for `POST /internal/nutanix/cluster/{id}/refresh`
            dict -- When wait_for_completion is True, the full API response of the job status
        """

        self.function_name = inspect.currentframe().f_code.co_name

        self.log(
            "refresh_ahv: Searching the Rubrik cluster for the provided AHV cluster.")
        ahv_id = self.object_id(nutanix_ahv_cluster, "ahv_cluster", timeout=timeout)

        self.log("refresh_ahv: Refresh AHV cluster.")
        api_request = self.post(
            "internal", "/nutanix/cluster/{}/refresh".format(ahv_id), timeout)

        if wait_for_completion:
            return self.job_status(api_request["links"][0]["href"])

        return api_request

    def update_proxy(self, host, protocol, port, username=None, password=None, timeout=15):
        """Update the proxy configuration on the Rubrik cluster.

        Arguments:
            host {str} -- The IP address or FQDN of the proxy you wish to add.
            protocol {str} -- The protocol of the proxy you wish to add.
            port {int} -- The port of the proxy you wish to add.

        Keyword Arguments:
            username {str} -- The username used for authentication. (default: {None})
            password {str} -- The password used for authentication. (default: {None})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            dict -- The full API response for `PATCH /internal/node_management/proxy_config`
        """

        self.function_name = inspect.currentframe().f_code.co_name

        valid_protocols = [
            'HTTP',
            'HTTPS',
            'SOCKS5']

        if protocol not in valid_protocols:
            sys.exit("Error: The protocol argument must be one of the following: {}.".format(
                valid_protocols))

        config = {}
        config["host"] = host
        config["protocol"] = protocol
        config["port"] = port
        config["username"] = username
        config["password"] = password

        self.log("update_proxy: Getting the current proxy configuration")
        current_proxy_settings = self.get(
            "internal", "/node_management/proxy_config", timeout=timeout)

        if current_proxy_settings["host"] == host and current_proxy_settings["port"] == port and current_proxy_settings["username"] == username:
            return "No change required. The proxy '{}' has already been added to the Rubrik cluster.".format(host)

        self.log("update_proxy: Updating proxy configuration.")
        return self.patch("internal", "/node_management/proxy_config", config, timeout)

    def delete_proxy(self, timeout=15):
        """Delete the proxy configuration from the Rubrik cluster.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            str -- No change required. The proxy configuration is already cleared out.
            dict -- The full API response for `DELETE /internal/node_management/proxy_config`
        """

        self.function_name = inspect.currentframe().f_code.co_name

        current_proxy_settings = self.get(
            "internal", "/node_management/proxy_config", timeout=timeout)
        self.log("delete_proxy: Current proxy configuration {}".format(
            current_proxy_settings))

        if current_proxy_settings["host"] == "":
            return "No change required. The proxy configuration is already cleared out."

        self.log("delete_proxy: Deleting proxy configuration.")
        return self.delete("internal", "/node_management/proxy_config", timeout)

    def create_user(self, username, password, first_name=None, last_name=None, email_address=None, contact_number=None, timeout=15):  # pylint: ignore
        """Create a new user on the Rubrik cluster

        Arguments:
            username {str} -- The username for the user you wish to create.
            password {str} -- The password for the user you wish to create.

        Keyword Arguments:
            first_name {str} -- The first name of the user you wish to create. (default: {None})
            last_name {str} -- The last name of the user you wish to create. (default: {None})
            email_address {str} -- The email address of the user you wish to create. (default: {None})
            contact_number {str} -- The contact number of the user you wish to create. (default: {None})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            str -- No change required. The user '`username`' already exists on the Rubrik cluster
            dict -- The full API response from `POST /internal/user`.
        """

        self.function_name = inspect.currentframe().f_code.co_name

        self.log("create_user: Searching for the current users on the Rubrik cluster")
        current_users = self.get(
            "internal", "/user?username={}".format(username), timeout=timeout)
        if len(current_users) > 0:
            return "No change required. The user '{}' already exists on the Rubrik cluster.".format(username)

        config = {}
        config["username"] = username
        config["password"] = password
        if first_name is not None:
            config["firstName"] = first_name
        if last_name is not None:
            config["lastName"] = last_name
        if email_address is not None:
            config["emailAddress"] = email_address
        if contact_number is not None:
            config["contactNumber"] = contact_number

        self.log("create_user: Creating the new user account.")
        return self.post("internal", "/user", config, timeout)

    def read_only_authorization(self, username, timeout=15):
        """Grant read-only access to a specific user.

         Arguments:
             username {str} -- The username you wish to grant read-only access to.

         Keyword Arguments:
             timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

         Returns:
             str -- No change required. The user '`username`' already has read-only permissions.
             dict -- The full API response from `POST /internal/authorization/role/read_only_admin`.
         """

        self.function_name = inspect.currentframe().f_code.co_name

        if self.minimum_installed_cdm_version(5.0) is False:
            raise CDMVersionException(5.0)

        self.log(
            "read_only_authorization: Searching for the current users on the Rubrik cluster")
        current_users = self.get(
            "internal", "/user?username={}".format(username), timeout=timeout)
        if len(current_users) < 1:
            raise InvalidParameterException(
                "The user '{}' does not exsit on the Rubrik cluster.".format(username))

        self.log(
            "read_only_authorization: Checking the current authorizations for user '{}'".format(username))
        current_authorizations = self.get(
            "internal", "/authorization/role/read_only_admin?principals={}".format(current_users[0]["id"]), timeout=timeout)

        try:
            if current_authorizations["data"][0]["privileges"]["basic"][0] == "Global:::All":
                return "No change required. The user '{}' already has read-only permissions.".format(username)
        except BaseException:
            pass

        config = {}
        config["principals"] = [current_users[0]["id"]]
        config["privileges"] = {}
        config["privileges"]["basic"] = ["Global:::All"]

        self.log(
            "read_only_authorization: Granting read-only privilages to user '{}'.".format(username))
        return self.post("internal", "/authorization/role/read_only_admin", config, timeout)

    def add_guest_credential(self, username, password, domain=None, timeout=15):
        """Add a new guest credential to the Rubrik cluster.

        Arguments:
            username {str} -- The account username used for authentication.
            password {str} -- The account password used for authentication.

        Keyword Arguments:
            domain {int} -- The domain name of account password used for authentication. (default: {None})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            str -- No change required. The account 'username' has already been added to the Rubrik cluster.
            str -- No change required. The account 'username@domain' has already been added to the Rubrik cluster.
            dict -- The full API response for `POST /v1/vmware/guest_credential`.
        """

        self.function_name = inspect.currentframe().f_code.co_name

        config = {}
        config["username"] = username
        config["password"] = password
        config["domain"] = domain

        self.log("add_guest_credential: Getting the current guest credentials.")
        current_guest_credentials = self.get(
            "internal", "/vmware/guest_credential", timeout=timeout)

        for guest_credential in current_guest_credentials["data"]:
            if guest_credential.get("domain"):
                if guest_credential["username"] == username and guest_credential["domain"] == domain:
                    return "No change required. The account '{}@{}' has already been added to the Rubrik cluster.".format(
                        username, domain)
            elif domain is None:
                if guest_credential["username"] == username:
                    return "No change required. The account '{}' has already been added to the Rubrik cluster.".format(
                        username)

        self.log(
            "guest_credentials: Adding new guest OS credential '{}@{}' to the Rubrik cluster.".format(username, domain))
        return self.post("internal", "/vmware/guest_credential", config, timeout)

    def delete_guest_credential(self, username, domain=None, timeout=15):
        """Delete a guest credential from the Rubrik cluster.

        Arguments:
            username {str} -- The account username to be deleted.

        Keyword Arguments:
            domain {int} -- The domain name of the account to be deleted. (default: {None})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            str -- No change required. The guest credential 'username' does not exist.
            str -- No change required. The guest credential 'username@domain' does not exist.
            dict -- The full API response for `POST /v1/vmware/guest_credential`
        """

        self.function_name = inspect.currentframe().f_code.co_name

        current_guest_credentials = self.get(
            "internal", "/vmware/guest_credential", timeout=timeout)
        self.log("delete_guest_credential: Current guest credentials {}".format(
            current_guest_credentials))

        delete_guest_credential = ""

        for guest_credential in current_guest_credentials["data"]:
            if domain is None:
                if guest_credential["username"] == username:
                    delete_guest_credential = guest_credential["id"]
                    self.log(
                        "guest_credentials: Deleting guest OS credentials '{}' to the Rubrik cluster.".format(username))
                    return self.delete(
                        "internal", "/vmware/guest_credential/{}".format(delete_guest_credential), timeout)
            elif guest_credential.get("domain"):
                if guest_credential["username"] == username and guest_credential["domain"] == domain:
                    delete_guest_credential = guest_credential["id"]
                    self.log(
                        "guest_credentials: Deleting guest OS credentials '{}@{}' to the Rubrik cluster.".format(
                            username, domain))
                    return self.delete(
                        "internal", "/vmware/guest_credential/{}".format(delete_guest_credential), timeout)

        if domain is None:
            return "No change required. The guest credential '{}' does not exist.".format(username)
        else:
            return "No change required. The guest credential '{}@{}' does not exist.".format(username, domain)

    def cluster_node_id(self, timeout=15):
        """Returns a list of node ids from all the nodes in the cluster.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
             list -- A list that contains the ID for each node in the Rubrik cluster.
        """

        self.function_name = inspect.currentframe().f_code.co_name

        self.log(
            "cluster_node_id - Getting all the node ids from the from the cluster.")
        node_id_list = []

        api_request = self.get('internal', '/node', timeout)

        for node in api_request['data']:
            node_id_list.append(node["id"])

        return node_id_list

    def cluster_support_tunnel(self, enabled=True, timeout=15):
        """Enable or Disable the support tunnel.

        Keyword Arguments:
            enabled (bool) -- The flag that enables or disables the support tunnel. (default: {True})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            str -- No change required. Support Tunnel is already enabled.
            str -- No change required. Support Tunnel is already disabled.
            dict -- The full API response from `POST /internal/node/me/support_tunnel`.
        """

        self.function_name = inspect.currentframe().f_code.co_name

        if not isinstance(enabled, bool):
            raise InvalidParameterException(
                "The enabled parameter must be True or False.")

        self.log(
            "cluster_support_tunnel - Determining status of Cluster Support Tunnel.")
        check_tunnel = self.get('internal', '/node/me/support_tunnel', timeout)

        if enabled is True:

            if check_tunnel['isTunnelEnabled'] is False:

                config = {}
                config['isTunnelEnabled'] = True
                config['inactivityTimeoutInSeconds'] = 0

                self.log(
                    "cluster_support_tunnel - Enabling Cluster Support Tunnel.")
                return self.patch('internal', '/node/me/support_tunnel', config, timeout)

            else:
                return("No change required. Support Tunnel is already enabled.")

        elif enabled is False:

            if check_tunnel['isTunnelEnabled'] is False:

                return ("No change required. Support Tunnel is already disabled.")

            else:
                config = {}
                config['isTunnelEnabled'] = False

                self.log("cluster_support_tunnel - Disable the Support Tunnel")

                return self.patch('internal', '/node/me/support_tunnel', config, timeout)

    def add_floating_ips(self, floating_ips, wait_for_completion=True, timeout=15):
        """Add floating IPs to CDM.

        Arguments:
            floating_ips {list} -- The IP addresses you wish to add.

        Returns:
            dict -- When wait_for_completion is False, the full API response for `POST /internal/node_management/cluster_ip`
            dict -- When wait_for_completion is True, the full API response of the job status
        """

        self.function_name = inspect.currentframe().f_code.co_name

        self.log("Appending list of floating IPs with {}".format(floating_ips))
        if isinstance(floating_ips, list) is False:
            raise InvalidParameterException(
                "The 'floating_ips' argument must be a list")

        config = self.get('internal', '/node_management/cluster_ip')
        if set(config).intersection(floating_ips):
            return("No change required. IP(s) {} is already in list".format(set(config).intersection(floating_ips)))
        else:
            for i in floating_ips:
                config.append(i)

        # return config
        return self.post('internal', '/node_management/cluster_ip', config)

    def remove_floating_ips(self, floating_ips, wait_for_completion=True, timeout=15):
        """Remove floating IPs from CDM.

        Arguments:
            floating_ips {list} -- The IP addresses you wish to remove.

        Returns:
            dict -- When wait_for_completion is False, the full API response for `POST /internal/node_management/cluster_ip`
            dict -- When wait_for_completion is True, the full API response of the job status
        """

        self.function_name = inspect.currentframe().f_code.co_name

        self.log("Removing list of floating IPs with {}".format(floating_ips))
        if isinstance(floating_ips, list) is False:
            raise InvalidParameterException(
                "The 'floating_ips' argument must be a list")

        config = self.get('internal', '/node_management/cluster_ip')
        if set(config).intersection(floating_ips):
            for i in floating_ips:
                if i in config:
                    config.remove(i)
        else:
            return("No change required. IP(s) {} is not in list".format(set(config).intersection(floating_ips)))

        return self.post('internal', '/node_management/cluster_ip', config)

    def get_floating_ips(self, wait_for_completion=True, timeout=15):
        """Returns list of floating IPs

        Returns:
            dict -- When wait_for_completion is False, the full API response for `GET /internal/node_management/cluster_ip`
            dict -- When wait_for_completion is True, the full API response of the job status
        """
        self.function_name = inspect.currentframe().f_code.co_name

        self.log("Returning list of floating IPs.")

        config = self.get('internal', '/node_management/cluster_ip')

        return config

    def get_all_vcenters(self, timeout=15):
        """Retrieve information for each vCenter connected to the Rubrik cluster.
        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {30})
        Returns:
            dict -- The full API response for `GET /v1/vmware/vcenter`.
        """

        self.function_name = inspect.currentframe().f_code.co_name

        self.log(
            'get_all_vcenters: Getting information for each vCenter connected  to the Rubrik cluster.')
        return self.get('v1', '/vmware/vcenter', timeout=timeout)
