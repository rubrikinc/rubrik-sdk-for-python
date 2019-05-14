# Copyright 2019 Rubrik, Inc.
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


class RubrikException(Exception):
    """Base class for exceptions in this module."""
    pass


class CDMVersionException(RubrikException):
    """Exception used to handle situations when the Rubrik cluster is not running a minimum
    required version of CDM.

    Arguments:
        RubrikException {class} -- Base class for exceptions in this module
    """

    def __init__(self, cdm_version):
        self.cdm_version = cdm_version

    def __str__(self):
        return("The Rubrik cluster must be running CDM version {} or later.".format(self.cdm_version))


class APICallException(RubrikException):
    """Exception related to the underlying API call being made to the Rubrik cluster."""
    pass


class InvalidParameterException(RubrikException):
    """Exception related to the parameters provided in the function. This can be related an issue with the value itself
    or the value provided not being found on the cluster."""
    pass


class InvalidTypeException(RubrikException):
    """Exception related to the wrong Python type being provided in the function parameters."""
    pass
