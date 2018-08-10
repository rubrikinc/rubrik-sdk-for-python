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

"""
This module contains the Rubrik SDK Data_Management class.
"""

import sys
from .api import Api

_API = Api


class Data_Management(_API):
    """This class contains methods related to backup and restore operations for the various objects managed by the Rubrik Cluster.
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
            self.log("on_demand_snapshot: Searching the Rubrik Cluster for the vSphere VM '{}'.".format(object_name))
            vm_id = self.object_id(object_name, object_type)

            if sla_name is 'current':
                self.log(
                    "on_demand_snapshot: Searching the Rubrik Cluster for the SLA Domain assigned to the vSphere VM '{}'.".format(object_name))

                vm_summary_api_endpoint = '/vmware/vm/{}'.format(vm_id)
                vm_summary = self.get('v1', vm_summary_api_endpoint)

                sla_id = vm_summary['effectiveSlaDomainId']
            elif sla_name is not 'current':
                self.log("on_demand_snapshot: Searching the Rubrik Cluster for the SLA Domain '{}'.".format(sla_name))
                sla_id = self.object_id(sla_name, 'sla')

            snapshot_config = {}
            snapshot_config['slaId'] = sla_id

            self.log("on_demand_snapshot: Initiating snapshot for the vSphere VM '{}'.".format(object_name))
            vsphere_vm_snapshot_api_endpoint = '/vmware/vm/{}/snapshot'.format(vm_id)
            api_request = self.post('v1', vsphere_vm_snapshot_api_endpoint, snapshot_config)

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

        valid_object_type = ['vmware', 'sla', 'vmware_host']

        if object_type not in valid_object_type:
            sys.exit("Error: The object_id() object_type argument must be one of the following: {}.".format(valid_object_type))

        if object_type is 'vmware':
            object_summary_api_endpoint = '/vmware/vm?primary_cluster_id=local&is_relic=false&name={}'.format(
                object_name)
        elif object_type is 'sla':
            object_summary_api_endpoint = '/sla_domain?primary_cluster_id=local&name={}'.format(object_name)
        elif object_type is 'vmware_host':
            object_summary_api_endpoint = '/vmware/host?primary_cluster_id=local'

        self.log("object_id: Getting the object id for the {} object '{}'".format(object_type, object_name))
        api_request = self.get('v1', object_summary_api_endpoint)

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

    def assign_sla(self, object_name, sla_name, object_type=None):
        """Assign a Rubrik object to an SLA Domain.

        Arguments:
            object_name {str} -- The name of an object (ex. vSphere VM) you wish to assign to an SLA Domain.
            sla_name {str} -- The name of the SLA Domain you wish to assign an object to.

        Keyword Arguments:
            object_type {str} -- The type of object (ex. vmware) you are assigning to the SLA Domain. (default: {None}) (choices: {vmware})

        Returns:
            str -- If the object is already assigned to the SLA Domain a message to that effect will be retuned.
            dict -- The full API reponse of the SLA assignment API call.
        """

        valid_object_type = ['vmware']

        if object_type not in valid_object_type:
            sys.exit("Error: The assign_sla() object_type argument must be one of the following: {}.".format(valid_object_type))

        self.log("assign_sla: Searching the Rubrik Cluster for the SLA Domain '{}'.".format(sla_name))
        sla_id = self.object_id(sla_name, 'sla')

        if object_type is 'vmware':
            self.log("assign_sla: Searching the Rubrik Cluster for the vSphere VM '{}'.".format(object_name))
            vm_id = self.object_id(object_name, object_type)

            self.log("assign_sla: Determing the SLA Domain currently assigned to the vSphere VM '{}'.".format(object_name))
            vm_summary = self.get('v1', '/vmware/vm/{}'.format(vm_id))
            current_sla_id = vm_summary['effectiveSlaDomainId']

            if sla_id == current_sla_id:
                return "The vSphere VM '{}' is already assigned to the '{}' SLA Domain.".format(object_name, sla_name)
            else:
                self.log("assign_sla: Assigning the vSphere VM '{}' to the '{}' SLA Domain.".format(object_name, sla_name))
                config = {}
                config['configuredSlaDomainId'] = sla_id
                update_sla = self.patch('v1', '/vmware/vm/{}'.format(vm_id), config)
                return update_sla

    def live_mount_vsphere(self, vm_name, date='latest', time='latest', host='current', remove_network_devices=False, power_on=True):
        """Create a request to Instantly Recover a vSphere VM from a specified Snapshot. If a specific date and time is not provided the last Snapshot taken will be selected.

        Arguments:
            vm_name {str} -- The name of the VM to Instantly Recover.

        Keyword Arguments:
            date {str} -- The date of the Snapshot you wish to Instantly Recover formated as Month-Day-Year. Example: 1-15-2014. If latest is specified the last Snapshot taken will be Instantly Recovered. (default: {'latest'})
            time {str} -- The time of the Snapshot you wish to Instantly Recover formated formated as Hour:Minute AM/PM. Example: 1:30 AM. If latest is specified the last Snapshot taken will be Instantly Recovered. (default: {'latest'})
            host {str} -- The hostname or IP address of the ESXi host to Instantly Recover the VM on. By default the VM will be Instantly Recovered to the host it is currently on. (default: {'current'})
            remove_network_devices {bool} -- Determines whether to remove the network interfaces from the Instantly Recovered VM. Set to 'True' to remove all network interfaces. (default: {False})
            power_on {bool} -- Determines whether the VM should be powered on after Instantly Recover. Set to 'True' to power on the VM. Set to 'False' to mount the VM but not power it on. (default: {True})

        Returns:
            dict -- The full response of the Instantly Recover API call.
        """

        if isinstance(remove_network_devices, bool) is False:
            sys.exit("Error: The 'remove_network_devices' argument must be True or False.")
        elif isinstance(power_on, bool) is False:
            sys.exit("Error: The 'power_on' argument must be True or False.")
        elif date is not 'latest' and time is 'latest' or date is 'latest' and time is not 'latest':
            sys.exit("Error: The date and time arguments most both be 'latest' or a specific date and time.")

        self.log("live_mount_vsphere: Searching the Rubrik Cluster for the vSphere VM '{}'.".format(vm_name))
        vm_id = self.object_id(vm_name, 'vmware')

        self.log("live_mount_vsphere: Getting a list of all Snapshots for vSphere VM '{}'.".format(vm_name))
        vm_summary = self.get('v1', '/vmware/vm/{}'.format(vm_id))

        if date is 'latest' and time is 'latest':
            number_of_snapshots = len(vm_summary['snapshots'])
            snapshot_id = vm_summary['snapshots'][number_of_snapshots - 1]['id']
        else:

            self.log("live_mount_vsphere: Converting the provided date/time into UTC.")
            snapshot_date_time = self._date_time_conversion(date, time)

            current_snapshots = {}

            for snapshot in vm_summary['snapshots']:
                current_snapshots[snapshot['id']] = snapshot['date']

            self.log("live_mount_vsphere: Searching for the provided Snapshot.")
            for id, date_time in current_snapshots.items():
                if snapshot_date_time in date_time:
                    snapshot_id = id

        try:
            snapshot_id
        except NameError:
            sys.exit("Error: The vSphere VM '{}' does not have a Snapshot taken on {} at {}.".format(vm_name, date, time))
        else:
            if host is 'current':
                host_id = vm_summary['hostId']
            else:
                host_id = self.object_id(host, 'vmware_host')

            config = {}
            config['hostId'] = host_id
            config['removeNetworkDevices'] = remove_network_devices
            config['powerOn'] = power_on

            self.log("live_mount_vsphere: Instantly Recovering the Snapshot taken on {} at {} for vSphere VM '{}'.".format(
                date, time, vm_name))

            live_mount = self.post('v1', '/vmware/vm/snapshot/{}/mount'.format(snapshot_id), config)

            return live_mount

    def instant_recovery_vsphere(self, vm_name, date='latest', time='latest', host='current', remove_network_devices=False, power_on=True, disable_network=False, keep_mac_addresses=False, preserve_moid=False):
        """Instantly recovery a virtual machine from a snapshot. If a specific date and time is not provided the last Snapshot taken will be selected.

        Arguments:
            vm_name {str} -- The name of the VM to Instantly Recover.

        Keyword Arguments:
            date {str} -- The date of the Snapshot you wish to Instantly Recover formated as Month-Day-Year. Example: 1-15-2014. If 'latest' is specified the last Snapshot taken will be Instantly Recovered. (default: {'latest'})
            time {str} -- The time of the Snapshot you wish to Instantly Recover formated formated as Hour:Minute AM/PM. Example: 1:30 AM. If 'latest' is specified the last Snapshot taken will be Instantly Recovered. (default: {'latest'})
            host {str} -- The hostname or IP address of the ESXi host to Instantly Recover the VM on. By default the VM will be Instantly Recovered to the host it is currently on. (default: {'current'})
            remove_network_devices {bool} -- Determines whether to remove the network interfaces from the Instantly Recovered VM. Set to 'True' to remove all network interfaces. (default: {False})
            power_on {bool} -- Determines whether the VM should be powered on after Instant Recovery. Set to 'True' to power on the VM. Set to 'False' to mount the VM but not power it on. (default: {True})
            disable_network {bool} -- Sets the state of the network interfaces when the VM is mounted. Use 'False' to enable the network interfaces. Use 'True' to disable the network interfaces. Disabling the interfaces can prevent IP conflicts. (default: {False})
            keep_mac_addresses {bool} -- Determines whether the MAC addresses of the network interfaces on the source VM are assigned to the new VM. Set to 'True' to assign the original MAC addresses to the new VM. Set to 'False' to assign new MAC addresses. When 'remove_network_devices' is set to 'True', this property is ignored. (default: {False})
            preserve_moid {bool} -- Determines whether to preserve the MOID of the source VM in a restore operation. Use 'True' to keep the MOID of the source. Use 'False' to assign a new moid. (default: {False})

        Returns:
            dict -- The full response of the Instantly Recover API call.
        """

        if isinstance(remove_network_devices, bool) is False:
            sys.exit("Error: The 'remove_network_devices' argument must be True or False.")
        elif isinstance(power_on, bool) is False:
            sys.exit("Error: The 'power_on' argument must be True or False.")
        elif isinstance(disable_network, bool) is False:
            sys.exit("Error: The 'disable_network' argument must be True or False.")
        elif isinstance(keep_mac_addresses, bool) is False:
            sys.exit("Error: The 'keep_mac_addresses' argument must be True or False.")
        elif isinstance(preserve_moid, bool) is False:
            sys.exit("Error: The 'preserve_moid' argument must be True or False.")
        elif date is not 'latest' and time is 'latest' or date is 'latest' and time is not 'latest':
            sys.exit("Error: The date and time arguments most both be 'latest' or a specific date and time.")

        self.log("instant_recovery_vsphere: Searching the Rubrik Cluster for the vSphere VM '{}'.".format(vm_name))
        vm_id = self.object_id(vm_name, 'vmware')

        self.log("instant_recovery_vsphere: Getting a list of all Snapshots for vSphere VM '{}'.".format(vm_name))
        vm_summary = self.get('v1', '/vmware/vm/{}'.format(vm_id))

        if date is 'latest' and time is 'latest':
            number_of_snapshots = len(vm_summary['snapshots'])
            snapshot_id = vm_summary['snapshots'][number_of_snapshots - 1]['id']
        else:

            self.log("instant_recovery_vsphere: Converting the provided date/time into UTC.")
            snapshot_date_time = self._date_time_conversion(date, time)

            current_snapshots = {}

            for snapshot in vm_summary['snapshots']:
                current_snapshots[snapshot['id']] = snapshot['date']

            self.log("instant_recovery_vsphere: Searching for the provided Snapshot.")
            for id, date_time in current_snapshots.items():
                if snapshot_date_time in date_time:
                    snapshot_id = id

        try:
            snapshot_id
        except NameError:
            sys.exit("Error: The vSphere VM '{}' does not have a Snapshot taken on {} at {}.".format(vm_name, date, time))
        else:
            if host is 'current':
                host_id = vm_summary['hostId']
            else:
                host_id = self.object_id(host, 'vmware_host')

            config = {}
            config['hostId'] = host_id
            config['removeNetworkDevices'] = remove_network_devices
            config['powerOn'] = power_on
            config['disableNetwork'] = disable_network
            config['keepMacAddresses'] = keep_mac_addresses
            config['preserveMoid'] = preserve_moid

            self.log("instant_recovery_vsphere: Instantly Recovering the Snapshot taken on {} at {} for vSphere VM '{}'.".format(
                date, time, vm_name))

            instant_recovery = self.post('v1', '/vmware/vm/snapshot/{}/instant_recover'.format(snapshot_id), config)

            return instant_recovery

    def _date_time_conversion(self, date, time):
        """All date values returned by the Rubrik API are stored in Coordinated Universal Time (UTC) 
        and need to be converted to the timezone configured on the Rubrik Cluster in order to match 
        the values provided by the end user in various functions. This internal function will handle that
        conversion process.

        Arguments:
            date {str} -- A date value formated as Month-Day-Year. Example: 1/15/2014
            time {str} -- A time value formated as Hour:Minute AM/PM. Example: 1:30 AM

        Returns:
            str -- A combined date/time value formated as Year-Month-DayTHour:Minute. Where Hour:Minute is on the 24-hour clock. Example: 2014-1-15T01:30
        """

        from datetime import datetime
        import pytz

        # Validate the Date formating
        try:
            snapshot_date = datetime.strptime(date, '%m-%d-%Y')
        except ValueError:
            sys.exit("Error: The date argument '{}' must be formatd as 'Month-Date-Year'. Example: 8-9-2018.".format(date))

        # Validate the Time formating
        try:
            snapshot_time = datetime.strptime(time, '%I:%M %p')
        except ValueError:
            sys.exit("Error: The time argument '{}' must be formatd as 'Hour:Minute AM/PM' . Example: 2:57 AM.".format(time))

        self.log("_date_time_conversion: Getting the Rubrik Cluster timezone.")
        cluster_summary = self.get('v1', '/cluster/me')
        cluster_timezone = cluster_summary['timezone']['timezone']

        self.log("_date_time_conversion: Converting the provided time to the 24-hour clock.")
        snapshot_time_24_hour_clock = datetime.strftime(snapshot_time, "%H:%M")

        self.log("_date_time_conversion: Creating a combined date/time variable.")
        snapshot_datetime = datetime.strptime('{} {}'.format(date, snapshot_time_24_hour_clock), '%m-%d-%Y %H:%M')

        # Add Timezone to snapshot_datetime Variable
        timezone = pytz.timezone(cluster_timezone)
        snapshot_datetime = timezone.localize(snapshot_datetime)

        self.log("_date_time_conversion: Converting the time to UTC.\n")
        utc_timezone = pytz.UTC
        snapshot_datetime = snapshot_datetime.astimezone(utc_timezone)

        snapshot_datetime = snapshot_datetime.strftime('%Y-%m-%dT%H:%M')
        return snapshot_datetime
