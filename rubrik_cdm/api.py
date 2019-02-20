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

"""
This module contains the Rubrik SDK API class.
"""

import requests
import json
import sys
import time
try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+
from random import choice


class Api():
    """This class contains the base API methods that can be called independently or internally in standalone functions."""

    def __init__(self, node_ip):
        super().__init__(node_ip)

    def _common_api(self, call_type, api_version, api_endpoint, config=None,
                    job_status_url=None, timeout=15, authentication=True, params=None):
        """Internal method that consolidates the base API functions.

        Arguments:
            call_type {str} -- The HTTP Method for the type of RESTful API call being made. (choices: {'GET', 'POST', 'PATCH', 'DELETE', and 'JOB_STATUS'.})
            api_version {str} -- The version of the Rubrik CDM API to call. (choices: {v1, v2, internal})
            api_endpoint {str} -- The endpoint of the Rubrik CDM API to call (ex. /cluster/me).

        Keyword Arguments:
            params {dict} -- An optional dict containing variables in a key:value format to send with `GET` & `DELETE` API calls (default: {None})
            config {dict} -- The specified data to send with `POST` and `PATCH` API calls. (default: {None})
            job_status_url {str} -- The job status URL provided by a previous API call. (default: {None})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})
            authentication {bool} -- Flag that specifies whether or not to utilize authentication when making the API call. (default: {True})

        Returns:
            dict -- The full API call response for the provided endpoint.
        """
        if call_type != 'JOB_STATUS':
            self._api_validation(api_version, api_endpoint)

        # Determine if authentication should be sent as part of the API Header
        if authentication:
            header = self._authorization_header()
        elif authentication is False:
            header = self._header()
        else:
            sys.exit('Error: "authentication" must be either True or False')

        try:
            # Determine which call type is being used and then set the relevant
            # variables for that call type
            if call_type == 'GET':
                request_url = "https://{}/api/{}{}".format(self.node_ip, api_version, api_endpoint)
                if params is not None:
                    request_url = request_url + "?" + '&'.join("{}={}".format(key, val)
                                                               for (key, val) in params.items())
                request_url = quote(request_url, '://?=&')
                self.log('GET {}'.format(request_url))
                api_request = requests.get(
                    request_url, verify=False, headers=header, timeout=timeout)
            elif call_type == 'POST':
                config = json.dumps(config)
                request_url = "https://{}/api/{}{}".format(
                    self.node_ip, api_version, api_endpoint)
                self.log('POST {}'.format(request_url))
                self.log('Config: {}'.format(config))
                api_request = requests.post(
                    request_url,
                    verify=False,
                    headers=header,
                    data=config,
                    timeout=timeout)
            elif call_type == 'PATCH':
                config = json.dumps(config)
                request_url = "https://{}/api/{}{}".format(
                    self.node_ip, api_version, api_endpoint)
                self.log('PATCH {}'.format(request_url))
                self.log('Config: {}'.format(config))
                api_request = requests.patch(request_url, verify=False, headers=header, data=config, timeout=timeout)
            elif call_type == 'DELETE':
                request_url = "https://{}/api/{}{}".format(
                    self.node_ip, api_version, api_endpoint)
                if params is not None:
                    request_url = request_url + "?" + '&'.join("{}={}".format(key, val)
                                                               for (key, val) in params.items())
                self.log('DELETE {}'.format(request_url))
                api_request = requests.delete(
                    request_url, verify=False, headers=header, timeout=timeout)
            elif call_type == 'JOB_STATUS':
                self.log('JOB STATUS for {}'.format(job_status_url))
                api_request = requests.get(job_status_url, verify=False, headers=header, timeout=timeout)
            else:
                sys.exit('Error: the _common_api() call_type must be one of the following: {}'.format(
                    ['GET', 'POST', 'PATCH', 'DELETE', 'JOB_STATUS']))

            self.log(str(api_request) + "\n")
            try:
                api_response = api_request.json()
                # Check to see if an error message has been provided by Rubrik
                for key, value in api_response.items():
                    if key == "errorType" or key == 'message':
                        error_message = api_response['message']
                        api_request.raise_for_status()

            except BaseException:
                api_request.raise_for_status()
        except requests.exceptions.ConnectTimeout:
            sys.exit(
                "Error: Unable to establish a connection to the Rubrik cluster.")
        except requests.exceptions.ReadTimeout:
            sys.exit("Error: The Rubrik cluster did not respond to the API request in the allotted amount of time. To fix this issue, increase the timeout value.")
        except requests.exceptions.RequestException as error:
            # If "error_message" has be defined sys.exit that message else
            # sys.exit the request exception error
            try:
                error_message
            except NameError:
                sys.exit(error)
            else:
                sys.exit('Error: ' + error_message)
        else:
            try:
                return api_request.json()
            except BaseException:
                return {'status_code': api_request.status_code}

    def get(self, api_version, api_endpoint, timeout=15,
            authentication=True, params=None):
        """Send a GET request to the provided Rubrik API endpoint.

        Arguments:
            api_version {str} -- The version of the Rubrik CDM API to call. (choices: {v1, v2, internal})
            api_endpoint {str} -- The endpoint of the Rubrik CDM API to call (ex. /cluster/me).

        Keyword Arguments:
            params {dict} -- An optional dict containing variables in a key:value format to send with `GET` & `DELETE` API calls (default: {None})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})
            authentication {bool} -- Flag that specifies whether or not to utilize authentication when making the API call. (default: {True})

        Returns:
            dict -- The response body of the API call.
        """

        return self._common_api(
            'GET',
            api_version,
            api_endpoint,
            config=None,
            job_status_url=None,
            timeout=timeout,
            authentication=authentication,
            params=params)

    def post(self, api_version, api_endpoint, config,
             timeout=15, authentication=True):
        """Send a POST request to the provided Rubrik API endpoint.

        Arguments:
            api_version {str} -- The version of the Rubrik CDM API to call. (choices: {v1, v2, internal})
            api_endpoint {str} -- The endpoint of the Rubrik CDM API to call (ex. /cluster/me).
            config {dict} -- The specified data to send with the API call.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})
            authentication {bool} -- Flag that specifies whether or not to utilize authentication when making the API call. (default: {True})

        Returns:
            dict -- The response body of the API call.
        """

        return self._common_api(
            'POST',
            api_version,
            api_endpoint,
            config=config,
            job_status_url=None,
            timeout=timeout,
            authentication=authentication)

    def patch(self, api_version, api_endpoint, config,
              timeout=15, authentication=True):
        """Send a PATCH request to the provided Rubrik API endpoint.

        Arguments:
            api_version {str} -- The version of the Rubrik CDM API to call. (choices: {v1, v2, internal})
            api_endpoint {str} -- The endpoint of the Rubrik CDM API to call (ex. /cluster/me).
            config {dict} -- The specified data to send with the API call.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})
            authentication {bool} -- Flag that specifies whether or not to utilize authentication when making the API call. (default: {True})

        Returns:
            dict -- The response body of the API call.
        """

        return self._common_api(
            'PATCH',
            api_version,
            api_endpoint,
            config=config,
            job_status_url=None,
            timeout=timeout,
            authentication=authentication)

    def delete(self, api_version, api_endpoint, timeout=15,
               authentication=True, params=None):
        """Send a DELETE request to the provided Rubrik API endpoint.

        Arguments:
            api_version {str} -- The version of the Rubrik CDM API to call. (choices: {v1, v2, internal})
            api_endpoint {str} -- The endpoint of the Rubrik CDM API to call (ex. /cluster/me).

        Keyword Arguments:
            params {dict} -- An optional dict containing variables in a key:value format to send with `GET` & `DELETE` API calls (default: {None})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})
            authentication {bool} -- Flag that specifies whether or not to utilize authentication when making the API call. (default: {True})

        Returns:
            dict -- The response body of the API call.
        """

        return self._common_api(
            'DELETE',
            api_version,
            api_endpoint,
            config=None,
            job_status_url=None,
            timeout=timeout,
            authentication=authentication,
            params=params)

    def job_status(self, url, wait_for_completion=True, timeout=15):
        """Certain Rubrik operations (on-demand snapshots, live mounts, etc.) may not complete instantaneously. In those cases we have
        the ability to monitor the status of the job through a job status url provided in the actions API response body. This function will
        perform a GET operation on the provided url and return the jobs status.

        Arguments:
            url {str} -- The job status URL provided by a previous API call.

        Keyword Arguments:
            wait_for_completion {bool} -- Flag that determines if the method should wait for the job to complete before exiting. (default: {True})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})


        Returns:
            dict -- The response body of the API call.
        """

        if not isinstance(wait_for_completion, bool):
            sys.exit(
                'Error: The job_status() wait_for_completion argument must be True or False.')

        if wait_for_completion:
            self.log('Job Status: Waiting for the job to complete.')
            api_call = self._common_api(
                'JOB_STATUS',
                api_version=None,
                api_endpoint=None,
                config=None,
                job_status_url=url,
                timeout=timeout)

            while True:

                api_call = self._common_api(
                    'JOB_STATUS',
                    api_version=None,
                    api_endpoint=None,
                    config=None,
                    job_status_url=url,
                    timeout=timeout)

                job_status = api_call['status']

                if job_status == "SUCCEEDED":
                    self.log('Job Progress 100%\n')
                    job_status = api_call['status']
                    break
                elif job_status == "QUEUED" or "RUNNING":
                    self.log('Job Progress {}%\n'.format(api_call['progress']))
                    job_status = api_call['status']
                    time.sleep(10)
                    continue
                else:
                    sys.exit('Error: {}'.format(str(api_call)))

        else:
            api_call = self._common_api(
                'JOB_STATUS',
                api_version=None,
                api_endpoint=None,
                config=None,
                job_status_url=url,
                timeout=timeout)

        return api_call
