# Copyright 2018 Rubrik, Inc.
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
This module contains the Rubrik SDK Data_Management class.
"""
import re
from .api import Api
from .exceptions import CDMVersionException, InvalidParameterException, InvalidTypeException


_API = Api


class Data_Management(_API):
    """This class contains methods related to backup and restore operations for the various objects managed by the Rubrik cluster."""

    def on_demand_snapshot(self, object_name, object_type, sla_name='current', fileset=None, host_os=None, sql_host=None, sql_instance=None, sql_db=None, timeout=15):  # pylint: ignore
        """Initiate an on-demand snapshot.

        Arguments:
            object_name {str} -- The name of the Rubrik object to take a on-demand snapshot of.
            object_type {str} -- The Rubrik object type you want to backup. (choices: {vmware, physical_host, ahv, mssql})

        Keyword Arguments:
            sla_name {str} -- The SLA Domain name you want to assign the on-demand snapshot to. By default, the currently assigned SLA Domain will be used. (default: {'current'})
            fileset {str} -- The name of the Fileset you wish to backup. Only required when taking a on-demand snapshot of a physical host. (default: {'None'})
            host_os {str} -- The operating system for the physical host. Only required when taking a on-demand snapshot of a physical host. (default: {'None'}) (choices: {Linux, Windows})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            tuple -- When object_type is vmware, the full API response for `POST /v1/vmware/vm/{ID}/snapshot` and the job status URL which can be used to monitor progress of the snapshot. (api_response, job_status_url)
            tuple -- When object_type is physical_host, the full API response for `POST /v1/fileset/{}/snapshot` and the job status URL which can be used to monitor progress of the snapshot. (api_response, job_status_url)

        """

        valid_object_type = ['vmware', 'physical_host', 'ahv', 'mssql_db']
        valid_host_os_type = ['Linux', 'Windows']

        if object_type not in valid_object_type:
            raise InvalidParameterException("The on_demand_snapshot() `object_type` argument must be one of the following: {}.".format(
                valid_object_type))

        if host_os is not None:
            if host_os not in valid_host_os_type:
                raise InvalidParameterException("The on_demand_snapshot() `host_os` argument must be one of the following: {}.".format(
                    valid_host_os_type))

        if object_type == 'vmware':
            self.log("on_demand_snapshot: Searching the Rubrik cluster for the vSphere VM '{}'.".format(object_name))
            vm_id = self.object_id(object_name, object_type, timeout=timeout)

            if sla_name == 'current':
                self.log(
                    "on_demand_snapshot: Searching the Rubrik cluster for the SLA Domain assigned to the vSphere VM '{}'.".format(object_name))

                vm_summary = self.get('v1', '/vmware/vm/{}'.format(vm_id), timeout=timeout)
                sla_id = vm_summary['effectiveSlaDomainId']

            elif sla_name != 'current':
                self.log("on_demand_snapshot: Searching the Rubrik cluster for the SLA Domain '{}'.".format(sla_name))
                sla_id = self.object_id(sla_name, 'sla', timeout=timeout)

            config = {}
            config['slaId'] = sla_id

            self.log("on_demand_snapshot: Initiating snapshot for the vSphere VM '{}'.".format(object_name))
            api_request = self.post('v1', '/vmware/vm/{}/snapshot'.format(vm_id), config, timeout)

            snapshot_status_url = api_request['links'][0]['href']

        elif object_type == 'ahv':

            self.log("on_demand_snapshot: Searching the Rubrik cluster for the AHV VM '{}'.".format(object_name))

            vm_id = self.object_id(object_name, object_type, timeout=timeout)

            if sla_name == 'current':
                self.log(
                    "on_demand_snapshot: Searching the Rubrik cluster for the SLA Domain assigned to the AHV VM '{}'.".format(object_name))

                vm_summary = self.get('internal', '/nutanix/vm/{}'.format(vm_id), timeout)
                sla_id = vm_summary['effectiveSlaDomainId']

            elif sla_name != 'current':
                self.log("on_demand_snapshot: Searching the Rubrik cluster for the SLA Domain '{}'.".format(sla_name))
                sla_id = self.object_id(sla_name, 'sla', timeout=timeout)

            config = {}
            config['slaId'] = sla_id

            self.log("on_demand_snapshot: Initiating snapshot for the AHV VM '{}'.".format(object_name))
            api_request = self.post('internal', '/nutanix/vm/{}/snapshot'.format(vm_id), config, timeout)

            snapshot_status_url = api_request['links'][0]['href']

        elif object_type == 'mssql_db':

            self.log(
                "on_demand_snapshot: Searching the Rubrik cluster for the MS SQL '{}'.".format(object_name))

            mssql_host = self.object_id(sql_host, 'physical_host', timeout=timeout)

            mssql_instance = self.get(
                'v1', '/mssql/instance?primary_cluster_id=local&root_id={}'.format(mssql_host), timeout)

            for instance in mssql_instance['data']:
                if instance['name'] == sql_instance:
                    sql_db_id = instance['id']

            mssql_db = self.get('v1', '/mssql/db?primary_cluster_id=local&instance_id={}'.format(sql_db_id), timeout)

            for db in mssql_db['data']:
                if db['name'] == sql_db:
                    mssql_id = db['id']

            if sla_name == 'current':
                self.log(
                    "on_demand_snapshot: Searching the Rubrik cluster for the SLA Domain assigned to the MS SQL '{}'.".format(object_name))

                mssql_summary = self.get('v1', '/mssql/db/{}'.format(mssql_id), timeout)
                sla_id = mssql_summary['effectiveSlaDomainId']

            elif sla_name != 'current':
                self.log("on_demand_snapshot: Searching the Rubrik cluster for the SLA Domain '{}'.".format(sla_name))
                sla_id = self.object_id(sla_name, 'sla', timeout=timeout)

            config = {}
            config['slaId'] = sla_id

            self.log(
                "on_demand_snapshot: Initiating snapshot for the MS SQL '{}'.".format(object_name))
            api_request = self.post('v1', '/mssql/db/{}/snapshot'.format(mssql_id), config, timeout)

            snapshot_status_url = api_request['links'][0]['href']

        elif object_type == 'mssql_db':

            self.log(
                "on_demand_snapshot: Searching the Rubrik cluster for the MS SQL '{}'.".format(object_name))

            mssql_host = self.object_id(sql_host, 'physical_host', timeout=timeout)
            mssql_instance = self.get(
                'v1', '/mssql/instance?primary_cluster_id=local&root_id={}'.format(mssql_host), timeout)

            for instance in mssql_instance['data']:
                if instance['name'] == sql_instance:
                    sql_db_id = instance['id']

            mssql_db = self.get('v1', '/mssql/db?primary_cluster_id=local&instance_id={}'.format(sql_db_id), timeout)

            for db in mssql_db['data']:
                if db['name'] == sql_db:
                    mssql_id = db['id']

            if sla_name == 'current':
                self.log(
                    "on_demand_snapshot: Searching the Rubrik cluster for the SLA Domain assigned to the MS SQL '{}'.".format(object_name))

                mssql_summary = self.get(
                    'v1', '/mssql/db/{}'.format(mssql_id), timeout)
                sla_id = mssql_summary['effectiveSlaDomainId']

            elif sla_name != 'current':
                self.log(
                    "on_demand_snapshot: Searching the Rubrik cluster for the SLA Domain '{}'.".format(sla_name))
                sla_id = self.object_id(sla_name, 'sla', timeout=timeout)

            config = {}
            config['slaId'] = sla_id

            self.log(
                "on_demand_snapshot: Initiating snapshot for the MS SQL '{}'.".format(object_name))
            api_request = self.post(
                'v1', '/mssql/db/{}/snapshot'.format(mssql_id), config, timeout)

            snapshot_status_url = api_request['links'][0]['href']

        elif object_type == 'physical_host':
            if host_os is None:
                raise InvalidParameterException(
                    "The on_demand_snapshot() `host_os` argument must be populated when taking a Physical host snapshot.")
            elif fileset is None:
                raise InvalidParameterException(
                    "The on_demand_snapshot() `fileset` argument must be populated when taking a Physical host snapshot.")

            self.log("on_demand_snapshot: Searching the Rubrik cluster for the Physical Host '{}'.".format(object_name))
            host_id = self.object_id(object_name, object_type, timeout=timeout)

            self.log("on_demand_snapshot: Searching the Rubrik cluster for the Fileset Template '{}'.".format(fileset))
            fileset_template_id = self.object_id(fileset, 'fileset_template', host_os, timeout=timeout)

            self.log("on_demand_snapshot: Searching the Rubrik cluster for the full Fileset.")
            api_endpoint = '/fileset?primary_cluster_id=local&host_id={}&is_relic=false&template_id={}'.format(
                host_id, fileset_template_id)
            fileset_summary = self.get('v1', api_endpoint, timeout=timeout)

            if fileset_summary['total'] == 0:
                raise InvalidParameterException(
                    "The Physical Host '{}' is not assigned to the '{}' Fileset.".format(
                        object_name, fileset))

            fileset_id = fileset_summary['data'][0]['id']

            if sla_name == 'current':
                sla_id = fileset_summary['data'][0]['effectiveSlaDomainId']
            elif sla_name != 'current':
                self.log("on_demand_snapshot: Searching the Rubrik cluster for the SLA Domain '{}'.".format(sla_name))
                sla_id = self.object_id(sla_name, 'sla', timeout=timeout)

            config = {}
            config['slaId'] = sla_id

            self.log("on_demand_snapshot: Initiating snapshot for the Physical Host '{}'.".format(object_name))
            api_request = self.post('v1', '/fileset/{}/snapshot'.format(fileset_id), config, timeout)

            snapshot_status_url = api_request['links'][0]['href']

        return (api_request, snapshot_status_url)

    def object_id(self, object_name, object_type, host_os=None, timeout=15):
        """Get the ID of a Rubrik object by providing its name.

        Arguments:
            object_name {str} -- The name of the Rubrik object whose ID you wish to lookup.
            object_type {str} -- The object type you wish to look up. (choices: {vmware, sla, vmware_host, physical_host, fileset_template, managed_volume, aws_native, vcenter})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            str -- The ID of the provided Rubrik object.
        """

        valid_object_type = [
            'vmware',
            'sla',
            'vmware_host',
            'physical_host',
            'fileset_template',
            'managed_volume',
            'mssql_db',
            'mssql_instance',
            'vcenter',
            'ahv',
            'aws_native']

        if object_type not in valid_object_type:
            raise InvalidParameterException("The object_id() object_type argument must be one of the following: {}.".format(
                valid_object_type))

        if object_type == 'fileset_template':
            if host_os is None:
                raise InvalidParameterException("You must provide the Fileset Tempalte OS type.")
            elif host_os not in ['Linux', 'Windows']:
                raise InvalidParameterException("The host_os must be either 'Linux' or 'Windows'.")

        if object_type == 'sla':
            if object_name.upper() == "FOREVER" or object_name.upper() == "UNPROTECTED":
                return "UNPROTECTED"

        api_call = {
            "vmware": {
                "api_version": "v1",
                "api_endpoint": "/vmware/vm?primary_cluster_id=local&is_relic=false&name={}".format(object_name)
            },
            "sla": {
                "api_version": "v1",
                "api_endpoint": "/sla_domain?primary_cluster_id=local&name={}".format(object_name)
            },
            "vmware_host": {
                "api_version": "v1",
                "api_endpoint": "/vmware/host?primary_cluster_id=local"
            },
            "fileset_template": {
                "api_version": "v1",
                "api_endpoint": "/fileset_template?primary_cluster_id=local&operating_system_type={}&name={}".format(host_os, object_name)
            },
            "managed_volume": {
                "api_version": "internal",
                "api_endpoint": "/managed_volume?is_relic=false&primary_cluster_id=local&name={}".format(object_name)
            },
            "ahv": {
                "api_version": "internal",
                "api_endpoint": "/nutanix/vm?primary_cluster_id=local&is_relic=false&name={}".format(object_name)
            },
            "mssql_db": {
                "api_version": "v1",
                "api_endpoint": "/mssql/db?primary_cluster_id=local&is_relic=false&instance_id={}".format(object_name)
            },
            "mssql_instance": {
                "api_version": "v1",
                "api_endpoint": "/mssql/instance?primary_cluster_id=local&root_id={}".format(object_name)
            },
            "aws_native": {
                "api_version": "internal",
                "api_endpoint": "/aws/account?name={}".format(object_name)
            },
            "vcenter": {
                "api_version": "v1",
                "api_endpoint": "/vmware/vcenter"
            }
        }

        if object_type == 'physical_host':
            if self.minimum_installed_cdm_version(5.0, timeout) is True:
                filter_field_name = "name"
            else:
                filter_field_name = "hostname"

            api_call["physical_host"] = {
                "api_version": "v1",
                "api_endpoint": "/host?primary_cluster_id=local&{}={}".format(filter_field_name, object_name)
            }

        self.log("object_id: Getting the object id for the {} object '{}'.".format(object_type, object_name))
        api_request = self.get(
            api_call[object_type]["api_version"],
            api_call[object_type]["api_endpoint"],
            timeout=timeout)

        if api_request['total'] == 0:
            raise InvalidParameterException("The {} object '{}' was not found on the Rubrik cluster.".format(
                object_type, object_name))
        elif api_request['total'] > 0:
            object_ids = []
            # Define the "object name" to search for
            if object_type == 'physical_host':
                name_value = filter_field_name
            else:
                name_value = 'name'

            for item in api_request['data']:
                if item[name_value] == object_name:
                    object_ids.append(item['id'])

            if len(object_ids) > 1:
                raise InvalidParameterException(
                    "Multiple {} objects named '{}' were found on the Rubrik cluster. Unable to return a specific object id.".format(object_type, object_name))
            elif len(object_ids) == 0:
                raise InvalidParameterException(
                    "The {} object '{}' was not found on the Rubrik cluster.".format(object_type, object_name))
            else:
                return object_ids[0]

            raise InvalidParameterException(
                "The {} object '{}' was not found on the Rubrik cluster.".format(object_type, object_name))

    def assign_sla(self, object_name, sla_name, object_type, log_backup_frequency_in_seconds=None, log_retention_hours=None, copy_only=None, timeout=30):  # pytest: ignore
        """Assign a Rubrik object to an SLA Domain.

        Arguments:
            object_name {str} -- The name of the Rubrik object you wish to assign to an SLA Domain.
            sla_name {str} -- The name of the SLA Domain you wish to assign an object to. To exclude the object from all SLA assignments use `do not protect` as the `sla_name`. To assign the selected object to the SLA of the next higher level object use `clear` as the `sla_name`.
            object_type {str} -- The Rubrik object type you want to assign to the SLA Domain. (choices: {vmware, mssql_host})

        Keyword Arguments:
            log_backup_frequency_in_seconds {str} -- The MSSQL Log Backup frequency you'd like to specify with the SLA. Required when the `object_type` is `mssql_host`. (default {None})
            log_retention_hours {int} -- The MSSQL Log Retention frequency you'd like to specify with the SLA. Required when the `object_type` is `mssql_host`. (default {None})
            copy_only {int} -- Take Copy Only Backups with MSSQL. Required when the `object_type` is `mssql_host`. (default {None})
            timeout {bool} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {30})

        Returns:
            str -- No change required. The vSphere VM '`object_name`' is already assigned to the '`sla_name`' SLA Domain.
            dict -- The full API reponse for `POST /internal/sla_domain/{sla_id}/assign`.
        """

        valid_object_type = ['vmware', 'mssql_host']

        if object_type not in valid_object_type:
            raise InvalidParameterException(
                "The assign_sla() object_type argument must be one of the following: {}.".format(valid_object_type))

        if object_type == "mssql_host":
            if log_backup_frequency_in_seconds is None or log_retention_hours is None or copy_only is None:
                raise InvalidParameterException(
                    "When the object_type is 'mssql_host' the 'log_backup_frequency_in_seconds', 'log_retention_hours', 'copy_only' paramaters must be populated.")
        # Determine if 'do not protect' or 'clear' are the SLA Domain Name
        do_not_protect_regex = re.findall('\\bdo not protect\\b', sla_name, flags=re.IGNORECASE)
        clear_regex = re.findall('\\bclear\\b', sla_name, flags=re.IGNORECASE)

        if len(do_not_protect_regex) > 0:
            sla_id = "UNPROTECTED"
        elif len(clear_regex) > 0:
            sla_id = 'INHERIT'
        else:
            self.log("assign_sla: Searching the Rubrik cluster for the SLA Domain '{}'.".format(sla_name))
            sla_id = self.object_id(sla_name, 'sla', timeout=timeout)

        if object_type == 'vmware':
            self.log("assign_sla: Searching the Rubrik cluster for the vSphere VM '{}'.".format(object_name))
            vm_id = self.object_id(object_name, object_type, timeout=timeout)

            self.log("assign_sla: Determing the SLA Domain currently assigned to the vSphere VM '{}'.".format(object_name))
            vm_summary = self.get('v1', '/vmware/vm/{}'.format(vm_id), timeout=timeout)

            if sla_id == vm_summary['configuredSlaDomainId']:
                return "No change required. The vSphere VM '{}' is already assigned to the '{}' SLA Domain.".format(
                    object_name, sla_name)
            else:
                self.log("assign_sla: Assigning the vSphere VM '{}' to the '{}' SLA Domain.".format(object_name, sla_name))

                config = {}
                config['managedIds'] = [vm_id]

                return self.post("internal", "/sla_domain/{}/assign".format(sla_id), config, timeout)

        elif object_type == 'mssql_host':

            host_id = ''
            mssql_id = ''
            db_sla_lst = []

            self.log('Searching the Rubrik cluster for the current hosts.')
            current_hosts = self.get(
                'v1',
                '/host?operating_system_type=Windows&primary_cluster_id=local',
                timeout=timeout)

            for rubrik_host in current_hosts['data']:
                if rubrik_host['name'] == object_name:
                    host_id = rubrik_host['id']

            if(host_id):
                self.log("assign_sla: Searching the Rubrik cluster for the MSSQL Instance '{}'.".format(object_name))
                mssql_instances = self.get('v1', '/mssql/instance?root_id={}'.format(host_id), timeout=timeout)

                for mssql_instance in mssql_instances['data']:
                    mssql_id = mssql_instance['id']
                    mssql_instance_name = mssql_instance['name']

                    self.log(
                        "assign_sla: Determing the SLA Domain currently assigned to the MSSQL Instance '{}'.".format(mssql_instance_name))

                    mssql_summary = self.get('v1', '/mssql/instance/{}'.format(mssql_id), timeout=timeout)

                    if (sla_id == mssql_summary['configuredSlaDomainId'] and log_backup_frequency_in_seconds == mssql_summary['logBackupFrequencyInSeconds'] and
                            log_retention_hours == mssql_summary['logRetentionHours'] and copy_only == mssql_summary['copyOnly']):
                        return "No change required. The MSSQL Instance '{}' is already assigned to the '{}' SLA Domain with the following log settings:" \
                               " log_backup_frequency_in_seconds: {}, log_retention_hours: {} and copy_only: {}.".format(
                                   object_name, sla_name, log_backup_frequency_in_seconds, log_retention_hours, copy_only)

                    else:
                        self.log(
                            "assign_sla: Assigning the MSSQL Instance '{}' to the '{}' SLA Domain.".format(
                                object_name, sla_name))

                        config = {}
                        if log_backup_frequency_in_seconds is not None:
                            config['logBackupFrequencyInSeconds'] = log_backup_frequency_in_seconds
                        if log_retention_hours is not None:
                            config['logRetentionHours'] = log_retention_hours
                        if copy_only is not None:
                            config['copyOnly'] = copy_only

                        config['configuredSlaDomainId'] = sla_id

                        patch_resp = self.patch("v1", "/mssql/instance/{}".format(mssql_id), config, timeout)
                        db_sla_lst.append(patch_resp)
            else:
                raise InvalidParameterException(
                    "Host ID not found for instance '{}'").format(object_name)

            return db_sla_lst

    def vsphere_live_mount(self, vm_name, date='latest', time='latest', host='current', remove_network_devices=False, power_on=True, timeout=15):  # pylint: ignore
        """Live Mount a vSphere VM from a specified snapshot. If a specific date and time is not provided, the last snapshot taken will be used.

        Arguments:
            vm_name {str} -- The name of the vSphere VM to Live Mount.

        Keyword Arguments:
            date {str} -- The date of the snapshot you wish to Live Mount formated as `Month-Day-Year` (ex: 1-15-2014). If `latest` is specified, the last snapshot taken will be used. (default: {'latest'})
            time {str} -- The time of the snapshot you wish to Live Mount formated formated as `Hour:Minute AM/PM` (ex: 1:30 AM). If `latest` is specified, the last snapshot taken will be used. (default: {'latest'})
            host {str} -- The hostname or IP address of the ESXi host to Live Mount the VM on. By default, the current host will be used. (default: {'current'})
            remove_network_devices {bool} -- Flag that determines whether to remove the network interfaces from the Live Mounted VM. Set to `True` to remove all network interfaces. (default: {False})
            power_on {bool} -- Flag that determines whether the VM should be powered on after the Live Mount. Set to `True` to power on the VM. Set to `False` to mount the VM but not power it on. (default: {True})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            dict -- The full response of `POST /v1/vmware/vm/snapshot/{snapshot_id}/mount`.
        """

        if isinstance(remove_network_devices, bool) is False:
            raise InvalidTypeException("The 'remove_network_devices' argument must be True or False.")
        elif isinstance(power_on, bool) is False:
            raise InvalidTypeException("The 'power_on' argument must be True or False.")
        elif date != 'latest' and time == 'latest' or date == 'latest' and time != 'latest':
            raise InvalidParameterException(
                "The date and time arguments most both be 'latest' or a specific date and time.")

        self.log("vsphere_live_mount: Searching the Rubrik cluster for the vSphere VM '{}'.".format(vm_name))
        vm_id = self.object_id(vm_name, 'vmware', timeout=timeout)

        self.log("vsphere_live_mount: Getting a list of all Snapshots for vSphere VM '{}'.".format(vm_name))
        vm_summary = self.get('v1', '/vmware/vm/{}'.format(vm_id), timeout=timeout)

        if date == 'latest' and time == 'latest':
            number_of_snapshots = len(vm_summary['snapshots'])
            snapshot_id = vm_summary['snapshots'][number_of_snapshots - 1]['id']
        else:
            self.log("vsphere_live_mount: Converting the provided date/time into UTC.")
            snapshot_date_time = self._date_time_conversion(date, time)

            current_snapshots = {}

            for snapshot in vm_summary['snapshots']:
                current_snapshots[snapshot['id']] = snapshot['date']

            self.log("vsphere_live_mount: Searching for the provided snapshot.")
            for id, date_time in current_snapshots.items():
                if snapshot_date_time in date_time:
                    snapshot_id = id

        try:
            snapshot_id
        except NameError:
            raise InvalidParameterException("The vSphere VM '{}' does not have a snapshot taken on {} at {}.".format(
                vm_name, date, time))
        else:
            if host == 'current':
                host_id = vm_summary['hostId']
            else:
                host_id = self.object_id(host, 'vmware_host', timeout=timeout)

            config = {}
            config['hostId'] = host_id
            config['removeNetworkDevices'] = remove_network_devices
            config['powerOn'] = power_on

            self.log(
                "vsphere_live_mount: Live Mounting the snapshot taken on {} at {} for vSphere VM '{}'.".format(
                    date,
                    time,
                    vm_name))

            return self.post('v1', '/vmware/vm/snapshot/{}/mount'.format(snapshot_id), config, timeout)

    def vsphere_instant_recovery(self, vm_name, date='latest', time='latest', host='current', remove_network_devices=False, power_on=True, disable_network=False, keep_mac_addresses=False, preserve_moid=False, timeout=15):  # pylint: ignore
        """Instantly recover a vSphere VM from a provided snapshot. If a specific date and time is not provided, the last snapshot taken will be used.

        Arguments:
            vm_name {str} -- The name of the VM to Instantly Recover.

        Keyword Arguments:
            date {str} -- The date of the snapshot you wish to Instantly Recover formated as `Month-Day-Year` (ex: 1-15-2014). If 'latest' is specified, the last snapshot taken will used. (default: {'latest'})
            time {str} -- The time of the snapshot you wish to Instantly Recover formated formated as `Hour:Minute AM/PM`  (ex: 1:30 AM). If 'latest' is specified, the last snapshot taken will be used. (default: {'latest'})
            host {str} -- The hostname or IP address of the ESXi host to Instantly Recover the VM on. By default, the current host will be used. (default: {'current'})
            remove_network_devices {bool} -- Flag that determines whether to remove the network interfaces from the Instantly Recovered VM. Set to `True` to remove all network interfaces. (default: {False})
            power_on {bool} -- Flag that determines whether the VM should be powered on after Instant Recovery. Set to `True` to power on the VM. Set to `False` to instantly recover the VM but not power it on. (default: {True})
            disable_network {bool} -- Sets the state of the network interfaces when the VM is instantly recovered. Use `False` to enable the network interfaces. Use `True` to disable the network interfaces. Disabling the interfaces can prevent IP conflicts. (default: {False})
            keep_mac_addresses {bool} -- Flag that determines whether the MAC addresses of the network interfaces on the source VM are assigned to the new VM. Set to `True` to assign the original MAC addresses to the new VM. Set to `False` to assign new MAC addresses. When 'remove_network_devices' is set to `True`, this property is ignored. (default: {False})
            preserve_moid {bool} -- Flag that determines whether to preserve the MOID of the source VM in a restore operation. Use `True` to keep the MOID of the source. Use `False` to assign a new moid. (default: {False})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            dict -- The full response of `POST /v1/vmware/vm/snapshot/{snapshot_id}/instant_recover`.
        """

        if isinstance(remove_network_devices, bool) is False:
            raise InvalidTypeException("The 'remove_network_devices' argument must be True or False.")
        elif isinstance(power_on, bool) is False:
            raise InvalidTypeException("The 'power_on' argument must be True or False.")
        elif isinstance(disable_network, bool) is False:
            raise InvalidTypeException("The 'disable_network' argument must be True or False.")
        elif isinstance(keep_mac_addresses, bool) is False:
            raise InvalidTypeException("The 'keep_mac_addresses' argument must be True or False.")
        elif isinstance(preserve_moid, bool) is False:
            raise InvalidTypeException("The 'preserve_moid' argument must be True or False.")
        elif date != 'latest' and time == 'latest' or date == 'latest' and time != 'latest':
            raise InvalidParameterException(
                "The date and time arguments most both be 'latest' or a specific date and time.")

        self.log("vsphere_instant_recovery: Searching the Rubrik cluster for the vSphere VM '{}'.".format(vm_name))
        vm_id = self.object_id(vm_name, 'vmware', timeout=timeout)

        self.log("vsphere_instant_recovery: Getting a list of all Snapshots for vSphere VM '{}'.".format(vm_name))
        vm_summary = self.get('v1', '/vmware/vm/{}'.format(vm_id), timeout=timeout)

        if date == 'latest' and time == 'latest':
            number_of_snapshots = len(vm_summary['snapshots'])
            snapshot_id = vm_summary['snapshots'][number_of_snapshots - 1]['id']
        else:
            self.log("vsphere_instant_recovery: Converting the provided date/time into UTC.")
            snapshot_date_time = self._date_time_conversion(date, time)

            current_snapshots = {}
            for snapshot in vm_summary['snapshots']:
                current_snapshots[snapshot['id']] = snapshot['date']

            self.log("vsphere_instant_recovery: Searching for the provided snapshot.")
            for id, date_time in current_snapshots.items():
                if snapshot_date_time in date_time:
                    snapshot_id = id

        try:
            snapshot_id
        except NameError:
            raise InvalidParameterException(
                "The vSphere VM '{}' does not have a snapshot taken on {} at {}.".format(
                    vm_name, date, time))
        else:
            if host == 'current':
                host_id = vm_summary['hostId']
            else:
                host_id = self.object_id(host, 'vmware_host', timeout=timeout)

            config = {}
            config['hostId'] = host_id
            config['removeNetworkDevices'] = remove_network_devices
            config['powerOn'] = power_on
            config['disableNetwork'] = disable_network
            config['keepMacAddresses'] = keep_mac_addresses
            config['preserveMoid'] = preserve_moid

            self.log("vsphere_instant_recovery: Instantly Recovering the snapshot taken on {} at {} for vSphere VM '{}'.".format(
                date,
                time,
                vm_name))

            return self.post('v1', '/vmware/vm/snapshot/{}/instant_recover'.format(snapshot_id), config, timeout)

    def _date_time_conversion(self, date, time, timeout=30):
        """All date values returned by the Rubrik API are stored in Coordinated Universal Time (UTC)
        and need to be converted to the timezone configured on the Rubrik cluster in order to match
        the values provided by the end user in various functions. This internal function will handle that
        conversion process.

        Arguments:
            date {str} -- A date value formated as `Month-Day-Year` (ex: 1/15/2014).
            time {str} -- A time value formated as `Hour:Minute AM/PM` (ex: 1:30 AM).

        Returns:
            str -- A combined date/time value formated as `Year-Month-DayTHour:Minute` where Hour:Minute is on the 24-hour clock (ex : 2014-1-15T01:30).
        """

        from datetime import datetime
        import pytz

        # Validate the Date formating
        try:
            snapshot_date = datetime.strptime(date, '%m-%d-%Y')
        except ValueError:
            raise InvalidParameterException(
                "The date argument '{}' must be formatd as 'Month-Date-Year' (ex: 8-9-2018).".format(date))
        # Validate the Time formating
        try:
            snapshot_time = datetime.strptime(time, '%I:%M %p')
        except ValueError:
            raise InvalidParameterException(
                "The time argument '{}' must be formatd as 'Hour:Minute AM/PM' (ex: 2:57 AM).".format(time))

        self.log("_date_time_conversion: Getting the Rubrik cluster timezone.")
        cluster_summary = self.get('v1', '/cluster/me', timeout=timeout)
        cluster_timezone = cluster_summary['timezone']['timezone']

        self.log("_date_time_conversion: Converting the provided time to the 24-hour clock.")
        snapshot_time_24_hour_clock = datetime.strftime(snapshot_time, "%H:%M")

        self.log("_date_time_conversion: Creating a combined date/time variable.")
        snapshot_datetime = datetime.strptime('{} {}'.format(
            date, snapshot_time_24_hour_clock), '%m-%d-%Y %H:%M')

        # Add Timezone to snapshot_datetime Variable
        timezone = pytz.timezone(cluster_timezone)
        snapshot_datetime = timezone.localize(snapshot_datetime)

        self.log("_date_time_conversion: Converting the time to UTC.\n")
        utc_timezone = pytz.UTC
        snapshot_datetime = snapshot_datetime.astimezone(utc_timezone)

        return snapshot_datetime.strftime('%Y-%m-%dT%H:%M')

    def pause_snapshots(self, object_name, object_type, timeout=180):
        """Pause all snapshot activity for the provided object.

        Arguments:
            object_name {str} -- The name of the Rubrik object to pause snapshots for.
            object_type {str} -- The Rubrik object type you wish to pause snaphots on. (choices: {vmware})

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster. (default: {180})

        Returns:
            str -- No change required. The '`object_type`' '`object_name`' is already paused.
            dict -- The full API response for `PATCH /v1/vmware/vm/{vm_id}`.
        """

        valid_object_type = ['vmware']

        if object_type not in valid_object_type:
            raise InvalidParameterException("The pause_snapshots() object_type argument must be one of the following: {}.".format(
                valid_object_type))

        if object_type == 'vmware':

            self.log("pause_snapshots: Searching the Rubrik cluster for the vSphere VM '{}'.".format(object_name))
            vm_id = self.object_id(object_name, object_type, timeout=timeout)

            self.log("pause_snapshots: Determing the current pause state of the vSphere VM '{}'.".format(object_name))
            api_request = self.get('v1', '/vmware/vm/{}'.format(vm_id), timeout=timeout)

            if api_request['blackoutWindowStatus']['isSnappableBlackoutActive']:
                return "No change required. The {} VM '{}' is already paused.".format(object_type, object_name)
            else:
                self.log("pause_snapshots: Pausing Snaphots for the vSphere VM '{}'.".format(object_name))
                config = {}
                config['isVmPaused'] = True

                return self.patch('v1', '/vmware/vm/{}'.format(vm_id), config, timeout)

    def resume_snapshots(self, object_name, object_type, timeout=180):
        """Resume all snapshot activity for the provided object.

        Arguments:
            object_name {str} -- The name of the Rubrik object to resume snapshots for.
            object_type {str} -- The Rubrik object type you wish to resume snaphots on. (choices: {vmware})

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster. (default: {180})

        Returns:
            str -- No change required. The 'object_type' object 'object_name' is currently not paused.
            dict -- The full response for `PATCH /v1/vmware/vm/{vm_id}`.
        """

        valid_object_type = ['vmware']

        if object_type not in valid_object_type:
            raise InvalidParameterException("The resume_snapshots() object_type argument must be one of the following: {}.".format(
                valid_object_type))

        if object_type == 'vmware':

            self.log("resume_snapshots: Searching the Rubrik cluster for the vSphere VM '{}'.".format(object_name))
            vm_id = self.object_id(object_name, object_type, timeout=timeout)

            self.log("resume_snapshots: Determing the current pause state of the vSphere VM '{}'.".format(object_name))
            api_request = self.get('v1', '/vmware/vm/{}'.format(vm_id), timeout=timeout)

            if not api_request['blackoutWindowStatus']['isSnappableBlackoutActive']:
                return "No change required. The '{}' object '{}' is currently not paused.".format(
                    object_type, object_name)
            else:
                self.log("resume_snapshots: Resuming Snaphots for the vSphere VM '{}'.".format(object_name))
                config = {}
                config['isVmPaused'] = False

                return self.patch('v1', '/vmware/vm/{}'.format(vm_id), config, timeout)

    def begin_managed_volume_snapshot(self, name, timeout=30):
        """Open a managed volume for writes. All writes to the managed volume until the snapshot is ended will be part of its snapshot.

        Arguments:
            name {str} -- The name of the Managed Volume to begin the snapshot on.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster. (default: {30})

        Returns:
            str -- No change required. The Managed Volume '`name`' is already assigned in a writeable state.
            dict -- The full API response for `POST /managed_volume/{id}/begin_snapshot`.
        """

        self.log("begin_managed_volume_snapshot: Searching the Rubrik cluster for the Managed Volume '{}'.".format(name))
        managed_volume_id = self.object_id(name, 'managed_volume', timeout=timeout)

        self.log("begin_managed_volume_snapshot: Determing the state of the Managed Volume '{}'.".format(name))
        managed_volume_summary = self.get('internal', '/managed_volume/{}'.format(managed_volume_id), timeout=timeout)

        if not managed_volume_summary['isWritable']:
            self.log("begin_managed_volume_snapshot: Setting the Managed Volume '{}' to a writeable state.".format(name))
            return self.post('internal', '/managed_volume/{}/begin_snapshot'.format(managed_volume_id),
                             config={}, timeout=timeout)
        else:
            return "No change required. The Managed Volume '{}' is already assigned in a writeable state.".format(name)

    def end_managed_volume_snapshot(self, name, sla_name='current', timeout=30):
        """Close a managed volume for writes. A snapshot will be created containing all writes since the last begin snapshot call.

        Arguments:
            name {str} -- The name of the Managed Volume to end snapshots on.

        Keyword Arguments:
            sla_name {str} -- The SLA Domain name you want to assign the snapshot to. By default, the currently assigned SLA Domain will be used. (default: {'current'})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster. (default: {30})

        Returns:
            str -- No change required. The Managed Volume `name` is already assigned in a read only state.
            dict -- The full API response for `POST /managed_volume/{id}/end_snapshot`.
        """

        self.log("end_managed_volume_snapshot: Searching the Rubrik cluster for the Managed Volume '{}'.".format(name))
        managed_volume_id = self.object_id(name, 'managed_volume', timeout=timeout)

        self.log("end_managed_volume_snapshot: Determing the state of the Managed Volume '{}'.".format(name))
        managed_volume_summary = self.get("internal", "/managed_volume/{}".format(managed_volume_id), timeout=timeout)

        if not managed_volume_summary['isWritable']:
            return "No change required. The Managed Volume 'name' is already assigned in a read only state."

        if sla_name == 'current':
            self.log(
                "end_managed_volume_snapshot: Searching the Rubrik cluster for the SLA Domain assigned to the Managed Volume '{}'.".format(name))
            if managed_volume_summary['slaAssignment'] == 'Unassigned' or managed_volume_summary['effectiveSlaDomainId'] == 'UNPROTECTED':
                raise InvalidParameterException(
                    "The Managed Volume '{}' does not have a SLA assigned currently assigned. You must populate the sla_name argument.".format(name))
            config = {}
        else:
            self.log("end_managed_volume_snapshot: Searching the Rubrik cluster for the SLA Domain '{}'.".format(sla_name))
            sla_id = self.object_id(sla_name, 'sla', timeout=timeout)

            config = {}
            config['retentionConfig'] = {}
            config['retentionConfig']['slaId'] = sla_id

        return self.post("internal", "/managed_volume/{}/end_snapshot".format(managed_volume_id), config, timeout)

    def get_sla_objects(self, sla, object_type, timeout=15):
        """Retrieve the name and ID of a specific object type.

        Arguments:
            sla {str} -- The name of the SLA Domain you wish to search.
            object_type {str} -- The object type you wish to search the SLA for. (choices: {vmware})

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster. (default: {15})

        Returns:
            dict -- The `name:id` of each object in the provided SLA Domain.
        """

        valid_object_type = ['vmware']

        if object_type not in valid_object_type:
            raise InvalidParameterException(
                "The get_sla_object() object_type argument must be one of the following: {}.".format(valid_object_type))

        if object_type == 'vmware':

            sla_id = self.object_id(sla, "sla", timeout=timeout)

            all_vms_in_sla = self.get(
                "v1",
                "/vmware/vm?effective_sla_domain_id={}&is_relic=false".format(sla_id),
                timeout=timeout)

            vm_name_id = {}
            for vm in all_vms_in_sla["data"]:
                vm_name_id[vm["name"]] = vm["id"]

            if bool(vm_name_id) is False:
                raise InvalidParameterException(
                    "The SLA '{}' is currently not protecting any {} objects.".format(
                        sla, object_type))

            return vm_name_id
