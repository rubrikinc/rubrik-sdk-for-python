# Copyright 2018 Rubrik, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License prop
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from .api import Api

_API = Api


class Data_Management(_API):
    """[summary]

    """

    def on_demand_snapshot(self, object_name, object_type=None, sla_name='current'):
        """Initiate an on-demand snapshot.

        Arguments:
            object_name {str} -- The name of object (i.e vSphere VM, Fileset, etc.) to take a Snapshot of.

        Keyword Arguments:
            object_type {str} -- The Rubrik object type you wish to backup. vmware is currently the only supported option. (default: {None})
            sla_name {str} -- The SLA Domain name you to assign the snapshot to. By default the currently assigne SLA Domain will be used. (default: {'current'})

        Returns:
            tuple -- The full API response and the job status URL which can be used to monitor progress of the Snapshot. (api_response, job_status_url)
        """

        valid_object_type = ['vmware']

        if object_type not in valid_object_type:
            sys.exit("Error: The on_demand_snapshot() object_type argument must be one of the following: {}.".format(valid_object_type))

        if object_type is 'vmware':
            self.log("On-Demand vSphere Snapshot: Searching the Rubrik Cluster for the VM '{}'.".format(object_name))
            vm_id = self.object_id(object_name, object_type)

            if sla_name is 'current':
                self.log(
                    "On-Demand vSphere Snapshot: Searching the Rubrik Cluster for the SLA Domain assigned to the VM '{}'.".format(object_name))

                vm_summary_api_version = 'v1'
                vm_summary_api_endpoint = '/vmware/vm/{}'.format(vm_id)
                vm_summary = self.get(vm_summary_api_version, vm_summary_api_endpoint)

                sla_id = vm_summary['effectiveSlaDomainId']
            elif sla_name is not 'current':
                self.log("On-Demand vSphere Snapshot: Searching the Rubrik Cluster for the SLA Domain '{}'.".format(sla_name))
                sla_id = self.object_id(sla_name, 'sla')

            snapshot_config = {}
            snapshot_config['slaId'] = sla_id

            self.log("On-Demand vSphere Snapshot: Initiating snapshot for the VM '{}'.".format(object_name))
            vsphere_vm_snapshot_api_version = 'v1'
            vsphere_vm_snapshot_api_endpoint = '/vmware/vm/{}/snapshot'.format(vm_id)
            api_request = self.post(vsphere_vm_snapshot_api_version, vsphere_vm_snapshot_api_endpoint, snapshot_config)

            snapshot_status_url = api_request['links'][0]['href']

        return (api_request, snapshot_status_url)

    def object_id(self, object_name, object_type=None):
        """Get the ID of a provided object (ex. VM, SLA, etc.) by providing its name.

        Arguments:
            object_name {str} -- The name of the object whose ID you wish to lookup.

        Keyword Arguments:
            object_type {str} -- The object type you wish to look up. Valid options are vmware and sla. (default: {None})

        Returns:
            [str] -- The ID of the provided object.
        """

        object_summary_api_version = 'v1'

        if object_type is 'vmware':
            object_summary_api_endpoint = '/vmware/vm?primary_cluster_id=local&is_relic=false&name={}'.format(
                object_name)
        elif object_type is 'sla':
            object_summary_api_endpoint = '/sla_domain?primary_cluster_id=local&name={}'.format(object_name)

        api_request = self.get(object_summary_api_version, object_summary_api_endpoint)

        if api_request['total'] == 0:
            sys.exit("Error: The {} object '{}' was not found on the Rubrik Cluster.".format(object_type, object_name))
        elif api_request['total'] > 0:
            object_type_present = True
            for item in api_request['data']:
                if item['name'] == object_name:
                    object_type = False
                    object_id = item['id']
                    return object_id

        if object_type_present:
            sys.exit("Error: The {} object '{}' was not found on the Rubrik Cluster.".format(object_type, object_name))
