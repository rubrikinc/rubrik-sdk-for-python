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
        """Create the authorization header used in the API calls.


        Returns:
            dict -- The authorization header that utilizes Basic authentication.
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
        """Validate the API Version and API Endpoint provided by the end user

        Arguments:
            api_version {str} -- The version of the Rubrik CDM API to call.
            api_endpoint {str} -- The endpoint (ex. cluster/me) of the Rubrik CDM API to call.
        """

        valid_api_versions = ['v1', 'internal']

        # Validate the API Version
        if api_version not in valid_api_versions:
            sys.exit("Error: Enter a valid API version {}.".format(valid_api_versions))

        # Validate the API Endpoint Syntax
        if type(api_endpoint) is not str:
            sys.exit("Error: The API Endpoint must be a string.")
        elif api_endpoint[0] != "/":
            sys.exit("Error: The API Endpoint should begin with '/'. (ex: /cluster/me)")
        elif api_endpoint[-1] == "/":
            sys.exit("Error: The API Endpoint should not end with '/'. (ex. /cluster/me)")

    def get(self, api_version, api_endpoint):
        """Connect to a Rubrik Cluster and perform a GET operation.

        Arguments:
            api_version {str} -- The version of the Rubrik CDM API to call.
            api_endpoint {str} -- The endpoint (ex. cluster/me) of the Rubrik CDM API to call.

        Returns:
            json -- The response body of the API call.
        """

        self._api_validation(api_version, api_endpoint)

        request_url = "https://{}/api/{}{}".format(self.node_ip, api_version, api_endpoint)
        request_url = quote(request_url, '://?=&')

        header = self._authorization_header()

        try:
            api_request = requests.get(request_url, verify=False, headers=header)
            # Raise an error if they request was not successful
            api_request.raise_for_status()
        except requests.exceptions.RequestException as error_message:
            sys.exit(error_message)

        response_body = api_request.json()

        return response_body

    def post(self, api_version, api_endpoint, config):
        """Connect to a Rubrik Cluster and perform a POST operation.

        Arguments:
            api_version {str} -- The version of the Rubrik CDM API to call.
            api_endpoint {str} -- The endpoint (ex. cluster/me) of the Rubrik CDM API to call.
            config {[type]} -- description

        Returns:
            json -- The response body of the API call.
        """

        self._api_validation(api_version, api_endpoint)

        config = json.dumps(config)

        request_url = "https://{}/api/{}{}".format(self.node_ip, api_version, api_endpoint)

        header = self._authorization_header()

        try:
            api_request = requests.post(request_url, data=config, verify=False, headers=header)
            # Raise an error if they request was not successful
            api_request.raise_for_status()
        except requests.exceptions.RequestException as error_message:
            sys.exit(error_message)

        response_body = api_request.json()

        return response_body

    def patch(self, api_version, api_endpoint, config):
        """Connect to a Rubrik Cluster and perform a PATCH operation.

        Arguments:
            api_version {str} -- The version of the Rubrik CDM API to call.
            api_endpoint {str} -- The endpoint (ex. cluster/me) of the Rubrik CDM API to call.
            config {dict} -- description

        Returns:
            json -- The response body of the API call.
        """

        self._api_validation(api_version, api_endpoint)

        config = json.dumps(config)

        request_url = "https://{}/api/{}{}".format(self.node_ip, api_version, api_endpoint)

        header = self._authorization_header()

        try:
            api_request = requests.patch(request_url, data=config, verify=False, headers=header)
            # Raise an error if they request was not successful
            api_request.raise_for_status()
        except requests.exceptions.RequestException as error_message:
            sys.exit(error_message)

        response_body = api_request.json()

        return response_body

    def delete(self, api_version, api_endpoint):
        """Connect to a Rubrik Cluster and perform a DELETE operation.

        Arguments:
            api_version {str} -- The version of the Rubrik CDM API to call.
            api_endpoint {str} -- The endpoint (ex. cluster/me) of the Rubrik CDM API to call.

        """

        self._api_validation(api_version, api_endpoint)

        request_url = "https://{}/api/{}{}".format(self.node_ip, api_version, api_endpoint)

        header = self._authorization_header()

        try:
            api_request = requests.delete(request_url, verify=False, headers=header)
            # Raise an error if they request was not successful
            api_request.raise_for_status()
        except requests.exceptions.RequestException as error_message:
            sys.exit(error_message)

        response_body = api_request.json()

        return response_body

    def job_status(self, url):
        """Connect to the Rubrik Cluster and get the status of a particular job.

        Arguments:
            url {str} -- The job status URL provided by a previous API call.

        Returns:
            json -- The response body of the API call.
        """

        header = self._authorization_header()

        try:
            api_request = requests.get(url, verify=False, headers=header)
            # Raise an error if they request was not successful
            api_request.raise_for_status()
        except requests.exceptions.RequestException as error_message:
            sys.exit(error_message)

        response_body = api_request.json()

        return response_body
