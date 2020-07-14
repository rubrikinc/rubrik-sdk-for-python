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
This module contains the Rubrik SDK API class.
"""

import requests
import json
import time
try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+
from random import choice
from .exceptions import APICallException, InvalidParameterException, RubrikException, InvalidTypeException
import inspect


class Api():
    """This class contains the base API methods that can be called independently or internally in standalone functions."""

    def __init__(self, node_ip):
        super().__init__(node_ip)

    def _common_api(self, call_type, api_version, api_endpoint, config=None, job_status_url=None, timeout=15, authentication=True, params=None, gql_operation_name=None, gql_query=None, gql_variables=None):  # pylint: ignore
        """Internal method that consolidates the base API functions.

        Arguments:
            call_type {str} -- The HTTP Method for the type of RESTful API call being made. (choices: {'GET', 'POST', 'PATCH', 'DELETE', and 'JOB_STATUS'.})
            api_version {str} -- The version of the Rubrik CDM API to call. (choices: {v1, v2, internal})
            api_endpoint {str} -- The endpoint of the Rubrik CDM API to call (ex. /cluster/me).

        Keyword Arguments:
            params {dict} -- An optional dict containing variables in a key:value format to send with `GET` & `DELETE` API calls (default: {None})
            config {dict} -- The specified data to send with 'DELETE', `POST` and `PATCH` API calls. (default: {None})
            job_status_url {str} -- The job status URL provided by a previous API call. (default: {None})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})
            authentication {bool} -- Flag that specifies whether or not to utilize authentication when making the API call. (default: {True})

        Returns:
            dict -- The full API call response for the provided endpoint.
        """

        # Determine if authentication should be sent as part of the API Header
        if authentication:
            header = self._authorization_header()
        elif authentication is False:
            header = self._header()
        else:
            raise InvalidTypeException('"authentication" must be either True or False')
        try:
            # Determine which call type is being used and then set the relevant
            # variables for that call type
            if call_type == 'GET':
                request_url = "https://{}/api/{}{}".format(self.node_ip, api_version, api_endpoint)
                if params is not None:
                    request_url = request_url + "?" + '&'.join("{}={}".format(key, quote(str(val)))
                                                               for (key, val) in params.items())
                self.log('GET {}'.format(request_url))
                api_request = requests.get(
                    request_url, verify=False, headers=header, timeout=timeout)
            elif call_type == 'POST':
                config = json.dumps(config)
                request_url = "https://{}/api/{}{}".format(
                    self.node_ip, api_version, api_endpoint)
                self.log('POST {}'.format(request_url))
                self.log('Config: {}'.format(config))
                api_request = requests.post(request_url, verify=False, headers=header, data=config, timeout=timeout)
                self.log('Response: {}'.format(api_request.text))
            elif call_type == 'PATCH':
                config = json.dumps(config)
                request_url = "https://{}/api/{}{}".format(
                    self.node_ip, api_version, api_endpoint)
                self.log('PATCH {}'.format(request_url))
                self.log('Config: {}'.format(config))
                api_request = requests.patch(request_url, verify=False, headers=header, data=config, timeout=timeout)
            elif call_type == 'PUT':
                config = json.dumps(config)
                request_url = "https://{}/api/{}{}".format(
                    self.node_ip, api_version, api_endpoint)
                self.log('PUT {}'.format(request_url))
                self.log('Config: {}'.format(config))
                api_request = requests.put(request_url, verify=False, headers=header, data=config, timeout=timeout)
            elif call_type == 'DELETE':
                config = json.dumps(config)
                request_url = "https://{}/api/{}{}".format(
                    self.node_ip, api_version, api_endpoint)
                if params is not None:
                    request_url = request_url + "?" + '&'.join("{}={}".format(key, val)
                                                               for (key, val) in params.items())
                self.log('DELETE {}'.format(request_url))
                api_request = requests.delete(request_url, verify=False, headers=header, data=config, timeout=timeout)
            elif call_type == 'JOB_STATUS':
                self.log('JOB STATUS for {}'.format(job_status_url))
                api_request = requests.get(job_status_url, verify=False, headers=header, timeout=timeout)
            elif call_type == 'QUERY':
                config = json.dumps(config)
                request_url = "https://{}/api/internal/graphql".format(self.node_ip)
                self.log('POST {}'.format(request_url))
                if gql_operation_name is not None:
                    self.log('Operation Name: {}'.format(gql_operation_name))
                self.log('Query: {}'.format(gql_query))
                if gql_variables is not None:
                    self.log('Variables: {}'.format(gql_variables))
                api_request = requests.post(
                    request_url,
                    verify=False,
                    headers=header,
                    json={
                        "operationName": gql_operation_name,
                        "variables": gql_variables,
                        "query": "query {}".format(gql_query)},
                    timeout=timeout)
            else:
                raise InvalidParameterException('the _common_api() call_type must be one of the following: {}'.format(
                    ['GET', 'POST', 'PATCH', 'DELETE', 'QUERY', 'JOB_STATUS']))

            self.log(str(api_request) + "\n")
            try:
                # request.json() will fail on a 204 (No Content) so skip the response check
                if api_request.status_code != 204:
                    api_response = api_request.json()
                    # Check to see if an error message has been provided by Rubrik
                    for key, value in api_response.items():
                        if key == "errorType" or key == 'message':
                            error_message = api_response['message']
                            api_request.raise_for_status()

                        # Check for GQL error message in the data response
                        if key == "error":
                            error_message = api_response['error']
                            api_request.raise_for_status()

            except BaseException:
                api_request.raise_for_status()
        except requests.exceptions.ConnectTimeout:
            raise APICallException("Unable to establish a connection to the Rubrik cluster.")
        except requests.exceptions.ConnectionError:
            raise APICallException("Unable to establish a connection to the Rubrik cluster.")
        except requests.exceptions.ReadTimeout:
            raise APICallException(
                "The Rubrik cluster did not respond to the API request in the allotted amount of time. To fix this issue, increase the timeout value.")
        except requests.exceptions.HTTPError as error:

            try:
                error_message = json.loads(error.response.text)["message"]
            except BaseException:
                error_message = error.response.text

            raise APICallException(error_message)

        except requests.exceptions.RequestException as error:
            # If "error_message" has be defined raise that message else raise the request exception error
            try:
                error_message
            except NameError:
                raise APICallException(error)
            else:
                raise APICallException('' + error_message)
        else:
            try:
                # GQL error messages may not be flag as exceptions so we need to
                # manually check to determine if the error has occured to
                # raise an error on the provided message
                if call_type == "QUERY":
                    try:
                        error_message
                        raise APICallException(error_message)
                    except NameError:
                        try:
                            return api_request.json()["data"]
                        except BaseException:
                            pass
                
                # request.json() will fail on a 204 (No Content), so just the response code
                if api_request.status_code != 204:
                    return api_request.json()
                else:
                    return {'status_code': api_request.status_code}
            except BaseException:
                return {'status_code': api_request.status_code}

    def get(self, api_version, api_endpoint, timeout=15, authentication=True, params=None):
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

        if self.function_name == "":
            self.function_name = inspect.currentframe().f_code.co_name

        return self._common_api(
            'GET',
            api_version,
            api_endpoint,
            config=None,
            job_status_url=None,
            timeout=timeout,
            authentication=authentication,
            params=params)

    def post(self, api_version, api_endpoint, config, timeout=15, authentication=True):
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

        if self.function_name == "":
            self.function_name = inspect.currentframe().f_code.co_name

        return self._common_api(
            'POST',
            api_version,
            api_endpoint,
            config=config,
            job_status_url=None,
            timeout=timeout,
            authentication=authentication)

    def query(self, query, operation_name=None, variables=None, timeout=15, authentication=True):
        """Send a GraphQL query to a CDM cluster.

        Arguments:
            query {str} -- The main GraphQL query body.
            operation_name {str} -- A meaningful and explicit name for your GraphQL operation. Think of this just like a function name in your favorite programming language. (default: {None})
            variables {dict} -- The variables to pass into your query. (default: {None})

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})
            authentication {bool} -- Flag that specifies whether or not to utilize authentication when making the API call. (default: {True})

        Returns:
            dict -- The response["data"] body of the API call.
        """

        if self.function_name == "":
            self.function_name = inspect.currentframe().f_code.co_name

        return self._common_api(
            'QUERY',
            api_version=None,
            api_endpoint=None,
            config=None,
            job_status_url=None,
            timeout=timeout,
            authentication=authentication,
            params=None,
            gql_operation_name=operation_name,
            gql_query=query,
            gql_variables=variables)

    def patch(self, api_version, api_endpoint, config, timeout=15, authentication=True):
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

        if self.function_name == "":
            self.function_name = inspect.currentframe().f_code.co_name

        return self._common_api(
            'PATCH',
            api_version,
            api_endpoint,
            config=config,
            job_status_url=None,
            timeout=timeout,
            authentication=authentication)

    def put(self, api_version, api_endpoint, config, timeout=15, authentication=True):
        """Send a PUT request to the provided Rubrik API endpoint.

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

        if self.function_name == "":
            self.function_name = inspect.currentframe().f_code.co_name

        return self._common_api(
            'PUT',
            api_version,
            api_endpoint,
            config=config,
            job_status_url=None,
            timeout=timeout,
            authentication=authentication)

    def delete(self, api_version, api_endpoint, timeout=15, authentication=True, config=None, params=None):
        """Send a DELETE request to the provided Rubrik API endpoint.

        Arguments:
            api_version {str} -- The version of the Rubrik CDM API to call. (choices: {v1, v2, internal})
            api_endpoint {str} -- The endpoint of the Rubrik CDM API to call (ex. /cluster/me).

        Keyword Arguments:
            params {dict} -- An optional dict containing variables in a key:value format to send with `GET` & `DELETE` API calls . Mutually exclusive with config (default: {None})
            config {dict} -- The specified data to send with the API call. Mutually exclusive with params (default: {None})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})
            authentication {bool} -- Flag that specifies whether or not to utilize authentication when making the API call. (default: {True})

        Returns:
            dict -- The response body of the API call.
        """

        if self.function_name == "":
            self.function_name = inspect.currentframe().f_code.co_name

        if config is not None and params is not None:
            raise InvalidParameterException(
                "DELETE cannot have both params and config set in the same call.")

        return self._common_api(
            'DELETE',
            api_version,
            api_endpoint,
            config=config,
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

        if self.function_name == "":
            self.function_name = inspect.currentframe().f_code.co_name

        if not isinstance(wait_for_completion, bool):
            raise InvalidTypeException(
                'The job_status() wait_for_completion argument must be True or False.')

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

                in_progress_status = [
                    "QUEUED",
                    "RUNNING",
                    "FINISHING",
                    "TO_FINISH",
                    "TO_RETRY",
                    "ACQUIRING",
                    "TO_YIELDING",
                    "YIELDING",
                    "TO_YIELDED",
                    "YIELDED"]

                canceling_status = ["CANCELING", "TO_CANCEL"]

                failing_status = ["TO_UNDO", "UNDOING"]

                if job_status == "SUCCEEDED":
                    self.log('Job Complete\n')
                    job_status = api_call['status']
                    break
                elif job_status == "CANCELED":
                    self.log('Job Cancelled\n')
                    job_status = api_call['status']
                    break
                elif job_status in in_progress_status:
                    self.log('Job Progress {}%\n'.format(api_call['progress']))
                    job_status = api_call['status']
                    time.sleep(10)
                    continue
                elif job_status in cancelling_status:
                    self.log('Job is being Cancelled {}%\n'.format(api_call['progress']))
                    job_status = api_call['status']
                    time.sleep(10)
                    continue
                elif job_status in failing_status:
                    self.log('Job Failing {}%\n'.format(api_call['progress']))
                    job_status = api_call['status']
                    time.sleep(10)
                    continue
                else:
                    # Job FAILED
                    raise RubrikException('{}'.format(str(api_call)))

        else:
            api_call = self._common_api(
                'JOB_STATUS',
                api_version=None,
                api_endpoint=None,
                config=None,
                job_status_url=url,
                timeout=timeout)

        return api_call
