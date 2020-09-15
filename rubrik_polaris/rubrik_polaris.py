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

import logging
import requests

from .exceptions import InvalidParameterException, PolarisException, APICallException


class PolarisClient:
    
    def __init__(self, domain, username, password, enable_logging=False, logging_level="debug"):
        valid_logging_levels = {
            "debug": logging.DEBUG,
            "critical": logging.CRITICAL,
            "error": logging.ERROR,
            "warning": logging.WARNING,
            "info": logging.INFO,
        }

        if logging_level not in valid_logging_levels:
            raise InvalidParameterException(
                "'{}' is not a valid logging_level. Valid choices are 'debug', 'critical', 'error', 'warning', or 'info'.".format(logging_level))

        # Enable logging for the SDK
        self.logging_level = logging_level
        if enable_logging:
            logging.getLogger().setLevel(valid_logging_levels[self.logging_level])

        self.domain = domain

        self._log("Polaris Domain: {}".format(self.domain))

        self.username = username
        self.password = password
        self.access_token = self._get_access_token()

        self.headers = {
            'Content-Type': 'application/json', 
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.access_token
        }

        self.baseurl = "https://" + self.domain + ".my.rubrik.com/api/graphql"



    def query(self, operation_name=None, query=None, variables=None, timeout=15):
        self._log('POST {}'.format(self.baseurl))
        
        if operation_name is not None:
            self._log('Operation Name: {}'.format(operation_name))
        
        self._log('Query: {}'.format(query))
        
        if variables is not None:
            self._log('Variables: {}'.format(variables))

        api_request = requests.post(
            self.baseurl,
            verify=False,
            headers=self.headers,
            json={
                "operationName": operation_name,
                "variables": variables,
                "query": "{}".format(query)
            },
            timeout=timeout
        )

        self._log(str(api_request) + "\n")
        try:
            api_response = api_request.json()
        except BaseException:
            api_request.raise_for_status()

        return api_response


    def schema(self):
        query = """
        fragment FullType on __Type {
            kind
            name
            fields(includeDeprecated: true) {
                name
                args {
                    ...InputValue
                }
                type {
                    ...TypeRef
                }
                isDeprecated
                deprecationReason
            }
            inputFields {
                ...InputValue
            }
            interfaces {
                ...TypeRef
            }
            enumValues(includeDeprecated: true) {
                name
                isDeprecated
                deprecationReason
            }
            possibleTypes {
                ...TypeRef
            }
        }
        fragment InputValue on __InputValue {
            name
            type {
                ...TypeRef
            }
            defaultValue
        }
        fragment TypeRef on __Type {
            kind
            name
            ofType {
                kind
                name
                ofType {
                    kind
                    name
                    ofType {
                        kind
                        name
                        ofType {
                            kind
                            name
                            ofType {
                                kind
                                name
                                ofType {
                                    kind
                                    name
                                    ofType {
                                        kind
                                        name
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        query IntrospectionQuery {
            __schema {
                queryType {
                    name
                }
                mutationType {
                    name
                }
                types {
                    ...FullType
                }
                directives {
                    name
                    locations
                    args {
                        ...InputValue
                    }
                }
            }
        }
        """
        return self.query(query=query)


    # Private 

    def _get_access_token(self):
        credentials = '{}:{}'.format(self.username, self.password)

        graphql_service_endpoint = 'https://{}.my.rubrik.com/api/session'.format(self.domain)

        payload = {
            "username": self.username,
            "password": self.password
        }
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain'
        }
        request = requests.post(graphql_service_endpoint, json=payload, headers=headers, verify=False)

        return request.json()['access_token']


    def _log(self, log_message):
        """Create properly formatted debug log messages.

        Arguments:
            log_message {str} -- The message to pass to the debug log.
        """

        log = logging.getLogger(__name__)

        set_logging = {
            "debug": log.debug,
            "critical": log.critical,
            "error": log.error,
            "warning": log.warning,
            "info": log.info

        }
        set_logging[self.logging_level](log_message)
