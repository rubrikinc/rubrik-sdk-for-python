""" Collection of functions that manipulate storage components"""

def get_object_ids_ebs(self, match_all=True, **kwargs):
    """Retrieves all AWS EBS object IDs that match query

    Arguments:
        match_all {bool} -- Set to false to match ANY defined criteria
        tags {name: value} -- Allows simple qualification of tags
        kwargs {} -- Any top level object from the get_storage_ebs call

    Returns:
        list -- List of all the EBS object id's
    """
    try:
        _o = []
        for _instance in self.get_storage_ebs():
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


def get_storage_ebs(self):
    """Retrieve all AWS EC2 instances from Polaris

    Returns:
        list -- List of all the AWS EBS volumes.
    """
    try:
        _query_name = "storage_aws_ebs"
        _request = self._query(_query_name, None)
        return self._dump_nodes(_request, _query_name)
    except Exception as e:
        print(e)

