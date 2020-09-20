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


def get_instances_ec2(self):
    ### Retrieve all EC2 instances from Polaris ###
    try:
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
