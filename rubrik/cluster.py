import json
import sys


class Cluster():
    """[summary]

    """

    def cluster_version(self):
        """Retrieves software version of the Rubrik cluster

        Returns:
            dict -- Software version running on the cluster
        """

        cluster_version_api_version = 'v1'
        cluster_version_api_endpoint = '/cluster/me/version'

        api_request = self.get(cluster_version_api_version, cluster_version_api_endpoint)

        ########### DO NOT MODIFY THESE VALUES - USED IN UNIT TESTS ONLY #########
        assert cluster_version_api_version == 'v1'
        assert cluster_version_api_endpoint == '/cluster/me/version'
        ##########################################################################

        return api_request

    def bootstrap(self, cluster_name, admin_email, admin_password, management_gateway, management_subnet_mask, enable_encryption=True, node_config=None, dns_search_domains=None, dns_nameservers=None, ntp_servers=None):
        """Issues a bootstrap request to a specified Rubrik cluster

        Arguments:
            cluster_name {str} -- Unique name to assign to the Rubrik cluster.
            admin_email {str} -- The Rubrik cluster sends messages for the admin account to this email address.
            admin_password {str} --  Password for the admin account.
            management_gateway {str} --  IP address assigned to the management network gateway
            management_subnet_mask {str} -- Subnet mask assigned to the management network.

        Keyword Arguments:
            enable_encryption {bool} -- Enable software data encryption at rest. (default: {True})
            node_config {dict} -- [description] (default: {None})
            dns_search_domains {str} -- The search domain that the DNS Service will use to resolve hostnames that are not fully qualified. (default: {None})
            dns_nameservers {list} -- IPv4 addresses of DNS servers. (default: {None})
            ntp_servers {list} -- FQDN or IPv4 address of a network time protocol (NTP) server. (default: {None})

        Returns:
            dict -- The response returned by the API call.
        """

        if node_config is None or isinstance(node_config, dict) is not True:
            sys.exit('Error: You must provide a valid dictionary for "node_config".')

        if dns_search_domains is None:
            dns_search_domains = []
        elif isinstance(dns_search_domains, dict) is not True:
            sys.exit('Error: You must provide a valid list for "dns_search_domains".')

        if dns_nameservers is None:
            dns_nameservers = ['8.8.8.8']
        elif isinstance(dns_nameservers, dict) is not True:
            sys.exit('Error: You must provide a valid list for "dns_nameservers".')

        if ntp_servers is None:
            ntp_servers = ['pool.ntp.org']
        elif isinstance(ntp_servers, dict) is not True:
            sys.exit('Error: You must provide a valid list for "ntp_servers".')

        bootstrap_api_version = 'internal'
        bootstrap_api_endpoint = '/cluster/me/bootstrap'

        bootstrap_config = {}
        bootstrap_config["enableSoftwareEncryptionAtRest"] = enable_encryption
        bootstrap_config["name"] = cluster_name
        bootstrap_config["dnsNameservers"] = dns_nameservers
        bootstrap_config["dnsSearchDomains"] = dns_search_domains
        bootstrap_config["ntpServers"] = ntp_servers

        bootstrap_config["adminUserInfo"] = {}
        bootstrap_config["adminUserInfo"]['password'] = admin_password
        bootstrap_config["adminUserInfo"]['emailAddress'] = admin_email
        bootstrap_config["adminUserInfo"]['id'] = "admin"

        bootstrap_config["nodeConfigs"] = {}
        for node_name, node_ip in node_config.items():
            bootstrap_config["nodeConfigs"][node_name] = {}
            bootstrap_config["nodeConfigs"][node_name]['managementIpConfig'] = {}
            bootstrap_config["nodeConfigs"][node_name]['managementIpConfig']['netmask'] = management_subnet_mask
            bootstrap_config["nodeConfigs"][node_name]['managementIpConfig']['gateway'] = management_gateway
            bootstrap_config["nodeConfigs"][node_name]['managementIpConfig']['address'] = node_ip

        api_request = self.post(bootstrap_api_version, bootstrap_api_endpoint,
                                bootstrap_config, timeout=10, authentication=False)

        return api_request

        ########### DO NOT MODIFY THESE VALUES - USED IN UNIT TESTS ONLY #########
        assert bootstrap_api_version == 'internal'
        assert bootstrap_api_endpoint == '/cluster/me/bootstrap'
        ##########################################################################

    def bootstrap_status(self, request_id="1"):
        """Retrieves status of in progress bootstrap requests

        Keyword Arguments:
            request_id {str} -- Id of the bootstrap request (default: {"1"})

        Returns:
            dict -- The response returned by the API call.
        """

        bootstrap_status_api_version = 'internal'
        bootstrap_status_api_endpoint = '/cluster/me/bootstrap?request_id={}'.format(request_id)

        api_request = self.get(bootstrap_status_api_version, bootstrap_status_api_endpoint, authentication=False)

        ########### DO NOT MODIFY THESE VALUES - USED IN UNIT TESTS ONLY #########
        assert bootstrap_status_api_version == 'internal'
        assert bootstrap_status_api_endpoint == '/cluster/me/bootstrap?request_id={}'.format(request_id)
        ##########################################################################

        return api_request
