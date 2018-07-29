import base64
import requests
import sys
import os
import logging


from .api import Api
from .cluster import Cluster

# Define the logging params
console_output_handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)s] --- %(message)s")
console_output_handler.setFormatter(formatter)

log = logging.getLogger(__name__)
log.addHandler(console_output_handler)


_API = Api
_CLUSTER = Cluster


class Connect(_API, _CLUSTER):
    """[summary]

    Arguments:
        _API {class} -- [description]
        _CORE {class} -- [description]
    """

    def __init__(self, node_ip=None, username=None, password=None):

        if node_ip is not None:
            self.node_ip = node_ip
        else:
            node_ip = os.environ.get('rubrik_cdm_node_ip')
            if node_ip is None:
                sys.exit("Error: The Rubrik CDM Node IP has not been provided.")
            else:
                self.node_ip = node_ip

        if username is not None:
            self.username = username
        else:
            username = os.environ.get('rubrik_cdm_username')
            if username is None:
                sys.exit("Error: The Rubrik CDM Username has not been provided.")
            else:
                self.username = username

        if password is not None:
            self.password = password
        else:
            password = os.environ.get('rubrik_cdm_password')
            if password is None:
                sys.exit("Error: The Rubrik CDM Password has not been provided.")
            else:
                self.password = password

        log.debug("Node IP: {}".format(self.node_ip))
        log.debug("Username: {}".format(self.username))
        log.debug("Password: {}\n".format(self.password))

    def _authorization_header(self):
        """Internal method used to create the authorization header used in the API calls.

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

    @staticmethod
    def _header():
        """Internal method used to create the a header without authorization used in the API calls.

        Returns:
            dict -- The header that does not include any authorization.
        """

        header = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        return header

    @staticmethod
    def _api_validation(api_version, api_endpoint):
        """Internal method used to validate the API Version and API Endpoint provided by the end user

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
