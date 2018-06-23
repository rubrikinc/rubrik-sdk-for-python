import base64
import requests
import json
import sys
try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+


class api:

    def __init__(self, node_ip, username, password):
        self.node_ip = node_ip
        self.username = username
        self.password = password

    def _authorization_header(self):
        """Takes a username and password and returns a value suitable for
        using as value of an Authorization header to do basic auth.
        """

        credentials = '{}:{}'.format(self.username, self.password)

        # Encode the Username:Password as base64
        authorization = base64.b64encode(credentials.encode())
        # Convert to String for API Call
        authorization = authorization.decode()

        authorization_header = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Basic ' + authorization
        }

        return authorization_header

    def _api_validation(self, api_version, api_endpoint):
        valid_api_versions = ['v1', 'internal']

        if api_version not in valid_api_versions:
            sys.exit("Error: Enter a valid API version {}.".format(valid_api_versions))

        if type(api_endpoint) is not str:
            sys.exit("Error: The API Endpoint must be a string.")
        elif api_endpoint[0] != "/":
            sys.exit("Error: The API Endpoint should begin with '/'. (ex: /cluster/me)")
        elif api_endpoint[-1] == "/":
            sys.exit("Error: The API Endpoint should not end with '/'. (ex. /cluster/me)")

    def get(self, api_version, api_endpoint):
        """ Connect to a Rubrik Cluster and perform a GET operation """

        self._api_validation(api_version, api_endpoint)

        request_url = "https://{}/api/{}{}".format(self.node_ip, api_version, api_endpoint)
        request_url = quote(request_url, '://?=&')

        header = self._authorization_header()

        try:
            api_request = requests.get(request_url, verify=False, headers=header)
            # Raise an error if they request was not successful
            api_request.raise_for_status()
        except requests.exceptions.RequestException as error_message:
            print(error_message)
            sys.exit(1)

        response_body = api_request.json()

        return response_body

    def job_status(self, url):
        '''Get the status of a Rubrik job '''

        header = self._authorization_header()

        try:
            api_request = requests.get(url, verify=False, headers=header)
            # Raise an error if they request was not successful
            api_request.raise_for_status()
        except requests.exceptions.RequestException as error_message:
            print(error_message)
            sys.exit(1)

        response_body = api_request.json()

        return response_body

    def post(self, api_version, api_endpoint, config):
        """ Connect to a Rubrik Cluster and perform a POST operation """

        self._api_validation(api_version, api_endpoint)

        config = json.dumps(config)

        request_url = "https://{}/api/{}{}".format(self.node_ip, api_version, api_endpoint)

        header = self._authorization_header()

        try:
            api_request = requests.post(request_url, data=config, verify=False, headers=header)
            # Raise an error if they request was not successful
            api_request.raise_for_status()
        except requests.exceptions.RequestException as error_message:
            print(error_message)
            sys.exit(1)

        response_body = api_request.json()

        return response_body

    def patch(self, api_version, api_endpoint, config):
        """ Connect to a Rubrik Cluster and perform a POST operation """

        self._api_validation(api_version, api_endpoint)

        config = json.dumps(config)

        request_url = "https://{}/api/{}{}".format(self.node_ip, api_version, api_endpoint)

        header = self._authorization_header()

        try:
            api_request = requests.patch(request_url, data=config, verify=False, headers=header)
            # Raise an error if they request was not successful
            api_request.raise_for_status()
        except requests.exceptions.RequestException as error_message:
            print(error_message)
            sys.exit(1)

        response_body = api_request.json()

        return response_body

    def delete(self, api_version, api_endpoint):
        """ Connect to a Rubrik Cluster and perform a DELETE operation """

        self._api_validation(api_version, api_endpoint)

        config = json.dumps(config)

        request_url = "https://{}/api/{}{}".format(self.node_ip, api_version, api_endpoint)

        header = self._authorization_header()

        try:
            api_request = requests.delete(request_url, data=config, verify=False, headers=header)
            # Raise an error if they request was not successful
            api_request.raise_for_status()
        except requests.exceptions.RequestException as error_message:
            print(error_message)
            sys.exit(1)

        response_body = api_request.json()

        return response_body
