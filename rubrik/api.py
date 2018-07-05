import requests
import json
import sys
try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+


class Api():
    """[summary]

    """

    def __init__(self, node_ip, username, password):
        super().__init__(node_ip, username, password)

    def get(self, api_version, api_endpoint):
        """Connect to a Rubrik Cluster and perform a GET operation.

        Arguments:
            api_version {str} -- The version of the Rubrik CDM API to call.
            api_endpoint {str} -- The endpoint (ex. cluster/me) of the Rubrik CDM API to call.

        Returns:
            dict -- The response body of the API call.
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
            dict -- The response body of the API call.
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
            dict -- The response body of the API call.
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
            dict -- The response body of the API call.
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
