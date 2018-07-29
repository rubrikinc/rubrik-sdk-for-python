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

    def get(self, api_version, api_endpoint, timeout=5, authentication=True):
        """Connect to a Rubrik Cluster and perform a GET operation.

        Arguments:
            api_version {str} -- The version of the Rubrik CDM API to call.
            api_endpoint {str} -- The endpoint (ex. cluster/me) of the Rubrik CDM API to call.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik Cluster. (default: {5})

        Returns:
            dict -- The response body of the API call.
        """

        self._api_validation(api_version, api_endpoint)

        request_url = "https://{}/api/{}{}".format(self.node_ip, api_version, api_endpoint)
        request_url = quote(request_url, '://?=&')

        self._log('GET {}'.format(request_url))

        if authentication == True:
            header = self._authorization_header()
        elif authentication == False:
            header = self._header()
        else:
            sys.exit('Error: "authentication" must be either True or False')

        try:
            api_request = requests.get(request_url, verify=False, headers=header, timeout=timeout)
            self._log(str(api_request) + "\n")
            try:
                api_response = api_request.json()
                # Check to see if an error message has been provided by Rubrik
                for key, value in api_response.items():
                    if key == "errorType":
                        error_message = api_response['message']
                        api_request.raise_for_status()
            except:
                api_request.raise_for_status()
        except requests.exceptions.ConnectTimeout:
            sys.exit('Error: Unable to establish a connection to the Rubrik Cluster.')
        except requests.exceptions.RequestException as error:
            # If "error_message" has be defined sys.exit that message else sys.exit the request exception error
            try:
                error_message
            except NameError:
                sys.exit(error)
            else:
                sys.exit('Error: ' + error_message)

        return api_request.json()

    def post(self, api_version, api_endpoint, config, timeout=5, authentication=True):
        """Connect to a Rubrik Cluster and perform a POST operation.

        Arguments:
            api_version {str} -- The version of the Rubrik CDM API to call.
            api_endpoint {str} -- The endpoint (ex. cluster/me) of the Rubrik CDM API to call.
            config {[type]} -- description

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik Cluster. (default: {5})

        Returns:
            dict -- The response body of the API call.
        """

        self._api_validation(api_version, api_endpoint)

        config = json.dumps(config)

        request_url = "https://{}/api/{}{}".format(self.node_ip, api_version, api_endpoint)

        self._log('POST {}'.format(request_url))
        self._log('Config: {}'.format(config))

        if authentication == True:
            header = self._authorization_header()
        elif authentication == False:
            header = self._header()
        else:
            sys.exit('Error: "authentication" must be either True or False')

        try:
            api_request = requests.post(request_url, verify=False, headers=header, data=config, timeout=timeout)
            self._log(str(api_request) + "\n")
            try:
                api_response = api_request.json()
                # Check to see if an error message has been provided by Rubrik
                for key, value in api_response.items():
                    if key == "errorType":
                        error_message = api_response['message']
                        api_request.raise_for_status()
            except:
                api_request.raise_for_status()
        except requests.exceptions.ConnectTimeout:
            sys.exit('Error: Unable to establish a connection to the Rubrik Cluster.')
        except requests.exceptions.RequestException as error:
            # If "error_message" has be defined sys.exit that message else sys.exit the request exception error
            try:
                error_message
            except NameError:
                sys.exit(error)
            else:
                sys.exit('Error: ' + error_message)

        return api_request.json()

    def patch(self, api_version, api_endpoint, config, timeout=5):
        """Connect to a Rubrik Cluster and perform a PATCH operation.

        Arguments:
            api_version {str} -- The version of the Rubrik CDM API to call.
            api_endpoint {str} -- The endpoint (ex. cluster/me) of the Rubrik CDM API to call.
            config {dict} -- description

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik Cluster. (default: {5})

        Returns:
            dict -- The response body of the API call.
        """

        self._api_validation(api_version, api_endpoint)

        config = json.dumps(config)

        request_url = "https://{}/api/{}{}".format(self.node_ip, api_version, api_endpoint)

        self._log('PATCH {}'.format(request_url))
        self._log('Config: {}'.format(config))

        header = self._authorization_header()

        try:
            api_request = requests.patch(request_url, verify=False, headers=header, data=config, timeout=timeout)
            self._log(str(api_request) + "\n")
            try:
                api_response = api_request.json()
                # Check to see if an error message has been provided by Rubrik
                for key, value in api_response.items():
                    if key == "errorType":
                        error_message = api_response['message']
                        api_request.raise_for_status()
            except:
                api_request.raise_for_status()
        except requests.exceptions.ConnectTimeout:
            sys.exit('Error: Unable to establish a connection to the Rubrik Cluster.')
        except requests.exceptions.RequestException as error:
            # If "error_message" has be defined sys.exit that message else sys.exit the request exception error
            try:
                error_message
            except NameError:
                sys.exit(error)
            else:
                sys.exit('Error: ' + error_message)

        return api_request.json()

    def delete(self, api_version, api_endpoint, timeout=5):
        """Connect to a Rubrik Cluster and perform a DELETE operation.

        Arguments:
            api_version {str} -- The version of the Rubrik CDM API to call.
            api_endpoint {str} -- The endpoint (ex. cluster/me) of the Rubrik CDM API to call.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik Cluster. (default: {5})
        """

        self._api_validation(api_version, api_endpoint)

        request_url = "https://{}/api/{}{}".format(self.node_ip, api_version, api_endpoint)

        self._log('DELETE {}'.format(request_url))

        header = self._authorization_header()

        try:
            api_request = requests.delete(request_url, verify=False, headers=header, timeout=timeout)
            self._log(str(api_request) + "\n")
            try:
                api_response = api_request.json()
                # Check to see if an error message has been provided by Rubrik
                for key, value in api_response.items():
                    if key == "errorType":
                        error_message = api_response['message']
                        api_request.raise_for_status()
            except:
                api_request.raise_for_status()
        except requests.exceptions.ConnectTimeout:
            sys.exit('Error: Unable to establish a connection to the Rubrik Cluster.')
        except requests.exceptions.RequestException as error:
            # If "error_message" has be defined sys.exit that message else sys.exit the request exception error
            try:
                error_message
            except NameError:
                sys.exit(error)
            else:
                sys.exit('Error: ' + error_message)

        return api_request.json()

    def job_status(self, url, timeout=5):
        """Connect to the Rubrik Cluster and get the status of a particular job.

        Arguments:
            url {str} -- The job status URL provided by a previous API call.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik Cluster. (default: {5})

        Returns:
            dict -- The response body of the API call.
        """

        header = self._authorization_header()

        self._log('Job Status {}'.format(url))

        header = self._authorization_header()

        try:
            api_request = requests.get(url, verify=False, headers=header, timeout=timeout)
            self._log(str(api_request) + "\n")
            try:
                api_response = api_request.json()
                # Check to see if an error message has been provided by Rubrik
                for key, value in api_response.items():
                    if key == "errorType":
                        error_message = api_response['message']
                        api_request.raise_for_status()
            except:
                api_request.raise_for_status()
        except requests.exceptions.ConnectTimeout:
            sys.exit('Error: Unable to establish a connection to the Rubrik Cluster.')
        except requests.exceptions.RequestException as error:
            # If "error_message" has be defined sys.exit that message else sys.exit the request exception error
            try:
                error_message
            except NameError:
                sys.exit(error)
            else:
                sys.exit('Error: ' + error_message)

        return api_request.json()
