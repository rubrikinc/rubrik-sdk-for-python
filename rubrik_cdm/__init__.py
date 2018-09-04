"rubrik: A Python package for interacting with the Rubrik CDM API."

from .rubrik_cdm import Connect
from .rubrik_cdm import Bootstrap

import logging

# Define the logging params
console_output_handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] -- %(message)s")
console_output_handler.setFormatter(formatter)

log = logging.getLogger(__name__)
log.addHandler(console_output_handler)

__version__ = "1.0"
__author__ = "Rubrik Ranger Team"
__all__ = []
