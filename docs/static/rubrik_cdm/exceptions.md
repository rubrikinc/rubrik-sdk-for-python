# Exceptions

The Rubrik SDK for Python will utilizes the following custom exceptions.

## CDMVersionException

Exception used to handle situations when the Rubrik cluster is not running a minimum required version of CDM.

## APICallException

Exception related to the underlying API call being made to the Rubrik cluster.

## InvalidParameterException

Exception related to the parameters provided in the function. This can be related an issue with the value itself or the value provided not being found on the cluster.

## TypeException

Exception related to the wrong Python type being provided in the function parameters.
