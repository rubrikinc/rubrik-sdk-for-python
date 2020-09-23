""" Collection of methods that control connection with Polaris """

def _query(self, _operation_name=None, _query=None, _variables=None, timeout=15):
    import requests
    try:
        _operation_name = "RubrikPolarisSDKRequest"
        self._log('POST {}'.format(self._baseurl))
        if _operation_name is not None:
            self._log('Operation Name: {}'.format(_operation_name))
        self._log('Query: {}'.format(_query))
        if _variables is not None:
            self._log('Variables: {}'.format(_variables))
        _api_request = requests.post(
            self._baseurl,
            verify=False,
            headers=self._headers,
            json={
                "operationName": _operation_name,
                "variables": _variables,
                "query": "{}".format(_query)
            },
            timeout=timeout
        )
        self._log(str(_api_request) + "\n")
        try:
            _api_response = _api_request.json()
        except BaseException:
            _api_request.raise_for_status()
        if 'code' in _api_response and 'message' in _api_response and _api_response['code'] >= 400:
            print(_api_response['message'])
        return _api_response
    except Exception as e:
        print(e)


def _get_access_token(self):
    import requests
    _session_url = self._baseurl.replace('graphql','session')
    try:
        _payload = {
            "username": self._username,
            "password": self._password
        }
        _headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain'
        }
        _request = requests.post(_session_url, json=_payload, headers=_headers, verify=False)
        del _payload
        return _request.json()['access_token']
    except Exception as e:
        print(e)
