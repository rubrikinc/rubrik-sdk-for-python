# configure_replication_nat

Configure replication partner as specified by user using NAT Arguments: username {str} -- Username for the TARGET cluster {string} password {str} -- Password for the TARGET cluster {string} source_gateway {list} -- Specification of source NAT gateway specified as [str IP, [list of portnumber(s)]] target_gateway {list} -- Specification of source NAT gateway specified as [str IP, [list of portnumber(s)]] Keyword Arguments: ca_certificate {str} -- CA certificiate used to perform TLS certificate validation (default: {None}) timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {30}) Returns: dict -- The full API response from `POST /internal/replication/target`.
```py
def configure_replication_nat(username, password, source_gateway, target_gateway,
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| username  | str  | Username for the TARGET cluster {string} |         |
| password  | str  | Password for the TARGET cluster {string} |         |
| source_gateway  | list  | Specification of source NAT gateway specified as [str IP, [list of portnumber(s)]] |         |
| target_gateway  | list  | Specification of source NAT gateway specified as [str IP, [list of portnumber(s)]] |         |
