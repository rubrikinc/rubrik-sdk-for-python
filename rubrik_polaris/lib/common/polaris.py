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


"""
Collection of methods that interact with Polaris primitives.
"""


def get_sla_domains(self, sla_domain_name=""):
    """Retrieves dictionary of SLA Domain Names and Identifiers, or the ID of a single SLA Domain

    Arguments:
        sla_domain_name {str} -- Rubrik SLA Domain name

    Returns:
        str -- ID for the given SLA Domain name as given by `sla_domain_name`
        dict -- If a `sla_domain_name` is not given or not found, the complete set of SLA domains will be returned
    """
    from rubrik_polaris.exceptions import RequestException

    try:
        query_name = "sla_domains"
        variables = {
            "filter": {
                "field": "NAME",
                "text": sla_domain_name
            }
        }
        request = self._query(None, self._graphql_query[query_name], variables)
        request_nodes = self._dump_nodes(request)

        return request_nodes
    except Exception:
        raise


def submit_on_demand(self, object_ids, sla_id, **kwargs):
    """Submits On Demand Snapshot

    Arguments:
        object_ids {[str]} -- Array of Rubrik Object IDs
        sla_id {str} -- Rubrik SLA Domain ID

    Returns:
        list -- List of errors if any occurred
    """
    from rubrik_polaris.exceptions import RequestException

    try:
        mutation_name = "on_demand"
        variables = {
            "objectIds": object_ids,
            "slaId": sla_id
        }
        request = self._query(None, self._graphql_query[mutation_name], variables)
        result = self._dump_nodes(request)

        results = []

        if result['errors']:
            for error_object in result['errors']:
                results.append(error_object)

        if 'wait' in kwargs:
            results = self._monitor_task(result['taskchainUuids'])

        # TODO: find a better way to report errors per uuid

        return results
    except Exception:
        raise


def submit_assign_sla(self, object_ids, sla_id):
    """Submits a Rubrik SLA change for objects

    Arguments:
        object_ids {[str]} -- Array of Rubrik Object IDs
        sla_id {str} -- Rubrik SLA Domain ID
    
    Returns:
        list -- List of objects assigned the SLA
    """
    from rubrik_polaris.exceptions import RequestException

    try:
        mutation_name = "assign_sla"
        variables = {
            "objectIds": object_ids,
            "slaId": sla_id
        }
        request = self._query(None, self._graphql_query[mutation_name], variables)
        return self._dump_nodes(request)
    except Exception:
        raise


def get_task_status(self, task_chain_id):
    """Retrieve task status from Polaris

    Arguments:
        task_chain_id {str} -- Task Chain UUID from request

    Returns:
        str -- Task state
    """
    from rubrik_polaris.exceptions import RequestException

    try:
        query_name = "taskchain_status"
        variables = {
            "filter": task_chain_id
        }
        request = self._query(None, self._graphql_query[query_name], variables)
        response = self._dump_nodes(request)

        return response['taskchain']['state']
    except Exception:
        raise


def get_snapshots(self, snappable_id, **kwargs):
    """Retrieve Snapshots for a Snappable from Polaris

    Arguments:
        snappable_id {str} -- Object UUID
        recovery_point {str} -- Optional datetime of snapshot to return, or 'latest', or not defined to return all
        
    Returns:
        dict -- A dictionary of snapshots or a single snapshot if 'latest' was passed as `recovery_point`. If no snapshots are found, an empty dict is returned.
    """
    from dateutil.parser import parse
    from dateutil.tz import tzlocal

    try:
        query_name = "snappable_snapshots"
        variables = {
            "snappable_id": snappable_id
        }
        if kwargs and 'recovery_point' in kwargs and kwargs['recovery_point'] == 'latest':
            variables['first'] = 1

        request = self._query(None, self._graphql_query[query_name], variables)
        response = self._dump_nodes(request)

        if len(response) == 0:
            return {}

        snapshot_comparison = {}
        for snapshot in response:
            if kwargs and 'recovery_point' in kwargs and kwargs['recovery_point'] != 'latest':
                parsed_snapshot_date = parse(snapshot['date']).astimezone()
                parsed_recovery_point = parse(kwargs['recovery_point'])
                parsed_recovery_point = parsed_recovery_point.replace(tzinfo=tzlocal())
                snapshot['date_local'] = parsed_snapshot_date.isoformat()
                if parsed_snapshot_date >= parsed_recovery_point:
                    snapshot_comparison[abs(parsed_recovery_point - parsed_snapshot_date)] = snapshot

        if kwargs and 'recovery_point' in kwargs and kwargs['recovery_point'] != 'latest':
            return snapshot_comparison[min(snapshot_comparison)]

        return response
    except Exception:
        raise
