""" Collection of lib methods that interact with Polaris primitives"""

def get_sla_domains(self, _sla_domain_name=""):
    """Retrieves dictionary of SLA Domain Names and Identifiers,
       or the ID of a single SLA Domain

    Arguments:
        sla_domain_name {str} -- Rubrik SLA Domain Name

   """
    try:
        _query_name = "sla_domains"
        _variables = {
            "filter": {
                "field": "NAME",
                "text": _sla_domain_name
            }
        }
        _request = self._query(None, self._graphql_query[_query_name], _variables)
        _request_nodes = self._dump_nodes(_request, _query_name)
        if _sla_domain_name and len(_request_nodes) == 1:
            return _request_nodes[0]['id']
        elif _sla_domain_name and len(_request_nodes) > 1:
            for i in _request_nodes:
                if i['name'] == _sla_domain_name:
                    return i['id']
        else:
            return _request_nodes
    except Exception as e:
        print(e)

def submit_on_demand(self, object_ids, sla_id, **kwargs):
    """Submits On Demand Snapshot

    Arguments:
        object_ids [string] -- Array of Rubrik Object IDs
        sla_id string -- Rubrik SLA Domain ID
    """
    try:
        _mutation_name = "on_demand"
        _variables = {
            "objectIds": object_ids,
            "slaId": sla_id
        }
        _request = self._query(None, self._graphql_mutation[_mutation_name], _variables)
        _result = self._dump_nodes(_request, _mutation_name)
        _results = []
        if _result['errors']:
            for _error_object in _result['errors']:
                _results.append(_error_object)
        if 'wait' in kwargs:
            _results = self._monitor_task(_result['taskchainUuids'])
        return _results
            #todo: find a better way to report errors per uuid
    except Exception as e:
        print(e)

def submit_assign_sla(self, _object_ids, _sla_id):
    """Submits a Rubrik SLA change for objects

        Arguments:
            object_ids [string] -- Array of Rubrik Object IDs
            sla_id string -- Rubrik SLA Domain ID
        """
    try:
        _mutation_name = "assign_sla"
        _variables = {
                "objectIds": _object_ids,
                "slaId": _sla_id
            }
        request = self._query(None, self._graphql_mutation[_mutation_name], _variables)
        return  self._dump_nodes(request, _mutation_name)
    except Exception as e:
        print(e)

def get_task_status(self, _task_chain_id):
    """Retrieve task status from Polaris

        Arguments:
            task_id [uuid] -- Task UUID from request
        """
    _query_name = "taskchain_status"
    try:
        _variables = {
            "filter": _task_chain_id
        }
        _request = self._query(None, self._graphql_query[_query_name], _variables)
        _response = self._dump_nodes(_request, _query_name)
        return _response['taskchain']['state']
    except Exception as e:
        print(e)





