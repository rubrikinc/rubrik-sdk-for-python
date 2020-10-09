""" Collection of lib methods that interact with Polaris primitives"""
from dateutil.tz import tzlocal


def get_sla_domains(self, sla_domain_name=""):
    """Retrieves dictionary of SLA Domain Names and Identifiers, or the ID of a single SLA Domain

    Arguments:
        sla_domain_name {str} -- Rubrik SLA Domain name

    Returns:
        str -- ID for the given SLA Domain name as given by `sla_domain_name`
        dict -- If a `sla_domain_name` is not given or not found, the complete set of SLA domains will be returned
    """
    try:
        _query_name = "sla_domains"
        _variables = {
            "filter": {
                "field": "NAME",
                "text": sla_domain_name
            }
        }
        _request = self._query(None, self._graphql_query[_query_name], _variables)
        _request_nodes = self._dump_nodes(_request, _query_name)
        if sla_domain_name and len(_request_nodes) == 1:
            return _request_nodes[0]['id']
        elif sla_domain_name and len(_request_nodes) > 1:
            for i in _request_nodes:
                if i['name'] == sla_domain_name:
                    return i['id']
        else:
            return _request_nodes
    except Exception as e:
        print(e)

def submit_on_demand(self, object_ids, sla_id, **kwargs):
    """Submits On Demand Snapshot

    Arguments:
        object_ids {[str]} -- Array of Rubrik Object IDs
        sla_id {str} -- Rubrik SLA Domain ID

    Returns:
        list -- List of errors if any occured
    """
    try:
        _mutation_name = "on_demand"
        _variables = {
            "objectIds": object_ids,
            "slaId": sla_id
        }
        _request = self._query(None, self._graphql_query[_mutation_name], _variables)
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

def submit_assign_sla(self, object_ids, sla_id):
    """Submits a Rubrik SLA change for objects

    Arguments:
        object_ids {[str]} -- Array of Rubrik Object IDs
        sla_id {str} -- Rubrik SLA Domain ID
    
    Returns:
        list -- List of objects assigned the SLA
    """
    try:
        _mutation_name = "assign_sla"
        _variables = {
                "objectIds": object_ids,
                "slaId": sla_id
            }
        request = self._query(None, self._graphql_query[_mutation_name], _variables)
        return  self._dump_nodes(request, _mutation_name)
    except Exception as e:
        print(e)

def get_task_status(self, task_chain_id):
    """Retrieve task status from Polaris

    Arguments:
        task_chain_id {str} -- Task Chain UUID from request

    Returns:
        str -- Task state
    """
    _query_name = "taskchain_status"
    try:
        _variables = {
            "filter": task_chain_id
        }
        _request = self._query(None, self._graphql_query[_query_name], _variables)
        _response = self._dump_nodes(_request, _query_name)
        return _response['taskchain']['state']
    except Exception as e:
        print(e)

def get_snapshots(self, snappable_id, **kwargs):
    """Retrieve Snapshots for a Snappable from Polaris

    Arguments:
        snappable_id {str} -- Object UUID
        recovery_point {str} -- Optional datetime of snapshot to return, or 'latest', or not defined to return all
        
    Returns:
        dict -- A dictionary of snapshots or a single snapshot if 'latest' was passed as `recovery_point`
    """
    from dateutil.parser import parse

    _query_name = "snappable_snapshots"
    try:
        _variables = {
            "snappable_id": snappable_id
        }
        if kwargs and 'recovery_point' in kwargs and kwargs['recovery_point'] == 'latest':
            _variables['first'] = 1
        _request = self._query(None, self._graphql_query[_query_name], _variables)
        _response = self._dump_nodes(_request, _query_name)
        if not len(_response):
            raise Exception("No Snapshots found for Snappable : {}".format(snappable_id))
        snapshot_comparison = {}
        for snapshot in _response:
            if kwargs and 'recovery_point' in kwargs and kwargs['recovery_point'] != 'latest':
                parsed_snapshot_date = parse(snapshot['date']).astimezone()
                parsed_recovery_point = parse(kwargs['recovery_point'])
                parsed_recovery_point = parsed_recovery_point.replace(tzinfo = tzlocal())
                snapshot['date_local'] = parsed_snapshot_date.isoformat()
                if parsed_snapshot_date >= parsed_recovery_point:
                    snapshot_comparison[abs(parsed_recovery_point - parsed_snapshot_date)] = snapshot
        if kwargs and 'recovery_point' in kwargs and kwargs['recovery_point'] != 'latest':
            return snapshot_comparison[min(snapshot_comparison)]
        if len(_response) == 1:
            return _response[0]
        else:
            return _response
    except Exception as e:
        print(e)

