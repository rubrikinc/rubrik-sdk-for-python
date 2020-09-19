""" Collection of methods that control connection with Polaris """

def _query(self, operation_name=None, query=None, variables=None, timeout=15):
    import requests
    try:
        self._log('POST {}'.format(self.baseurl))
        if operation_name is not None:
            self._log('Operation Name: {}'.format(operation_name))
        self._log('Query: {}'.format(query))
        if variables is not None:
            self._log('Variables: {}'.format(variables))
        api_request = requests.post(
            self.baseurl,
            verify=False,
            headers=self.headers,
            json={
                "operationName": operation_name,
                "variables": variables,
                "query": "{}".format(query)
            },
            timeout=timeout
        )
        self._log(str(api_request) + "\n")
        try:
            api_response = api_request.json()
        except BaseException:
            api_request.raise_for_status()
        if 'code' in api_response and 'message' in api_response and api_response['code'] >= 400:
            print(api_response['message'])
        return api_response
    except Exception as e:
        print(e)


def _get_access_token(self):
    import requests
    try:
        if 'root_domain' in self.kwargs and self.kwargs['root_domain'] is not None:
            graphql_service_endpoint = "https://{}.{}/api/session".format(self.domain, self.kwargs['root_domain'])
        else:
            graphql_service_endpoint = "https://{}.my.rubrik.com/api/session".format(self.domain)
        payload = {
            "username": self.username,
            "password": self.password
        }
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain'
        }
        request = requests.post(graphql_service_endpoint, json=payload, headers=headers, verify=False)
        del payload
        return request.json()['access_token']
    except Exception as e:
        print(e)
