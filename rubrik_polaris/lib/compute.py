""" Collection of functions that manipulate compute components"""

def get_object_ids_ec2(self, match_all=True, **kwargs):
    """Retrieves all EC2 objects that match query

    Arguments:
        match_all bool -- Set to false to match ANY defined criteria
        kwargs -- Any top level object from the get_instances_ec2 call
    """
    try:
        _o = []
        for _instance in self.get_instances_ec2():
            _t = len(kwargs)
            if 'tags' in kwargs:
                _t = _t + len(kwargs['tags']) - 1
            _c = _t
            for _key in kwargs:
                if _key == 'tags' and 'tags' in _instance:
                    for _instance_tag in _instance['tags']:
                        if _instance_tag['key'] in kwargs['tags'] and _instance_tag['value'] == kwargs['tags'][
                            _instance_tag['key']]:
                            _c -= 1
                elif _key in _instance and _instance[_key] == kwargs[_key]:
                    _c -= 1
            if match_all and not bool(_c):
                _o.append(_instance['id'])
            elif not match_all and _c < _t and bool(_c):
                _o.append(_instance['id'])
        return _o
    except Exception as e:
        print(e)


def get_object_ids_azure(self, match_all=True, **kwargs):
    """Retrieves all Azure objects that match query

    Arguments:
        match_all bool -- Set to false to match ANY defined criteria
        kwargs -- Any top level object from the get_instances_ec2 call
    """
    try:
        _o = []
        for _instance in self.get_instances_azure():
            _t = len(kwargs)
            _c = _t
            for _key in kwargs:
                if _key in _instance and _instance[_key] == kwargs[_key]:
                    _c -= 1
            if match_all and not bool(_c):
                _o.append(_instance['id'])
            elif not match_all and _c < _t and bool(_c):
                _o.append(_instance['id'])
        return _o
    except Exception as e:
        print (e)


def get_object_ids_gce(self, match_all=True, **kwargs):
    """Retrieves all Azure objects that match query

    Arguments:
        match_all bool -- Set to false to match ANY defined criteria
        kwargs -- Any top level object from the get_instances_ec2 call
    """
    try:
        _o = []
        for _instance in self.get_instances_gce():
            _t = len(kwargs)
            _c = _t
            for _key in kwargs:
                if _key in _instance and _instance[_key] == kwargs[_key]:
                    _c -= 1
            if match_all and not bool(_c):
                _o.append(_instance['id'])
            elif not match_all and _c < _t and bool(_c):
                _o.append(_instance['id'])
        return _o
    except Exception as e:
        print(e)


def get_instances_ec2(self, object_id = None):
    ### Retrieve all EC2 instances from Polaris ###
    #todo: make the changes to call specific instances for gce/azure
    try:
        _request = None
        if object_id:
            _query_name = "instances_ec2_detail"
            variables = {
                "object_id": object_id
            }
            _request = self._query(None, self._graphql_query[_query_name], variables)
        else:
            _query_name = "instances_ec2"
            _request = self._query(None, self._graphql_query[_query_name], None)
        return self._dump_nodes(_request, _query_name)
    except Exception as e:
        print(e)

def get_instances_azure(self):
    ### Retrieve all Azure instances from Polaris ###
    try:
        _query_name = "instances_azure"
        _request = self._query(None, self._graphql_query[_query_name], None)
        return self._dump_nodes(_request, _query_name)
    except Exception as e:
        print(e)


def get_instances_gce(self):
    ### Retrieve all GCE instances from Polaris ###
    try:
        _query_name = "instances_gce"
        _request = self._query(None, self._graphql_query[_query_name], None)
        return self._dump_nodes(_request, _query_name)
    except Exception as e:
        print(e)


def _submit_instance_restore(self, snapshot_id, **kwargs):
    """Submits a Restore of a compute instance

    Arguments:
        query_name [string] -- Backend query name for operation
        snapshot_id [string] -- Snapshot ID to be restored
        should_power_on bool -- Defaults to False
        should_restore_tags bool -- Defaults to False
        wait bool -- Return once complete Defaults to False
    """

    should_power_on = False
    if kwargs and 'should_power_on' in kwargs and kwargs['should_power_on']:
        should_power_on = True
    should_restore_tags = False
    if kwargs and 'should_restore_tags' in kwargs and kwargs['should_restore_tags']:
        should_power_on = True
    try:
        _mutation_name = kwargs['mutation']
        _variables = {
            "snapshot_id": snapshot_id,
            "should_power_on": kwargs['should_power_on'],
            "should_restore_tags": kwargs['should_restore_tags']
        }
        if _mutation_name not in self._graphql_query:
            raise Exception("Mutation not found : {}".format(_mutation_name))
        _request = self._query(None, self._graphql_query[_mutation_name], _variables)
        if 'errors' in _request and _request['errors']:
            return  {'errors': _request['errors'][0]['message']}
        _result = self._dump_nodes(_request, _mutation_name)
        _results = []
        if 'wait' in kwargs:
            _results = self._monitor_task(_result)
        return _results
        #todo: find a better way to report errors per uuid
    except Exception as e:
        print(e)

def submit_restore_ec2(self, snapshot_id, **kwargs):
    """Submits a Restore of an EC2 instance

    Arguments:
        snapshot_id [string] -- Snapshot ID to be restored
        should_power_on bool -- Defaults to False
        should_restore_tags bool -- Defaults to False
        wait bool -- Return once complete Defaults to False
    """
    return self._submit_instance_restore(snapshot_id, mutation = "instances_restore_ec2", **kwargs)

def submit_restore_azure(self, snapshot_id, **kwargs):
    """Submits a Restore of an Azure instance

    Arguments:
        snapshot_id [string] -- Snapshot ID to be restored
        should_power_on bool -- Defaults to False
        should_restore_tags bool -- Defaults to False
        wait bool -- Return once complete Defaults to False
    """
    return self._submit_instance_restore(snapshot_id, mutation = "instances_restore_azure", **kwargs)

def submit_restore_gce(self, snapshot_id, **kwargs):
    """Submits a Restore of a GCE instance

    Arguments:
        snapshot_id [string] -- Snapshot ID to be restored
        should_power_on bool -- Defaults to False
        should_restore_tags bool -- Defaults to False
        wait bool -- Return once complete Defaults to False
    """
    return self._submit_instance_restore(snapshot_id, mutation = "instances_restore_gce", **kwargs)
