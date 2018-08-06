# bootstrap()

Issues a bootstrap request to a specified Rubrik cluster

```py
def bootstrap(cluster_name, admin_email, admin_password, management_gateway, management_subnet_mask, enable_encryption=True, node_config=None, dns_search_domains=None, dns_nameservers=None, ntp_servers=None, timeout=15)
```

## Arguments
cluster_name {str} -- Unique name to assign to the Rubrik cluster.

admin_email {str} -- The Rubrik cluster sends messages for the admin account to this email address.

admin_password {str} --  Password for the admin account.

management_gateway {str} --  IP address assigned to the management network gateway

management_subnet_mask {str} -- Subnet mask assigned to the management network.


## Keyword Arguments
enable_encryption {bool} -- Enable software data encryption at rest. (default: {True})

node_config {dict} -- [description] (default: {None})

dns_search_domains {str} -- The search domain that the DNS Service will use to resolve hostnames that are not fully qualified. (default: {None})

dns_nameservers {list} -- IPv4 addresses of DNS servers. (default: {None})

ntp_servers {list} -- FQDN or IPv4 address of a network time protocol (NTP) server. (default: {None})

timeout {int} -- The response timeout value, in seconds, of the API call. (default: {15})


## Returns
dict -- The response returned by the API call.



