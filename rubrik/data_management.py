import sys


class Data_Management():
    """[summary]

    """

    def on_demand_snapshot(self, object_type, object_name, sla_name='current'):

        if object_type is 'vmware':

            vsphere_vm_summary_api_version = 'v1'
            vsphere_vm_summary_api_endpoint = '/vmware/vm?primary_cluster_id=local&is_relic=false&name={}'.format(
                object_name)

            self.log("On-Demand vSphere Snapshot: Searching the Rubrik Cluster for the VM '{}'.".format(object_name))
            api_request = self.get(vsphere_vm_summary_api_version, vsphere_vm_summary_api_endpoint)

            if api_request['total'] == 0:
                sys.exit("Error: The vSphere VM '{}' was not found on the Rubrik Cluster.".format(object_name))
            elif api_request['total'] > 0:
                vm_not_present = True
                for vm in api_request['data']:
                    if vm['name'] == object_name:
                        vm_not_present = False
                        vm_id = vm['id']
                        sla_id = vm['effectiveSlaDomainId']

            if vm_not_present:
                sys.exit("Error: The vSphere VM '{}' was not found on the Rubrik Cluster.".format(object_name))

            vsphere_vm_snapshot_api_version = 'v1'
            vsphere_vm_snapshot_api_endpoint = '/vmware/vm/{}/snapshot'.format(vm_id)

            if sla_name is not 'current':
                self.log("On-Demand vSphere Snapshot: Searching the Rubrik Cluster for the SLA Domain '{}'.".format(sla_name))
                sla_id = self.sla_domain_id(sla_name)

            snapshot_config = {}
            snapshot_config['slaId'] = sla_id

            self.log("On-Demand vSphere Snapshot: Initiating snapshot for the VM '{}'.".format(object_name))
            api_request = self.post(vsphere_vm_snapshot_api_version, vsphere_vm_snapshot_api_endpoint, snapshot_config)

            snapshot_status_url = api_request['links'][0]['href']

            ########### DO NOT MODIFY THESE VALUES - USED IN UNIT TESTS ONLY #########
            assert vsphere_vm_summary_api_version == 'v1'
            assert vsphere_vm_summary_api_endpoint == '/vmware/vm?primary_cluster_id=local&is_relic=false&name={}'.format(
                object_name)
            assert vsphere_vm_snapshot_api_version == 'v1'
            assert vsphere_vm_snapshot_api_endpoint == '/vmware/vm/{}/snapshot'.format(vm_id)
            ##########################################################################

        return (api_request, snapshot_status_url)

    def sla_domain_id(self, sla_name):
        """Get the ID of a provided SLA Domain

        Arguments:
            sla_name {str} -- The name of the SLA Domain you wish to get the ID of.

        Returns:
            str -- The ID of the provided the SLA Domain.
        """

        sla_summary_api_version = 'v1'
        sla_summary_api_endpoint = '/sla_domain?primary_cluster_id=local&name={}'.format(sla_name)

        api_request = self.get(sla_summary_api_version, sla_summary_api_endpoint)

        if api_request['total'] == 0:
            sys.exit("Error: The SLA Domain '{}' was not found on the Rubrik Cluster.".format(sla_name))
        elif api_request['total'] > 0:
            sla_not_present = True
            for sla in api_request['data']:
                if sla['name'] == sla_name:
                    sla_not_present = False
                    sla_id = sla['id']
                    return sla_id

        if sla_not_present:
            sys.exit("Error: The SLA Domain '{}' was not found on the Rubrik Cluster.".format(sla_name))
