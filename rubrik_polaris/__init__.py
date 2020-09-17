"rubrik: A Python package for interacting with the Rubrik Polaris API."

from .rubrik_polaris import PolarisClient

import logging

from .lib.common.connection import query, get_access_token as _get_access_token
from .lib.common.graphql import _dump_nodes, _get_query_names_from_graphql_query
from .lib.common.polaris import get_sla_domains, submit_on_demand, submit_assign_sla
from rubrik_polaris.lib.compute import get_instances_azure, get_instances_ec2, get_instances_gce
# from .lib.accounts import get_accounts_aws, get_accounts_azure, get_accounts_gcp
#    from .lib.compute import get_object_ids_azure, get_object_ids_ec2, get_object_ids_gc

# Define the logging params
console_output_handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] -- %(message)s")
console_output_handler.setFormatter(formatter)

log = logging.getLogger(__name__)
log.addHandler(console_output_handler)

__version__ = "1.0"
__author__ = "Rubrik Inc"
__all__ = []