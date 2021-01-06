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
Collection of functions that manipulate compute components
"""


def get_compute_object_ids_ec2(self, match_all=True, **kwargs):
    """Retrieves all AWS EC2 object IDs that match query

    Arguments:
        match_all {bool} -- Set to false to match ANY defined criteria
        tags {name: value} -- Allows simple qualification of tags
        kwargs {} -- Any top level object from the get_compute_ec2 call

    Returns:
        list -- List of all the EC2 object id's 
    """
    try:
        for instance in self.get_compute_ec2():
            object_ids = []
            num_criteria = len(kwargs)
            if 'tags' in kwargs:
                num_criteria = num_criteria + len(kwargs['tags']) - 1
            num_unmatched_criteria = num_criteria
            for key in kwargs:
                if key == 'tags' and 'tags' in instance:
                    for instance_tag in instance['tags']:
                        if instance_tag['key'] in kwargs['tags'] and \
                           instance_tag['value'] == kwargs['tags'][instance_tag['key']]:
                            num_unmatched_criteria -= 1
                elif key in instance and instance[key] == kwargs[key]:
                    num_unmatched_criteria -= 1
            if match_all and num_unmatched_criteria == 0:
                object_ids.append(instance['id'])
            elif not match_all and num_criteria > num_unmatched_criteria >= 1:
                object_ids.append(instance['id'])
        return object_ids
    except Exception:
        raise


def get_compute_object_ids_azure(self, match_all=True, **kwargs):
    """Retrieves all Azure VM object IDs that match query

    Arguments:
        match_all {bool} -- Set to false to match ANY defined criteria
        kwargs {} -- Any top level object from the get_compute_azure call
    
    Returns:
        list -- List of all the Azure VM object id's 
    """
    try:
        return self._get_compute_object_ids(self.get_compute_azure(), kwargs, match_all=match_all)
    except Exception:
        raise


def get_compute_object_ids_gce(self, match_all=True, **kwargs):
    """Retrieves all GCE object IDs that match query

    Arguments:
        match_all {bool} -- Set to `False` to match ANY defined criteria
        kwargs {} -- Any top level object from the get_compute_gce call
    
    Returns:
        list -- List of all the GCE object id's 
    """
    try:
        return self._get_compute_object_ids(self.get_compute_gce(), kwargs, match_all=match_all)
    except Exception:
        raise


def _get_compute_object_ids_vsphere(self, match_all=True, **kwargs):
    """Retrieves all vSphere objects that match query

    Arguments:
        match_all {bool} -- Set to false to match ANY defined criteria
        kwargs {} -- Any top level object from the get_compute_ec2 call
    """
    try:
        return self._get_object_ids_instances(self.get_instances_vsphere(), kwargs, match_all=match_all)
    except Exception:
        raise


def _get_compute_object_ids(self, instances, criterias, match_all=True):
    try:
        object_ids = []

        for instance in instances:
            num_criteria = len(criterias)
            num_unmatched_criteria = num_criteria

            for key in criterias:
                if key in instance and instance[key] == criterias[key]:
                    num_unmatched_criteria -= 1

            if match_all and num_unmatched_criteria == 0:
                object_ids.append(instance['id'])
            elif not match_all and num_criteria > num_unmatched_criteria >= 1:
                object_ids.append(instance['id'])

        return object_ids
    except Exception:
        raise


def get_compute_ec2(self, object_id=None):
    """Retrieve all AWS EC2 instances from Polaris
    
    Arguments:
        object_id {str} -- A specific Object ID to retrieve

    Returns:
        list -- List of all the AWS EC2 instances or the specific instance if the `object_id` is passed.
    """
    try:
        if object_id:
            query_name = "compute_aws_ec2_detail"
            variables = {
                "object_id": object_id
            }
            return self._query(query_name, variables)
        else:
            query_name = "compute_aws_ec2"
            return self._query(query_name, None)
    except Exception:
        raise

        
def get_compute_azure(self):
    """Retrieve all Azure instances from Polaris
    
    Returns:
        list -- List of all Azure VM instances
    """
    try:
        query_name = "compute_azure_iaas"
        return self._query(query_name, None)
    except Exception:
        raise


def get_compute_gce(self):
    """Retrieve all GCE instances from Polaris
        
    Returns:
        list -- List of all GCE instances
    """
    try:
        query_name = "compute_gcp_gce"
        return self._query(query_name, None)
    except Exception:
        raise


def _get_compute_vsphere(self):
    """ Retrieve all vSphere instances from Polaris """
    try:
        query_name = "compute_vmware_vsphere"
        variables = {"filter": []}
        return self._query(query_name, variables)
    except Exception:
        raise


def _submit_compute_restore(self, snapshot_id, **kwargs):
    """Submits a Restore of a compute instance

    Arguments:
        query_name {string} -- Backend query name for operation
        snapshot_id {string} -- Snapshot ID to be restored
        should_power_on {bool} -- Defaults to False
        should_restore_tags {bool} -- Defaults to False
        wait {bool} -- Return once complete Defaults to False
    """

    should_power_on = False
    if kwargs and 'should_power_on' in kwargs and kwargs['should_power_on']:
        should_power_on = True

    should_restore_tags = False
    if kwargs and 'should_restore_tags' in kwargs and kwargs['should_restore_tags']:
        should_restore_tags = True

    try:
        mutation_name = kwargs['mutation']
        variables = {
            "snapshot_id": snapshot_id,
            "should_power_on": should_power_on,
            "should_restore_tags": should_restore_tags
        }

        if mutation_name not in self._graphql_query:
            raise Exception("Mutation not found : {}".format(mutation_name))

        result = self._query(mutation_name, variables)
        if 'errors' in result and result['errors']:
            return {'errors': result['errors'][0]['message']}

        results = []
        if 'wait' in kwargs:
            results = self._monitor_task(result)

        return results
        # TODO: find a better way to report errors per uuid
    except Exception:
        raise


def submit_compute_restore_ec2(self, snapshot_id, **kwargs):
    """Submits a Restore of an EC2 instance

    Arguments:
        snapshot_id {str} -- Snapshot ID to be restored
        should_power_on {bool} -- Defaults to `False`
        should_restore_tags {bool} -- Defaults to `False`
        wait {bool} -- Return once complete Defaults to `False`
    
    Returns:
        list -- List of errors if any occurred during the restore
    """
    return self._submit_compute_restore(snapshot_id, mutation = "compute_restore_ec2", **kwargs)


def submit_compute_restore_azure(self, snapshot_id, **kwargs):
    """Submits a Restore of an Azure VM instance

    Arguments:
        snapshot_id {str} -- Snapshot ID to be restored
        should_power_on {bool} -- Defaults to `False`
        should_restore_tags {bool} -- Defaults to `False`
        wait {bool} -- Return once complete Defaults to `False`

    Returns:
        list -- List of errors if any occurred during the restore
    """
    return self._submit_compute_restore(snapshot_id, mutation = "compute_restore_azure", **kwargs)


def submit_compute_restore_gce(self, snapshot_id, **kwargs):
    """Submits a Restore of a GCE instance

    Arguments:
        snapshot_id {str} -- Snapshot ID to be restored
        should_power_on {bool} -- Defaults to `False`
        should_restore_tags {bool} -- Defaults to `False`
        wait {bool} -- Return once complete Defaults to `False`

    Returns:
        list -- List of errors if any occurred during the restore
    """
    return self._submit_compute_restore(snapshot_id, mutation = "compute_restore_gce", **kwargs)

