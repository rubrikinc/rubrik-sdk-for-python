""" Collection of functions that manipulate compute components"""

def get_object_ids_ec2(self, match_all=True, **kwargs):
    """Retrieves all EC2 objects that match query

    Arguments:
        match_all bool -- Set to false to match ANY defined criteria
        kwargs -- Any top level object from the get_instances_ec2 call
    """
    o = []
    for instance in self.get_instances_ec2():
        t = len(kwargs)
        if 'tags' in kwargs:
            t = t + len(kwargs['tags']) - 1
        c = t
        for key in kwargs:
            if key == 'tags' and 'tags' in instance:
                for instance_tag in instance['tags']:
                    if instance_tag['key'] in kwargs['tags'] and instance_tag['value'] == kwargs['tags'][
                        instance_tag['key']]:
                        c -= 1
            elif key in instance and instance[key] == kwargs[key]:
                c -= 1
        if match_all and not bool(c):
            o.append(instance['id'])
        elif not match_all and c < t and bool(c):
            o.append(instance['id'])
    return o


def get_object_ids_azure(self, match_all=True, **kwargs):
    """Retrieves all Azure objects that match query

    Arguments:
        match_all bool -- Set to false to match ANY defined criteria
        kwargs -- Any top level object from the get_instances_ec2 call
    """
    o = []
    for instance in self.get_instances_azure():
        t = len(kwargs)
        c = t
        for key in kwargs:
            if key in instance and instance[key] == kwargs[key]:
                c -= 1
        if match_all and not bool(c):
            o.append(instance['id'])
        elif not match_all and c < t and bool(c):
            o.append(instance['id'])
    return o


def get_object_ids_gce(self, match_all=True, **kwargs):
    """Retrieves all Azure objects that match query

    Arguments:
        match_all bool -- Set to false to match ANY defined criteria
        kwargs -- Any top level object from the get_instances_ec2 call
    """
    o = []
    for instance in self.get_instances_gce():
        t = len(kwargs)
        c = t
        for key in kwargs:
            if key in instance and instance[key] == kwargs[key]:
                c -= 1
        if match_all and not bool(c):
            o.append(instance['id'])
        elif not match_all and c < t and bool(c):
            o.append(instance['id'])
    return o


def get_instances_ec2(self):
    query_name = "instances_ec2"
    request = self.query(None, self.graphql_query[query_name], None)
    return self._dump_nodes(request, query_name)


def get_instances_azure(self):
    query_name = "instances_azure"
    request = self.query(None, self.graphql_query[query_name], None)
    return self._dump_nodes(request, query_name)


def get_instances_gce(self):
    query_name = "instances_gce"
    request = self.query(None, self.graphql_query[query_name], None)
    return self._dump_nodes(request, query_name)