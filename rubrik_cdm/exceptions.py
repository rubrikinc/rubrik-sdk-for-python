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


class APICallException(Exception):
    """Base class for exceptions in this module."""
    pass
