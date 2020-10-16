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
Collection of methods that control connection with Polaris.
"""


def _query(self, operation_name=None, query=None, variables=None, timeout=60):
    import requests
    from rubrik_polaris.exceptions import RequestException

    if not operation_name:
        operation_name = "RubrikPolarisSDKRequest"

    try:
        api_request = requests.post(
            "{}/graphql".format(self._baseurl),
            verify=False,
            headers=self._headers,
            json={
                "operationName": operation_name,
                "variables": variables,
                "query": "{}".format(query)
            },
            timeout=timeout
        )

        api_response = api_request.json()
        if 'code' in api_response and 'message' in api_response and api_response['code'] >= 400:
            raise RequestException(api_response['message'])
        else:
            api_request.raise_for_status()

        return api_response

    except requests.exceptions.RequestException as request_err:
        raise RequestException(request_err)
    except ValueError as value_err:
        raise RequestException(value_err)
    except Exception as err:
        raise


def _get_access_token(self):
    import requests
    from rubrik_polaris.exceptions import RequestException

    try:
        session_url = "{}/session".format(self._baseurl)
        payload = {
            "username": self._username,
            "password": self._password
        }
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain'
        }
        request = requests.post(session_url, json=payload, headers=headers, verify=False)
    
        del payload

        response_json = request.json()
        if 'access_token' not in response_json:
            raise RequestException("Authentication failed!")

        return response_json['access_token']

    except requests.exceptions.RequestException as request_err:
        raise RequestException(request_err)
    except ValueError as value_err:
        raise RequestException(value_err)
    except Exception as err:
        raise
