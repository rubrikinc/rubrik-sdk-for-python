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
from datetime import datetime
from .api import Api
from .exceptions import CDMVersionException, InvalidParameterException, InvalidTypeException, APICallException




_API = Api


class Data_Management(_API):
    """This class contains methods related to backup and restore operations for the various objects managed by the Rubrik cluster."""

    def on_demand_snapshot(self, object_name, object_type, sla_name='current', fileset=None, host_os=None, sql_host=None, sql_instance=None, sql_db=None, hostname=None, timeout=15):  # pylint: ignore
        """Initiate an on-demand snapshot.

        Arguments:
            object_name {str} -- The name of the Rubrik object to take a on-demand snapshot of.
            object_type {str} -- The Rubrik object type you want to backup. (choices: {vmware, physical_host, ahv, mssql})

        Keyword Arguments:
            sla_name {str} -- The SLA Domain name you want to assign the on-demand snapshot to. By default, the currently assigned SLA Domain will be used. (default: {'current'})
            fileset {str} -- The name of the Fileset you wish to backup. Only required when taking a on-demand snapshot of a physical host. (default: {'None'})
            host_os {str} -- The operating system for the physical host. Only required when taking a on-demand snapshot of a physical host. (default: {'None'}) (choices: {Linux, Windows})
            hostname {str} -- The host name, or one of the host names in the cluster, that the Oracle database is running. Required when the object_type is oracle_db.
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            tuple -- When object_type is vmware, the full API response for `POST /v1/vmware/vm/{ID}/snapshot` and the job status URL which can be used to monitor progress of the snapshot. (api_response, job_status_url)
            tuple -- When object_type is physical_host, the full API response for `POST /v1/fileset/{}/snapshot` and the job status URL which can be used to monitor progress of the snapshot. (api_response, job_status_url)

        """

        valid_object_type = ['vmware', 'physical_host', 'ahv', 'mssql_db', 'oracle_db']
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

            self.log("on_demand_snapshot: Initiating snapshot for the MS SQL '{}'.".format(object_name))
            api_request = self.post('v1', '/mssql/db/{}/snapshot'.format(mssql_id), config, timeout)

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

        elif object_type == 'oracle_db':
            if hostname is None:
                raise InvalidParameterException(
                    "You must provide the host or one of the hosts in a RAC cluster for the Oracle DB object.")

            self.log(
                "on_demand_snapshot: Searching the Rubrik cluster for the Oracle database '{}' on the host '{}'.".format(
                    object_name,
                    hostname))
            db_id = self.object_id(object_name, object_type, hostname=hostname, timeout=timeout)

            if sla_name == 'current':
                self.log(
                    "on_demand_snapshot: Searching the Rubrik cluster for the SLA Domain assigned to the Oracle database '{}'.".format(
                        object_name))

                oracle_db_summary = self.get('internal', '/oracle/db/{}'.format(db_id), timeout)
                sla_id = oracle_db_summary['effectiveSlaDomainId']

            elif sla_name != 'current':
                self.log("on_demand_snapshot: Searching the Rubrik cluster for the SLA Domain '{}'.".format(sla_name))
                sla_id = self.object_id(sla_name, 'sla', timeout=timeout)

            config = {}
            config['slaId'] = sla_id

            self.log("on_demand_snapshot: Initiating snapshot for the Oracle database '{}'.".format(object_name))
            api_request = self.post('internal', '/oracle/db/{}/snapshot'.format(db_id), config, timeout)

            snapshot_status_url = api_request['links'][0]['href']

        return (api_request, snapshot_status_url)

    def object_id(self, object_name, object_type, host_os=None, hostname=None, timeout=15):
        """Get the ID of a Rubrik object by providing its name.

        Arguments:
            object_name {str} -- The name of the Rubrik object whose ID you wish to lookup.
            object_type {str} -- The object type you wish to look up. (choices: {vmware, sla, vmware_host, physical_host, fileset_template, managed_volume, mysql_db, mysql_instance, vcenter, ahv, aws_native, oracle_db, volume_group, archival_location})
            hostname {str} -- The hostname, or one of the hostnames in the cluster, that the Oracle database is running. Required when the object_type is oracle_db.
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
            'aws_native',
            'oracle_db',
            'volume_group',
            'archival_location']

        if object_type not in valid_object_type:
            raise InvalidParameterException("The object_id() object_type argument must be one of the following: {}.".format(
                valid_object_type))

        if object_type == 'fileset_template':
            if host_os is None:
                raise InvalidParameterException("You must provide the Fileset Template OS type.")
            elif host_os not in ['Linux', 'Windows']:
                raise InvalidParameterException("The host_os must be either 'Linux' or 'Windows'.")

        if object_type == 'sla':
            if object_name.upper() == "FOREVER" or object_name.upper() == "UNPROTECTED":
                return "UNPROTECTED"

        if object_type == 'oracle_db':
            if hostname is None:
                raise InvalidParameterException(
                    "You must provide the host or one of the hosts in a RAC cluster for the Oracle DB object.")

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
            },
            "oracle_db": {
                "api_version": "internal",
                "api_endpoint": "/oracle/db"
            },
            "volume_group": {
                "api_version": "internal",
                "api_endpoint": "/volume_group?is_relic=false"
            },
            "archival_location": {
                "api_version": "internal",
                "api_endpoint": "/archive/location?name={}".format(object_name)
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
            elif object_type == "volume_group":
                name_value = "hostname"
            else:
                name_value = 'name'

            host_match = False
            for item in api_request['data']:
                if object_type == 'oracle_db' and item[name_value] == object_name:
                    for instance in item['instances']:
                        if hostname in instance['hostName']:
                            object_ids.append(item['id'])
                            host_match = True
                elif item[name_value] == object_name:
                    object_ids.append(item['id'])

            if object_type == 'oracle_db' and not host_match:
                raise InvalidParameterException(
                    "The {} object '{}' on the host '{}' was not found on the Rubrik cluster.".format(object_type, object_name, hostname))
            elif len(object_ids) > 1:
                raise InvalidParameterException(
                    "Multiple {} objects named '{}' were found on the Rubrik cluster. Unable to return a specific object id.".format(object_type, object_name))
            elif len(object_ids) == 0:
                raise InvalidParameterException(
                    "The {} object '{}' was not found on the Rubrik cluster.".format(object_type, object_name))
            else:
                return object_ids[0]

            raise InvalidParameterException(
                "The {} object '{}' was not found on the Rubrik cluster.".format(object_type, object_name))

    def assign_sla(self, object_name, sla_name, object_type, log_backup_frequency_in_seconds=None, log_retention_hours=None, copy_only=None, windows_host=None, timeout=30):  # pytest: ignore
        """Assign a Rubrik object to an SLA Domain.

        Arguments:
            object_name {str or list} -- The name of the Rubrik object you wish to assign to an SLA Domain. When the 'object_type' is 'volume_group', the object_name can be a list of volumes.
            sla_name {str} -- The name of the SLA Domain you wish to assign an object to. To exclude the object from all SLA assignments use `do not protect` as the `sla_name`. To assign the selected object to the SLA of the next higher level object use `clear` as the `sla_name`.
            object_type {str} -- The Rubrik object type you want to assign to the SLA Domain. (choices: {vmware, mssql_host, volume_group})

        Keyword Arguments:
            log_backup_frequency_in_seconds {str} -- The MSSQL Log Backup frequency you'd like to specify with the SLA. Required when the `object_type` is `mssql_host`. (default {None})
            log_retention_hours {int} -- The MSSQL Log Retention frequency you'd like to specify with the SLA. Required when the `object_type` is `mssql_host`. (default {None})
            copy_only {int} -- Take Copy Only Backups with MSSQL. Required when the `object_type` is `mssql_host`. (default {None})
            windows_host {str} -- The name of the Windows host that contains the relevant volume group. Required when the `object_type` is `volume_group`. (default {None})
            timeout {bool} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {30})

        Returns:
            str -- No change required. The vSphere VM '`object_name`' is already assigned to the '`sla_name`' SLA Domain.
            str -- No change required. The MSSQL Instance '`object_name`' is already assigned to the '`sla_name`' SLA Domain with the following log settings: log_backup_frequency_in_seconds: `log_backup_frequency_in_seconds`, log_retention_hours: `log_retention_hours` and copy_only: `copy_only`
            str -- No change required. The '`object_name`' volume_group is already assigned to the '`sla_name`' SLA Domain.
            dict -- The full API response for `POST /internal/sla_domain/{sla_id}/assign`.
            dict -- The full API response for `PATCH /internal/volume_group/{id}`.
        """

        valid_object_type = ['vmware', 'mssql_host', 'volume_group']

        if object_type not in valid_object_type:
            raise InvalidParameterException(
                "The assign_sla() object_type argument must be one of the following: {}.".format(valid_object_type))

        if object_type == "mssql_host":
            if log_backup_frequency_in_seconds is None or log_retention_hours is None or copy_only is None:
                raise InvalidParameterException(
                    "When the object_type is 'mssql_host' the 'log_backup_frequency_in_seconds', 'log_retention_hours', 'copy_only' paramaters must be populated.")

        if object_type == "volume_group":

            if not isinstance(object_name, (str, list)):
                raise InvalidParameterException(
                    "When the object_type is 'volume_group', the 'object_name' must be a string or a list.")

            if windows_host is None:
                raise InvalidParameterException(
                    "When the object_type is 'volumge_group' the 'windows_host' paramater must be populated.")
        else:
            if not isinstance(object_name, (str)):
                raise InvalidParameterException("The object_name must be a string.")

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

            # After 5.0, "hostname" is a deprecated field in the results that are returned in "current_hosts"
            if self.minimum_installed_cdm_version(5.0):
                current_hosts_name = "name"
            else:
                current_hosts_name = "hostname"

            for rubrik_host in current_hosts['data']:
                if rubrik_host[current_hosts_name] == object_name:
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

        elif object_type == "volume_group":

            volume_group_id = self.object_id(windows_host, "volume_group", timeout=timeout)
            physical_host_id = self.object_id(windows_host, "physical_host", host_os="windows", timeout=timeout)

            self.log("assign_sla: Getting a list of all volumes on the '{}' Windows host.".format(windows_host))
            host_volumes = self.get("internal", "/host/{}/volume".format(physical_host_id), timeout=timeout)

            # If the object_name (volumes to assign to the SLA) is a string, create a list for processing
            if not isinstance(object_name, list):
                volumes_to_assign = [object_name]
            else:
                volumes_to_assign = object_name

            # Create a mapping of the volumes on the windows host and their ids
            currnt_volumes = {}
            for volume in host_volumes["data"]:
                for v in volume["mountPoints"]:
                    if v in volumes_to_assign:
                        currnt_volumes[v] = volume["id"]

            # Validate that the provided volume(s) are on the windows host
            for v in volumes_to_assign:
                try:
                    currnt_volumes[v]
                except KeyError:
                    raise InvalidParameterException(
                        "The Windows Host '{}' does not have a '{}' volume.".format(windows_host, v))

            self.log("assign_sla: Getting details of the current volume group on the Windows host.")
            volume_group_details = self.get("internal", "/volume_group/{}".format(volume_group_id), timeout=timeout)

            # Create a config of the current volume sla settings
            current_volumes_included_in_snapshot = []
            for volume in volume_group_details["volumes"]:
                current_volumes_included_in_snapshot.append(volume["id"])

            current_config = {}
            current_config["configuredSlaDomainId"] = volume_group_details["configuredSlaDomainId"]
            current_config["volumeIdsIncludedInSnapshots"] = current_volumes_included_in_snapshot

            # Create the user desired config
            volumes_included_in_snapshot = []
            for volume, volume_id in currnt_volumes.items():
                volumes_included_in_snapshot.append(volume_id)

            config = {}
            config["configuredSlaDomainId"] = sla_id
            config["volumeIdsIncludedInSnapshots"] = volumes_included_in_snapshot

            if current_config == config:
                return "No change required. The {} volume_group is already assigned to the {} SLA.".format(
                    object_name, sla_name)
            else:
                self.log("assign_sla: Assigning the vSphere VM '{}' to the '{}' SLA Domain.".format(object_name, sla_name))
                return self.patch("internal", "/volume_group/{}".format(volume_group_id), config, timeout=timeout)

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

    def create_sla(self, name, hourly_frequency=None, hourly_retention=None, daily_frequency=None, daily_retention=None, monthly_frequency=None, monthly_retention=None, yearly_frequency=None, yearly_retention=None, archive_name=None, retention_on_brik_in_days=None, instant_archive=False, timeout=15):  # pylint: ignore
        """Create a new SLA Domain.

        Arguments:
            name {str} -- The name of the new SLA Domain.

        Keyword Arguments:
            hourly_frequency {int} -- Hourly frequency to take backups. (default: {None})
            hourly_retention {int} -- Number of hours to retain the hourly backups. (default: {None})
            daily_frequency {int} -- Daily frequency to take backups. (default: {None})
            daily_retention {int} -- Number of hours to retain the daily backups. (default: {None})
            monthly_frequency {int} -- Monthly frequency to take backups. (default: {None})
            monthly_retention {int} -- Number of hours to retain the monthly backups. (default: {None})
            yearly_frequency {int} -- Yearly frequency to take backups. (default: {None})
            yearly_retention {int} -- Number of hours to retain the yearly backups. (default: {None})
            archive_name {str} -- The optional archive location you wish to configure on the SLA Domain. When populated, you must also provide a `retention_on_brik_in_days`. (default: {None})
            retention_on_brik_in_days {int} -- The number of days you wish to keep the backups on the Rubrik cluster. When populated, you must also provide a `archive_name`. (default: {None})
            instant_archive= {bool} -- Flag that determines whether or not to enable instant archive. Set to true to enable. (default: {False})

        Returns:
            str -- No change required. The 'name' SLA Domain is already configured with the provided configuration.
            dict -- The full API response for `POST /v1/sla_domain`.
            dict -- The full API response for `POST /v2/sla_domain`.
        """

        v2_sla = self.minimum_installed_cdm_version("5.0", timeout=timeout)

        all_params = [
            hourly_frequency,
            hourly_retention,
            daily_frequency,
            daily_retention,
            monthly_frequency,
            monthly_retention,
            yearly_frequency,
            yearly_retention]

        # Validate all values besides name are ints
        for param in all_params:
            if not isinstance(param, int):
                raise InvalidParameterException("All 'frequency' and 'retention' parameters must be integers.")

        if not isinstance(retention_on_brik_in_days, int) and retention_on_brik_in_days is not None:
            raise InvalidParameterException("The 'retention_on_brik_in_days' parameter must be integer.")

        # Make sure at least one frequency and retention is populated
        if all(value is None for value in all_params):
            raise InvalidParameterException("You must populate at least one frequency and retention.")

        # Make sure the "time unit" frequency and retention are used together
        if hourly_frequency is not None and hourly_retention is None or hourly_frequency is None and hourly_retention is not None:
            raise InvalidParameterException(
                "The 'hourly_frequency' and 'hourly_retention' parameters must be populated together.")

        if daily_frequency is not None and daily_retention is None or daily_frequency is None and daily_retention is not None:
            raise InvalidParameterException(
                "The 'daily_frequency' and 'daily_retention' parameters must be populated together.")

        if monthly_frequency is not None and monthly_retention is None or monthly_frequency is None and monthly_retention is not None:
            raise InvalidParameterException(
                "The 'monthly_frequency' and 'monthly_retention' parameters must be populated together.")

        if yearly_frequency is not None and yearly_retention is None or yearly_frequency is None and yearly_retention is not None:
            raise InvalidParameterException(
                "The 'yearly_frequency' and 'yearly_retention' parameters must be populated together.")

        if archive_name is not None and retention_on_brik_in_days is None or archive_name is None and retention_on_brik_in_days is not None:
            raise InvalidParameterException(
                "The 'archive_name' and 'retention_on_brik_in_days' parameters must be populated together.")

        try:
            # object_id() will set sla_already_present to something besides False if the SLA is already on the cluter
            sla_id = self.object_id(name, "sla", timeout=timeout)
        except InvalidParameterException:
            sla_id = False

        config = {}

        config["name"] = name

        if v2_sla is True:
            # create the config for the v2 API
            config["frequencies"] = {}

            config["frequencies"]["hourly"] = {}
            config["frequencies"]["hourly"]["frequency"] = hourly_frequency
            config["frequencies"]["hourly"]["retention"] = hourly_retention

            config["frequencies"]["daily"] = {}
            config["frequencies"]["daily"]["frequency"] = daily_frequency
            config["frequencies"]["daily"]["retention"] = daily_retention

            config["frequencies"]["monthly"] = {}
            config["frequencies"]["monthly"]["dayOfMonth"] = "LastDay"
            config["frequencies"]["monthly"]["frequency"] = monthly_frequency
            config["frequencies"]["monthly"]["retention"] = monthly_retention

            config["frequencies"]["yearly"] = {}
            config["frequencies"]["yearly"]["yearStartMonth"] = "January"
            config["frequencies"]["yearly"]["dayOfYear"] = "LastDay"
            config["frequencies"]["yearly"]["frequency"] = yearly_frequency
            config["frequencies"]["yearly"]["retention"] = yearly_retention

        else:
            # Create the config for v1 endpoint
            frequencies = []
            if hourly_frequency is not None:
                frequencies.append({
                    "timeUnit": "Hourly",
                    "frequency": hourly_frequency,
                    "retention": hourly_retention
                })
            if daily_frequency is not None:
                frequencies.append({
                    "timeUnit": "Daily",
                    "frequency": daily_frequency,
                    "retention": daily_retention
                })
            if monthly_frequency is not None:
                frequencies.append({
                    "timeUnit": "Monthly",
                    "frequency": monthly_frequency,
                    "retention": monthly_retention
                })
            if yearly_frequency is not None:
                frequencies.append({
                    "timeUnit": "Yearly",
                    "frequency": yearly_frequency,
                    "retention": yearly_retention
                })
            config["frequencies"] = frequencies

        if archive_name is not None:
            archival_location_id = self.object_id(archive_name, "archival_location", timeout=timeout)

            # convert retention in days to seconds
            retention_on_brik_in_seconds = retention_on_brik_in_days * 86400
            if instant_archive is False:
                archival_threshold = retention_on_brik_in_seconds
            else:
                archival_threshold = 1

            config["localRetentionLimit"] = archival_threshold

            config["archivalSpecs"] = [{
                "locationId": archival_location_id,
                "archivalThreshold": archival_threshold
            }]

        if sla_id is not False:
            self.log("create_sla: Getting the configuration details for the SLA Domain {} already on the Rubrik cluster.".format(name))
            if v2_sla is True:
                current_sla_details = self.get("v2", "/sla_domain/{}".format(sla_id), timeout=timeout)
            else:
                current_sla_details = self.get("v1", "/sla_domain/{}".format(sla_id), timeout=timeout)

            keys_to_delete = [
                "id",
                "primaryClusterId",
                "allowedBackupWindows",
                "firstFullAllowedBackupWindows",
                "archivalSpecs",
                "replicationSpecs",
                "numDbs",
                "numOracleDbs",
                "numFilesets",
                "numHypervVms",
                "numNutanixVms",
                "numManagedVolumes",
                "numStorageArrayVolumeGroups",
                "numWindowsVolumeGroups",
                "numLinuxHosts",
                "numShares",
                "numWindowsHosts",
                "numVms",
                "numEc2Instances",
                "numVcdVapps",
                "numProtectedObjects",
                "isDefault",
                "uiColor",
                "maxLocalRetentionLimit",
                "showAdvancedUi",
                "advancedUiConfig"]

            if archive_name is not None:
                keys_to_delete.remove("archivalSpecs")
                current_sla_details["localRetentionLimit"] = archival_threshold

            for key in keys_to_delete:

                try:
                    del current_sla_details[key]
                except KeyError:
                    pass

            if config == current_sla_details:
                return "No change required. The {} SLA Domain is already configured with the provided configuration.".format(
                    name)
            else:
                raise InvalidParameterException("The Rubrik cluster already has an SLA Domain named '{}'.".format(name))

        self.log("create_sla: Creating the new SLA")
        if v2_sla is True:
            return self.post("v2", "/sla_domain", config, timeout=timeout)
        else:
            return self.post("v1", "/sla_domain", config, timeout=timeout)

    def delete_sla(self, name, timeout=15):
        """[summary]

        Arguments:
            name {[type]} -- [description]

        Keyword Arguments:
            timeout {int} -- [description] (default: {15})

        Returns:
            [type] -- [description]
        """

        try:
            # object_id() will set sla_already_present to something besides False if the SLA is already on the cluter
            sla_id = self.object_id(name, "sla", timeout=timeout)
        except InvalidParameterException:
            return "No change required. The SLA Domain '{}' is not on the Rubrik cluster.".format(name)

        try:
            self.log("delete_sla: Attempting to delete the SLA using the v1 API")
            delete_sla = self.delete("v1", "/sla_domain/{}".format(sla_id))
        except APICallException as api_response:
            if "SLA Domains created/updated using v2 rest api version cannot be deleted from v1" in str(api_response):
                self.log(
                    "delete_sla: SLA Domains created with the v2 endpoint can not be deleted by the v1 endpoint. Attempting to delete the SLA using the v2 API")
                delete_sla = self.delete("v2", "/sla_domain/{}".format(sla_id))
            else:
                raise APICallException(api_response)

        return delete_sla

    def _time_in_range(self, start, end, point_in_time):
        """Checks if a specific datetime exists in a start and end time. For example:
        checks if a recovery point exists in the available snapshots
        
        Arguments:
            start {datetime} -- The start time of the recoverable range the database can be mounted from.
            end {datetime} -- The end time of the recoverable range the database can be mounted from. 
            point_in_time {datetime} -- The point_in_time you wish to Live Mount.

        Returns:
            bool -- True if point_in_time is in the range [start, end]."""
        
        if start <= end:
            return start <= point_in_time <= end
        else:
            return start <= point_in_time or point_in_time <= end

    def sql_live_mount(self, db_name, date, time, sql_instance=None, sql_host=None, mount_name=None, timeout=30):  # pylint: ignore
        """Live Mount a database from a specified recovery point. 

        Arguments:
            db_name {str} -- The name of the database to Live Mount.
            date {str} -- The recovery_point date you wish to Live Mount formated as `Month-Day-Year` (ex: 1-15-2014). 
            time {str} -- The recovery_point time you wish to Live Mount formated formated as `Hour:Minute AM/PM` (ex: 1:30 AM).

        Keyword Arguments:
            sql_instance {str} -- The SQL instance name with the database you wish to Live Mount.
            sql_host {str} -- The SQL Host of the database/instance to Live Mount.
            mount_name {str} -- The name given to the Live Mounted database i.e. AdventureWorks_Clone.
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {30})

        Returns:
            dict -- The full response of `POST /v1/mssql/db/{id}/mount`.
        """
        
        
        if sql_instance is None or sql_host is None or mount_name is None:
                raise InvalidParameterException(
                    "To live mount a mssql database the 'sql_instance', 'sql_host', 'mount_name' paramaters must be populated.")

        mssql_host_id = self.object_id(sql_host, 'physical_host', timeout=timeout)
        
        self.log("sql_live_mount: Getting the list of instances on host {}.".format(sql_host))
        mssql_instance = self.get(
            'v1', '/mssql/instance?primary_cluster_id=local&root_id={}'.format(mssql_host_id), timeout=timeout)

        for instance in mssql_instance['data']:
            if instance['name'] == sql_instance:
                sql_instance_id = instance['id']
                break
        else:
            raise InvalidParameterException("The SQL instance {} does not exist, please provide a valid instance".format(sql_instance))

        self.log("sql_live_mount: Getting the list of databases on the instance {}, on host {}.".format(sql_instance, sql_host))
        mssql_db = self.get('v1', '/mssql/db?primary_cluster_id=local&instance_id={}'.format(sql_instance_id), timeout=timeout)

        for db in mssql_db['data']:
            if db['name'] == db_name:
                mssql_id = db['id']
                break
        else:
            raise InvalidParameterException("The database {} does not exist, please provide a valid database".format(db_name))
        
        self.log("sql_live_mount: Getting the recoverable range for mssql db '{}'.".format(db_name))
        range_summary = self.get('v1', '/mssql/db/{}/recoverable_range'.format(mssql_id), timeout=timeout)

        self.log("sql_live_mount: Converting the provided date/time into UTC.")
        recovery_date_time = self._date_time_conversion(date, time)
        recovery_date_time = datetime.strptime(recovery_date_time, '%Y-%m-%dT%H:%M')
        recovery_timestamp = int(recovery_date_time.strftime('%s')) * 1000

        for range in range_summary['data']:
            startstr = range['beginTime']
            endstr = range['endTime']
            startsplit = startstr[:16]
            endsplit = endstr[:16]
            start = datetime.strptime(startsplit,'%Y-%m-%dT%H:%M')
            end = datetime.strptime(endsplit,'%Y-%m-%dT%H:%M')

            self.log("sql_live_mount: Searching for the provided recovery_point.")
            is_recovery_point = self._time_in_range(start, end, recovery_date_time)
            if is_recovery_point == False:
                continue
            else:
                break

        try:
            if is_recovery_point == False:
                raise InvalidParameterException("The database '{}' does not have a recovery_point taken on {} at {}.".format(db_name, date, time))
        except NameError:
            pass
        else:
            config = {}
            config['recoveryPoint'] = {'timestampMs': recovery_timestamp}
            config['mountedDatabaseName'] = mount_name
                
            self.log(
                "sql_live_mount: Live Mounting the database from recovery_point on {} at {} as database '{}'.".format(
                    date,
                    time,
                    mount_name))

            return self.post('v1', '/mssql/db/{}/mount'.format(mssql_id), config, timeout)    

    def vsphere_live_unmount(self, mounted_vm_name, force=False, timeout=30):  # pylint: ignore
        """Delete a vSphere Live Mount from the Rubrik cluster. 

        Arguments:
            mounted_vm_name {str} -- The name of the Live Mounted vSphere VM to be unmounted. 

        Keyword Arguments:
            force {bool} -- Force unmount to remove metadata when the datastore of the Live Mount virtual machine was moved off of the Rubrik cluster. (default: {False})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {30})

        Returns:
            dict -- The full response of `DELETE '/vmware/vm/snapshot/mount/{id}?force={bool}'.
        """


        self.log("vsphere_live_unmount: Searching the Rubrik cluster for the Live Mount vSphere VM '{}'.".format(mounted_vm_name))
        mounted_vm_id = self.object_id(mounted_vm_name, 'vmware', timeout=timeout)

        self.log("vsphere_live_unmount: Getting the vSphere VM mount information from the Rubrik cluster.")
        mount_summary = self.get('v1', '/vmware/vm/snapshot/mount', timeout=timeout)

        self.log("vsphere_live_unmount: Getting the mount ID of the vSphere VM '{}'.".format(mounted_vm_name))
        for mountedvm in mount_summary['data']:
            if mountedvm['mountedVmId'] == mounted_vm_id:
                mount_id = mountedvm['id']
                break
        else:
            raise InvalidParameterException("The mounted vSphere VM '{}' does not exist, please provide a valid instance".format(mounted_vm_name))

        try:
            mount_id
        except NameError:
            raise InvalidParameterException("The mounted vSphere VM '{}' does exist, please check the name you provided.".format(
                mounted_vm_name))
        else:
            self.log(
                "vsphere_live_unmount: Unmounting the vSphere VM '{}'.".format(mounted_vm_name))

            return self.delete('v1', '/vmware/vm/snapshot/mount/{}?force={}'.format(mount_id, force), timeout)

    def sql_live_unmount(self, mounted_db_name, sql_instance=None, sql_host=None, force=False, timeout=30):  # pylint: ignore
        """Delete a Microsoft SQL Live Mount from the Rubrik cluster. 

        Arguments:
            mounted_db_name {str} -- The name of the Live Mounted database to be unmounted. 

        Keyword Arguments:
            sql_instance {str} -- The name of the MSSQL instance managing the Live Mounted database to be unmounted. 
            sql_host {str} -- The name of the MSSQL host running the Live Mounted database to be unmounted. 
            force {bool} -- Remove all data within the Rubrik cluster related to the Live Mount, even if the SQL Server database cannot be contacted. (default: {False})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {30})

        Returns:
            dict -- The full response of `DELETE /mssql/db/mount/{id}?force={bool}`.
        """


        if sql_instance is None or sql_host is None:
                raise InvalidParameterException(
                    "To unmount a mssql database the 'sql_instance' and 'sql_host' paramaters must be provided.")

        mssql_host_id = self.object_id(sql_host, 'physical_host', timeout=timeout)
        
        self.log("sql_live_unmount: Getting the list of instances on host {}.".format(sql_host))
        mssql_instance = self.get(
            'v1', '/mssql/instance?primary_cluster_id=local&root_id={}'.format(mssql_host_id), timeout=timeout)

        for instance in mssql_instance['data']:
            if instance['name'] == sql_instance:
                sql_instance_id = instance['id']
                break
        else:
            raise InvalidParameterException("The mssql instance {} does not exist, please provide a valid instance".format(sql_instance))

        self.log("sql_live_unmount: Getting the list of databases on the instance {}, on host {}.".format(sql_instance, sql_host))
        mssql_db = self.get('v1', '/mssql/db?primary_cluster_id=local&instance_id={}'.format(sql_instance_id), timeout=timeout)

        for db in mssql_db['data']:
            if db['name'] == mounted_db_name:
                mounted_db_id = db['id']
                break
        else:
            raise InvalidParameterException("The database {} does not exist, please provide a valid database".format(mounted_db_name))

        self.log("sql_live_unmount: Getting the MSSQL mount information from the Rubrik cluster.")
        mount_summary = self.get('v1', '/mssql/db/mount', timeout=timeout)

        self.log("sql_live_unmount: Getting the mount ID of the mounted database '{}'.".format(mounted_db_name))
        for mounteddb in mount_summary['data']:
            if mounteddb['mountedDatabaseId'] == mounted_db_id:
                mount_id = mounteddb['id']

        try:
            mount_id
        except NameError:
            raise InvalidParameterException("A mount ID for '{}' does exist, please provide a valid Live Mounted database.".format(
                mounted_db_name))
        else:
            self.log(
                "sql_live_unmount: Unmounting the database '{}'.".format(mounted_db_name))

            return self.delete('v1', '/mssql/db/mount/{}?force={}'.format(mount_id, force), timeout)

    def get_vsphere_live_mount(self, vm_name, timeout=15):  # pylint: ignore
        """Get existing Live Mounts for a vSphere VM.

        Arguments:
            vm_name {str} -- The name of the mounted vSphere VM.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            dict -- The full response of `GET /v1/vmware/vm/snapshot/mount?vm_id={vm_id}`.
        """

        self.log("get_vsphere_live_mount: Searching the Rubrik cluster for the mounted vSphere VM '{}'.".format(vm_name))
        vm_id = self.object_id(vm_name, 'vmware', timeout=timeout)

        self.log("get_vsphere_live_mount: Getting Live Mounts of vSphere VM {}.".format(vm_name))
        return self.get('v1', '/vmware/vm/snapshot/mount?vm_id={}'.format(vm_id), timeout)
    
    def get_vsphere_live_mount_names(self, vm_name, timeout=15):  # pylint: ignore
        """Get existing Live Mount VM name(s) for a vSphere VM.

        Arguments:
            vm_name {str} -- The name of the mounted vSphere VM.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            list -- A list of the Live Mounted VM names.
        """

        self.log("get_vsphere_live_mount_names: Searching the Rubrik cluster for the mounted vSphere VM '{}'.".format(vm_name))
        vm_id = self.object_id(vm_name, 'vmware', timeout=timeout)

        self.log("get_vsphere_live_mount_names: Getting Live Mounts of vSphere VM {}.".format(vm_name))
        mounted_vm = self.get('v1', '/vmware/vm/snapshot/mount?vm_id={}'.format(vm_id), timeout)
        mounted_vm_name = []
        for vm in mounted_vm['data']:
            try:
                vm_moid = vm['mountedVmId']
                split_moid = vm_moid.split('-')
                moid = split_moid[-2]+'-'+split_moid[-1]
                self.log("get_vsphere_live_mount_names: Getting summary of VM with moid '{}'.".format(moid))
                vm_data = self.get('v1', '/vmware/vm?moid={}'.format(moid), timeout)
                mounted_vm_name.append(vm_data['data'][0]['name'])
            except KeyError:
                self.log("get_vsphere_live_mount_names: A Live Mount of vSphere VM '{}' is in progress.".format(vm_name))
                continue
        return mounted_vm_name
