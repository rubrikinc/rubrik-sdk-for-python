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


""" Collection of methods that control connection with Polaris """

def _query(self, _operation_name=None, _query=None, _variables=None, _timeout=60):
    import requests

    try:
        _operation_name = "RubrikPolarisSDKRequest"

        _api_request = requests.post(
            self._baseurl,
            verify=False,
            headers=self._headers,
            json={
                "operationName": _operation_name,
                "variables": _variables,
                "query": "{}".format(_query)
            },
            timeout=_timeout
        )

        try:
            _api_response = _api_request.json()
            if 'code' in _api_response and 'message' in _api_response and _api_response['code'] >= 400:
                print(_api_response['message'])

            return _api_response
        except BaseException:
            _api_request.raise_for_status()

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
