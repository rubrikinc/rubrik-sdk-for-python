"rubrik: A Python package for interacting with the Rubrik Polaris API."

from .rubrik_polaris import PolarisClient

import logging



# Define the logging params
console_output_handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] -- %(message)s")
console_output_handler.setFormatter(formatter)

log = logging.getLogger(__name__)
log.addHandler(console_output_handler)

__version__ = "1.0"
__author__ = "Rubrik Inc"
__all__ = []