""" Collection of lib methods that interact with Polaris primitives"""

def get_sla_domains(self, sla_domain_name=""):
    """Retrieves dictionary of SLA Domain Names and Identifiers,
       or the ID of a single SLA Domain

    Arguments:
        sla_domain_name {str} -- Rubrik SLA Domain Name

   """
    query_name = "sla_domains"
    variables = {
        "filter": {
            "field": "NAME",
            "text": sla_domain_name
        }
    }
    request = self.query(None, self.graphql_query[query_name], variables)
    request_nodes = self._dump_nodes(request, query_name)
    if sla_domain_name and len(request_nodes) == 1:
        return request_nodes[0]['id']
    elif sla_domain_name and len(request_nodes) > 1:
        for i in request_nodes:
            if i['name'] == sla_domain_name:
                return i['id']
    else:
        return request_nodes

def submit_on_demand(self, object_ids, sla_id):
    """Submits On Demand Snapshot

    Arguments:
        object_ids [string] -- Array of Rubrik Object IDs
        sla_id string -- Rubrik SLA Domain ID
    """
    mutation_name = "on_demand"
    variables = {
        "objectIds": object_ids,
        "slaId": sla_id
    }
    request = self.query(None, self.graphql_mutation[mutation_name], variables)
    return request

def submit_assign_sla(self, object_ids, sla_id):
    """Submits a Rubrik SLA change for objects

        Arguments:
            object_ids [string] -- Array of Rubrik Object IDs
            sla_id string -- Rubrik SLA Domain ID
        """
    mutation_name = "assign_sla"
    variables = {
            "objectIds": object_ids,
            "slaId": sla_id
        }
    request = self.query(None, self.graphql_mutation[mutation_name], variables)
    return request


