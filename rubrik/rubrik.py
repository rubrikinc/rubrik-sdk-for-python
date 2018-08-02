# Copyright 2018 Rubrik, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License prop
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import requests
import sys
import os
import logging
from random import choice


from .cluster import Cluster
from .data_management import Data_Management

# Define the logging params
console_output_handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] -- %(message)s")
console_output_handler.setFormatter(formatter)

log = logging.getLogger(__name__)
log.addHandler(console_output_handler)


_CLUSTER = Cluster
_DATA_MANAGEMENT = Data_Management


class Connect(_CLUSTER, _DATA_MANAGEMENT):
    """[summary]

    Arguments:
        _CLUSTER {class} -- This class contains methods related to the managment of the Rubrik Cluster itself.
        _DATA_MANAGEMENT {class} - [description]
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

        self.log("User Provided Node IP: {}".format(self.node_ip))
        self.log("Username: {}".format(self.username))
        self.log("Password: *******\n")

        self.log("Generating a list of all Cluster Node IPs.")
        self.node_ip = self.cluster_node_ip(timeout=5)

    @staticmethod
    def log(log_message):
        """Internal method used for debug log messages.

        Arguments:
            log_message {str} -- The message to pass to the debug log.
        """
        log.debug(log_message)

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
