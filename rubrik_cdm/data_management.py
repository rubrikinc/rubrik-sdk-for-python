
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
This module contains the Rubrik SDK Data_Management class.
"""
import re
from datetime import datetime
from .api import Api
from .exceptions import CDMVersionException, InvalidParameterException, InvalidTypeException, APICallException
import inspect


class Data_Management(Api):
    """This class contains methods related to backup and restore operations for the various objects managed by the Rubrik cluster."""

    def on_demand_snapshot(self, object_name, object_type, sla_name='current', fileset=None, host_os=None, sql_host=None, sql_instance=None, sql_db=None, hostname=None, force_full=False, share_type=None, timeout=15):  # pylint: ignore
        """Initiate an on-demand snapshot.
        Arguments:
            object_name {str} -- The name of the Rubrik object to take a on-demand snapshot of.
            object_type {str} -- The Rubrik object type you want to backup. (choices: {vmware, physical_host, ahv, mssql_db, oarcle_db})
        Keyword Arguments:
            sla_name {str} -- The SLA Domain name you want to assign the on-demand snapshot to. By default, the currently assigned SLA Domain will be used. (default: {'current'})
            fileset {str} -- The name of the Fileset you wish to backup. Only required when taking a on-demand snapshot of a physical host or share. (default: {'None'})
            host_os {str} -- The operating system for the physical host. Only required when taking a on-demand snapshot of a physical host. (default: {'None'}) (choices: {Linux, Windows})
            hostname {str} -- Required when the object_type is either oracle_db or share. When oracle_db is the object_type, this argument corresponds to the host name, or one of those host names in the cluster that the Oracle database is running. When share is the object_type this argument corresponds to the NAS server host name.
            force_full {bool} -- If True will force a new full image backup of an Oracle database. (default: {False})
            share_type {str} -- The type of NAS share i.e. NFS or SMB. Only required when taking a snapshot of a Share.
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})
        Returns:
            tuple -- When object_type is vmware, the full API response for `POST /v1/vmware/vm/{ID}/snapshot` and the job status URL which can be used to monitor progress of the snapshot. (api_response, job_status_url)
            tuple -- When object_type is physical_host, the full API response for `POST /v1/fileset/{}/snapshot` and the job status URL which can be used to monitor progress of the snapshot. (api_response, job_status_url)
        """

        self.function_name = inspect.currentframe().f_code.co_name

        valid_object_type = ['vmware', 'physical_host',
                             'ahv', 'mssql_db', 'oracle_db', 'share']
        valid_host_os_type = ['Linux', 'Windows']

        if object_type not in valid_object_type:
            raise InvalidParameterException("The on_demand_snapshot() `object_type` argument must be one of the following: {}.".format(
                valid_object_type))

        if host_os is not None:
            if host_os not in valid_host_os_type:
                raise InvalidParameterException("The on_demand_snapshot() `host_os` argument must be one of the following: {}.".format(
                    valid_host_os_type))

        if object_type == 'vmware':
            self.log("on_demand_snapshot: Searching the Rubrik cluster for the vSphere VM '{}'.".format(
                object_name))
            vm_id = self.object_id(object_name, object_type, timeout=timeout)

            if sla_name == 'current':
                self.log(
                    "on_demand_snapshot: Searching the Rubrik cluster for the SLA Domain assigned to the vSphere VM '{}'.".format(object_name))

                vm_summary = self.get(
                    'v1', '/vmware/vm/{}'.format(vm_id), timeout=timeout)
                sla_id = vm_summary['effectiveSlaDomainId']

            elif sla_name != 'current':
                self.log(
                    "on_demand_snapshot: Searching the Rubrik cluster for the SLA Domain '{}'.".format(sla_name))
                sla_id = self.object_id(sla_name, 'sla', timeout=timeout)

            config = {}
            config['slaId'] = sla_id

            self.log("on_demand_snapshot: Initiating snapshot for the vSphere VM '{}'.".format(
                object_name))
            api_request = self.post(
                'v1', '/vmware/vm/{}/snapshot'.format(vm_id), config, timeout)

            snapshot_status_url = api_request['links'][0]['href']

        elif object_type == 'ahv':

            self.log("on_demand_snapshot: Searching the Rubrik cluster for the AHV VM '{}'.".format(
                object_name))

            vm_id = self.object_id(object_name, object_type, timeout=timeout)

            if sla_name == 'current':
                self.log(
                    "on_demand_snapshot: Searching the Rubrik cluster for the SLA Domain assigned to the AHV VM '{}'.".format(object_name))

                vm_summary = self.get(
                    'internal', '/nutanix/vm/{}'.format(vm_id), timeout)
                sla_id = vm_summary['effectiveSlaDomainId']

            elif sla_name != 'current':
                self.log(
                    "on_demand_snapshot: Searching the Rubrik cluster for the SLA Domain '{}'.".format(sla_name))
                sla_id = self.object_id(sla_name, 'sla', timeout=timeout)

            config = {}
            config['slaId'] = sla_id

            self.log("on_demand_snapshot: Initiating snapshot for the AHV VM '{}'.".format(
                object_name))
            api_request = self.post(
                'internal', '/nutanix/vm/{}/snapshot'.format(vm_id), config, timeout)

            snapshot_status_url = api_request['links'][0]['href']

        elif object_type == 'mssql_db':

            self.log(
                "on_demand_snapshot: Searching the Rubrik cluster for the MS SQL '{}'.".format(object_name))

            mssql_host = self.object_id(
                sql_host, 'physical_host', timeout=timeout)

            mssql_instance = self.get(
                'v1', '/mssql/instance?primary_cluster_id=local&root_id={}'.format(mssql_host), timeout)

            for instance in mssql_instance['data']:
                if instance['name'] == sql_instance:
                    sql_db_id = instance['id']

            mssql_db = self.get(
                'v1', '/mssql/db?primary_cluster_id=local&instance_id={}'.format(sql_db_id), timeout)

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

            self.log("on_demand_snapshot: Initiating snapshot for the MS SQL '{}'.".format(
                object_name))
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

            self.log("on_demand_snapshot: Searching the Rubrik cluster for the Physical Host '{}'.".format(
                object_name))
            host_id = self.object_id(object_name, object_type, timeout=timeout)

            self.log(
                "on_demand_snapshot: Searching the Rubrik cluster for the Fileset Template '{}'.".format(fileset))
            fileset_template_id = self.object_id(
                fileset, 'fileset_template', host_os, timeout=timeout)

            self.log(
                "on_demand_snapshot: Searching the Rubrik cluster for the full Fileset.")
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
                self.log(
                    "on_demand_snapshot: Searching the Rubrik cluster for the SLA Domain '{}'.".format(sla_name))
                sla_id = self.object_id(sla_name, 'sla', timeout=timeout)

            config = {}
            config['slaId'] = sla_id

            self.log("on_demand_snapshot: Initiating snapshot for the Physical Host '{}'.".format(
                object_name))
            api_request = self.post(
                'v1', '/fileset/{}/snapshot'.format(fileset_id), config, timeout)

            snapshot_status_url = api_request['links'][0]['href']

        elif object_type == 'oracle_db':
            if hostname is None:
                raise InvalidParameterException(
                    "You must provide the host or one of the hosts in a RAC cluster for the Oracle DB object.")

            self.log(
                "on_demand_snapshot: Searching the Rubrik cluster for the Oracle database '{}' on the host '{}'.".format(
                    object_name,
                    hostname))
            db_id = self.object_id(
                object_name, object_type, hostname=hostname, timeout=timeout)

            if sla_name == 'current':
                self.log(
                    "on_demand_snapshot: Searching the Rubrik cluster for the SLA Domain assigned to the Oracle database '{}'.".format(
                        object_name))

                oracle_db_summary = self.get(
                    'internal', '/oracle/db/{}'.format(db_id), timeout)
                sla_id = oracle_db_summary['effectiveSlaDomainId']

            elif sla_name != 'current':
                self.log(
                    "on_demand_snapshot: Searching the Rubrik cluster for the SLA Domain '{}'.".format(sla_name))
                sla_id = self.object_id(sla_name, 'sla', timeout=timeout)

            config = {}
            config['slaId'] = sla_id
            config['forceFullSnapshot'] = force_full

            self.log("on_demand_snapshot: Initiating snapshot for the Oracle database '{}'.".format(
                object_name))
            api_request = self.post(
                'internal', '/oracle/db/{}/snapshot'.format(db_id), config, timeout)

            snapshot_status_url = api_request['links'][0]['href']

        elif object_type == 'share':
            if hostname is None:
                raise InvalidParameterException(
                    "The on_demand_snapshot() `hostname` argument must be populated when taking a NAS Share fileset snapshot.")
            elif fileset is None:
                raise InvalidParameterException(
                    "The on_demand_snapshot() `fileset` argument must be populated when taking a NAS Share fileset snapshot.")
            elif share_type is None:
                raise InvalidParameterException(
                    "The on_demand_snapshot() `share_type` argument must be populated when taking a NAS Share fileset snapshot.")

            self.log(
                "on_demand_snapshot: Searching the Rubrik cluster for the NAS Host '{}'.".format(hostname))
            host_id = self.object_id(
                hostname, 'physical_host', timeout=timeout)

            self.log("on_demand_snapshot: Searching the Rubrik cluster for the NAS share '{}'.".format(
                object_name))
            share_id = self.object_id(
                object_name, 'share', hostname=hostname, share_type=share_type, timeout=timeout)

            self.log(
                "on_demand_snapshot: Searching the Rubrik cluster for the full Fileset.")
            api_endpoint = '/fileset?share_id={}&host_id={}&is_relic=false&name={}'.format(
                share_id, host_id, fileset)
            fileset_summary = self.get('v1', api_endpoint, timeout=timeout)

            if fileset_summary['total'] == 0:
                raise InvalidParameterException(
                    "The NAS Share '{}' is not assigned to the '{}' Fileset.".format(
                        object_name, fileset))

            fileset_id = fileset_summary['data'][0]['id']

            if sla_name == 'current':
                sla_id = fileset_summary['data'][0]['effectiveSlaDomainId']
            elif sla_name != 'current':
                self.log(
                    "on_demand_snapshot: Searching the Rubrik cluster for the SLA Domain '{}'.".format(sla_name))
                sla_id = self.object_id(sla_name, 'sla', timeout=timeout)

            config = {}
            config['slaId'] = sla_id

            self.log(
                "on_demand_snapshot: Initiating snapshot for the NAS Share '{}' Fileset '{}'.".format(
                    object_name, fileset))
            api_request = self.post(
                'v1', '/fileset/{}/snapshot'.format(fileset_id), config, timeout)

            snapshot_status_url = api_request['links'][0]['href']

        return (api_request, snapshot_status_url)

    def object_id(self, object_name, object_type, host_os=None, hostname=None, share_type=None, mssql_host=None, mssql_instance=None, timeout=15):
        """Get the ID of a Rubrik object by providing its name.
        Arguments:
            object_name {str} -- The name of the Rubrik object whose ID you wish to lookup.
            object_type {str} -- The object type you wish to look up. (choices: {vmware, sla, vmware_host, physical_host, fileset_template, managed_volume, mssql_db, mssql_instance, mssql_availability_group, vcenter, ahv, aws_native, oracle_db, oracle_host, volume_group, archival_location, share, organization, organization_role_id, organization_admin_role})
        Keyword Arguments:
            host_os {str} -- The operating system for the host. Required when object_type is 'fileset_template'. (default: {None}) (choices: {Windows, Linux})
            hostname {str} -- The Oracle hostname, Oracle RAC cluster name, or one of the hostnames in the Oracle RAC cluster. Required when the object_type is oracle_db or share. Using the IP is not supported.
            share_type {str} -- The type of NAS share i.e. NFS or SMB
            mssql_host {str} -- The name of a MSSQL Host. Required when the object_type is mssql_db or mssql_instance.
            mssql_instance {str} -- The name of a MSSQL database instance. Required when the object_type is mssql_db.
            timeout {int} -- The number of seconds to wait to establish a connection with the Rubrik cluster before returning a timeout error. (default: {15})
        Returns:
            str -- The ID of the provided Rubrik object.
        """

        if self.function_name == "":
            self.function_name = inspect.currentframe().f_code.co_name

        valid_object_type = [
            'vmware',
            'sla',
            'vmware_host',
            'physical_host',
            'fileset_template',
            'managed_volume',
            'mssql_db',
            'mssql_instance',
            'mssql_availability_group',
            'vcenter',
            'ahv',
            'aws_native',
            'oracle_db',
            'oracle_host',
            'volume_group',
            'archival_location',
            'share',
            'organization',
            'organization_role_id',
            'organization_admin_role']

        if object_type not in valid_object_type:
            raise InvalidParameterException("The object_id() object_type argument must be one of the following: {}.".format(
                valid_object_type))

        if object_type == 'fileset_template':
            if host_os is None:
                raise InvalidParameterException(
                    "You must provide the Fileset Template OS type.")
            elif host_os not in ['Linux', 'Windows']:
                raise InvalidParameterException(
                    "The host_os must be either 'Linux' or 'Windows'.")

        if object_type == 'sla':
            if object_name.upper() == "FOREVER" or object_name.upper() == "UNPROTECTED":
                return "UNPROTECTED"

        if object_type == 'oracle_db':
            if hostname is None:
                raise InvalidParameterException(
                    "You must provide the hostname, the RAC cluster name, or one of the hosts in the RAC cluster for the Oracle DB object.")
            # Regular expression to test for an IP Address.
            regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
                                        25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
                                        25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
                                        25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'''
            # Check to make sure the hostname is not an IP address.
            if re.search(regex, hostname):
                raise InvalidParameterException(
                    "You must provide the hostname, RAC cluster name or one of the hosts in a RAC cluster for the Oracle DB object. Using an IP address is not supported.")
            # Remove the domain name if present. Hostnames may be stored with and without domain names. Using just the hostname for a consistent match.
            hostname = hostname.split('.')[0]

        if object_type == 'share':
            if hostname is None:
                raise InvalidParameterException(
                    "You must provide the 'hostname' with the NAS share object.")

            if share_type is None:
                raise InvalidParameterException(
                    "You must provide the 'share_type' with the NAS share object.")
            else:
                self.log('Searching the Rubrik cluster for the host ID.')
                host_id = self.object_id(
                    hostname, 'physical_host', timeout=timeout)

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
            "aws_native": {
                "api_version": "internal",
                "api_endpoint": "/aws/account?name={}".format(object_name)
            },
            "vcenter": {
                "api_version": "v1",
                "api_endpoint": "/vmware/vcenter?primary_cluster_id=local"
            },
            "oracle_db": {
                "api_version": "internal",
                "api_endpoint": "/oracle/db?name={}".format(object_name)
            },
            "oracle_host": {
                "api_version": "internal",
                "api_endpoint": "/oracle/hierarchy/root/children?name={}".format(object_name)
            },
            "volume_group": {
                "api_version": "internal",
                "api_endpoint": "/volume_group?is_relic=false"
            },
            "archival_location": {
                "api_version": "internal",
                "api_endpoint": "/archive/location?name={}".format(object_name)
            },
            "share": {
                "api_version": "internal",
                "api_endpoint": "/host/share?share_type={}".format(share_type)
            },
            "organization": {
                "api_version": "internal",
                "api_endpoint": "/organization?name={}".format(object_name)
            },
            "organization_role_id": {
                "api_version": "internal",
                "api_endpoint": "/organization?name={}".format(object_name)
            },
            "mssql_availability_group": {
                "api_version": "v1",
                "api_endpoint": "/mssql/hierarchy/root/children?has_instances=false&is_clustered=false&is_live_mount=false&limit=51&object_type=MssqlAvailabilityGroup&offset=0&primary_cluster_id=local&snappable_status=Protectable&name={}".format(object_name)
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

        if object_type == 'mssql_instance':
            if mssql_host is None:
                raise InvalidParameterException(
                    "You must provide a mssql_host when the object_type is mssql_instance.")
            # root_id is host_id in SQL speak
            root_id = self.object_id(mssql_host, 'physical_host')

            api_call["mssql_instance"] = {
                "api_version": "v1",
                "api_endpoint": "/mssql/instance?primary_cluster_id=local&root_id={}".format(root_id)
            }

        if object_type == 'mssql_db':
            if mssql_instance is None or mssql_host is None:
                raise InvalidParameterException(
                    "You must provide a mssql_host and mssql_instance when the object_type is mssql_db.")

            instance_id = self.object_id(
                mssql_instance, "mssql_instance", mssql_host=mssql_host)

            api_call["mssql_db"] = {
                "api_version": "v1",
                "api_endpoint": "/mssql/db?primary_cluster_id=local&is_relic=false&name={}&instance_id={}".format(object_name, instance_id)
            }

        # When looking up the org_admin_role the user should provide the org name
        # as the object_name. We then use that to look up the id for the org and
        # then set that as the "object_type" for the full org_admin_role query
        if object_type == "organization_admin_role":
            self.log(
                "object_id: Getting the ID for the {} organization.".format(object_name))
            org_role_id = self.object_id(
                object_name, "organization_role_id", timeout=timeout)

            api_call["organization_admin_role"] = {
                "api_version": "internal",
                "api_endpoint": "/role/{}/authorization".format(org_role_id)
            }

        self.log("object_id: Getting the object id for the {} object '{}'.".format(
            object_type, object_name))

        api_request = self.get(
            api_call[object_type]["api_version"],
            api_call[object_type]["api_endpoint"],
            timeout=timeout)

        object_ids = []

        if object_type == "organization_admin_role":
            object_ids.append(api_request["roleId"])
        else:

            if api_request['total'] == 0:
                raise InvalidParameterException("The {} object '{}' was not found on the Rubrik cluster.".format(
                    object_type, object_name))
            elif api_request['total'] > 0:
                # Define the "object name" to search for
                if object_type == 'physical_host':
                    name_value = filter_field_name
                elif object_type == "volume_group":
                    name_value = "hostname"
                elif object_type == 'share':
                    name_value = "exportPoint"
                else:
                    name_value = 'name'

                for item in api_request['data']:
                    if object_type == 'oracle_db':
                        if 'standaloneHostName' in item.keys():
                            if hostname == item['standaloneHostName'].split('.')[0]:
                                object_ids.append(item['id'])
                                break
                        elif 'racName' in item.keys():
                            if hostname == item['racName']:
                                object_ids.append(item['id'])
                                break
                            if any(instance['hostName'] == hostname for instance in item['instances']):
                                object_ids.append(item['id'])
                                break
                    elif object_type == 'share' and item[name_value] == object_name:
                        if item['hostId'] == host_id:
                            object_ids.append(item['id'])
                    elif object_type == "organization_role_id" and item[name_value].lower():
                        object_ids.append(item['roleId'])

                    elif item[name_value].lower() == object_name.lower():
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

    def assign_sla(self, object_name, sla_name, object_type, log_backup_frequency_in_seconds=None, log_retention_hours=None, copy_only=None, windows_host=None, nas_host=None, share=None, log_backup_frequency_in_minutes=None, num_channels=4, hostname=None, timeout=30):  # pytest: ignore
        """Assign a Rubrik object to an SLA Domain.
        Arguments:
            object_name {str or list} -- The name of the Rubrik object you wish to assign to an SLA Domain. When the 'object_type' is 'volume_group', the object_name can be a list of volumes.
            sla_name {str} -- The name of the SLA Domain you wish to assign an object to. To exclude the object from all SLA assignments use `do not protect` as the `sla_name`. To assign the selected object to the SLA of the next higher level object use `clear` as the `sla_name`.
            object_type {str} -- The Rubrik object type you want to assign to the SLA Domain. (choices: {ahv, mssql_host, oracle_host, vmware, volume_group})
        Keyword Arguments:
            log_backup_frequency_in_seconds {int} -- The MSSQL Log Backup frequency you'd like to specify with the SLA. Required when the `object_type` is `mssql_host`. (default {None})
            log_retention_hours {int} -- The MSSQL or Oracle Log Retention frequency you'd like to specify with the SLA. Required when the `object_type` is `mssql_host`, `oracle_db` or 'oracle_host'. (default {None})
            copy_only {bool} -- Take Copy Only Backups with MSSQL. Required when the `object_type` is `mssql_host`. (default {None})
            windows_host {str} -- The name of the Windows host that contains the relevant volume group. Required when the `object_type` is `volume_group`. (default {None})
            nas_host {str} -- The name of the NAS host that contains the relevant share. Required when the `object_type` is `fileset`. (default {None})
            share {str} -- The name of the network share a fileset will be created for. Required when the `object_type` is `fileset`. (default {None})
            log_backup_frequency_in_minutes {int} - The Oracle Log Backup frequency you'd like to specify with the SLA. Required when the `object_type` is `oracle_db` or `oracle_host`. (default {None})
            num_channels {int} - Number of RMAN channels used to backup the Oracle database. Required when the `object_type` is `oracle_host`. (default {"4""})
            hostname {str} -- The hostname, or one of the hostnames in a RAC cluster, or the RAC cluster name. Required when the object_type is `oracle_db`. (default {None})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {30})
        Returns:
            str -- No change required. The vSphere VM '`object_name`' is already assigned to the '`sla_name`' SLA Domain.
            str -- No change required. The MSSQL Instance '`object_name`' is already assigned to the '`sla_name`' SLA Domain with the following log settings: log_backup_frequency_in_seconds: `log_backup_frequency_in_seconds`, log_retention_hours: `log_retention_hours` and copy_only: `copy_only`
            str -- No change required. The Oracle Database '`object_name`' is already assigned to the '`sla_name`' SLA Domain with the following log settings: log_backup_frequency_in_minutes: `log_backup_frequency_in_seconds`, log_retention_hours: `log_retention_hours` and num_channels: `num_channels`.
            str -- No change required. The Oracle Host '`object_name`' is already assigned to the '`sla_name`' SLA Domain with the following log settings: log_backup_frequency_in_seconds: `log_backup_frequency_in_seconds`. log_retention_hours: `log_retention_hours`, and num_channels: `num_channels`
            str -- No change required. The '`object_name`' volume_group is already assigned to the '`sla_name`' SLA Domain.
            dict -- The full API response for `POST /internal/sla_domain/{sla_id}/assign`.
            dict -- The full API response for `PATCH /internal/volume_group/{id}`.
            dict -- The full API response for `PATCH /internal/oracle/db/{id}.`
            dict -- The full API response for `PATCH /internal/oracle/host/{id}`.
        """

        self.function_name = inspect.currentframe().f_code.co_name

        valid_object_type = ['vmware', 'mssql_host', 'volume_group',
                             'fileset', 'ahv', 'oracle_db', 'oracle_host']

        if object_type not in valid_object_type:
            raise InvalidParameterException(
                "The assign_sla() object_type argument must be one of the following: {}.".format(valid_object_type))

        if object_type == "mssql_host":
            if log_backup_frequency_in_seconds is None or log_retention_hours is None or copy_only is None:
                raise InvalidParameterException(
                    "When the object_type is 'mssql_host' the 'log_backup_frequency_in_seconds', 'log_retention_hours', 'copy_only' paramaters must be populated.")

        if object_type == "oracle_host":
            if log_backup_frequency_in_minutes is None or log_retention_hours is None or num_channels is None:
                raise InvalidParameterException(
                    "When the object_type is 'oracle_host' the 'log_backup_frequency_in_minutes', 'log_retention_hours', 'num_channels' paramaters must be populated.")

        if object_type == "oracle_db":
            if log_backup_frequency_in_minutes is None or log_retention_hours is None or num_channels is None or hostname is None:
                raise InvalidParameterException(
                    "When the object_type is 'oracle_db' the 'log_backup_frequency_in_minutes', 'log_retention_hours', 'num_channels' and 'hostname' paramaters must be populated.")

        if object_type == "fileset":
            if nas_host is None or share is None:
                raise InvalidParameterException(
                    "When the object_type is 'fileset' the 'nas_host' and 'share' paramaters must be populated.")

        if object_type == "volume_group":

            if not isinstance(object_name, (str, list)):
                raise InvalidParameterException(
                    "When the object_type is 'volume_group', the 'object_name' must be a string or a list.")

            if windows_host is None:
                raise InvalidParameterException(
                    "When the object_type is 'volumge_group' the 'windows_host' paramater must be populated.")
        else:
            if not isinstance(object_name, (str)):
                raise InvalidParameterException(
                    "The object_name must be a string.")

        # Determine if 'do not protect' or 'clear' are the SLA Domain Name
        do_not_protect_regex = re.findall(
            '\\bdo not protect\\b', sla_name, flags=re.IGNORECASE)
        clear_regex = re.findall('\\bclear\\b', sla_name, flags=re.IGNORECASE)

        if len(do_not_protect_regex) > 0:
            sla_id = "UNPROTECTED"
        elif len(clear_regex) > 0:
            sla_id = 'INHERIT'
        else:
            self.log(
                "assign_sla: Searching the Rubrik cluster for the SLA Domain '{}'.".format(sla_name))
            sla_id = self.object_id(sla_name, 'sla', timeout=timeout)

        if object_type == 'vmware':
            self.log("assign_sla: Searching the Rubrik cluster for the vSphere VM '{}'.".format(
                object_name))
            vm_id = self.object_id(object_name, object_type, timeout=timeout)

            self.log("assign_sla: Determing the SLA Domain currently assigned to the vSphere VM '{}'.".format(
                object_name))
            vm_summary = self.get(
                'v1', '/vmware/vm/{}'.format(vm_id), timeout=timeout)

            if sla_id == vm_summary['configuredSlaDomainId']:
                return "No change required. The vSphere VM '{}' is already assigned to the '{}' SLA Domain.".format(
                    object_name, sla_name)
            else:
                self.log("assign_sla: Assigning the vSphere VM '{}' to the '{}' SLA Domain.".format(
                    object_name, sla_name))

                config = {}
                config['managedIds'] = [vm_id]

                return self.post("internal", "/sla_domain/{}/assign".format(sla_id), config, timeout)

        elif object_type == 'fileset':
            self.log(
                "assign_sla: Searching the Rubrik cluster for the NAS host '{}'.".format(nas_host))
            host_id = self.object_id(
                nas_host, 'physical_host', timeout=timeout)

            self.log(
                "assign_sla: Searching the Rubrik cluster for the share '{}'.".format(share))
            share_summary = self.get(
                "internal", '/host/share', timeout=timeout)
            share_id = None
            for shares in share_summary['data']:
                if shares['hostId'] == host_id and shares['exportPoint'] == share:
                    share_id = shares['id']
            if share_id is None:
                raise InvalidParameterException(
                    "The share object'{}' does not exist for host '{}'.".format(
                        share, nas_host))

            self.log("assign_sla: Searching the Rubrik cluster for the fileset '{}' template.".format(
                object_name))
            fileset_summary = self.get(
                "v1", '/fileset?is_relic=false&name={}'.format(object_name), timeout=timeout)
            template_id = None
            for filesets in fileset_summary['data']:
                if filesets['hostId'] == host_id and filesets['name'] == object_name:
                    template_id = filesets['templateId']
            if template_id is None:
                raise InvalidParameterException(
                    "The fileset '{}' template does not exist".format(object_name))

            self.log(
                "assign_sla: Creating filesets for a network host. Each fileset is a fileset template applied to a host")
            bulk = [{
                'isPassthrough': False,
                'shareId': share_id,
                'templateId': template_id
            }]
            fileset_response = self.post(
                "internal", "/fileset/bulk", bulk, timeout)
            fileset_id = fileset_response['data'][0]['id']

            if sla_id == fileset_summary['data'][0]['configuredSlaDomainId']:
                return "No change required. The NAS fileset '{}' is already assigned to the '{}' SLA Domain.".format(
                    object_name, sla_name)

            else:
                self.log("assign_sla: Assigning the fileset '{}' to the '{}' SLA Domain.".format(
                    object_name, sla_name))

                config = {}
                config['managedIds'] = [fileset_id]

                return self.post("internal", "/sla_domain/{}/assign".format(sla_id), config, timeout=180)

        elif object_type == 'ahv':
            self.log("assign_sla: Searching the Rubrik cluster for the AHV VM '{}'.".format(
                object_name))
            vm_id = self.object_id(object_name, object_type, timeout=timeout)

            self.log("assign_sla: Determing the SLA Domain currently assigned to the AHV VM '{}'.".format(
                object_name))
            vm_summary = self.get(
                'internal', '/nutanix/vm/{}'.format(vm_id), timeout=timeout)

            if sla_id == vm_summary['configuredSlaDomainId']:
                return "No change required. The AHV VM '{}' is already assigned to the '{}' SLA Domain.".format(
                    object_name, sla_name)
            else:
                self.log("assign_sla: Assigning the AHV VM '{}' to the '{}' SLA Domain.".format(
                    object_name, sla_name))

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
                self.log("assign_sla: Searching the Rubrik cluster for the MSSQL Instance '{}'.".format(
                    object_name))
                mssql_instances = self.get(
                    'v1', '/mssql/instance?root_id={}'.format(host_id), timeout=timeout)

                for mssql_instance in mssql_instances['data']:
                    mssql_id = mssql_instance['id']
                    mssql_instance_name = mssql_instance['name']

                    self.log(
                        "assign_sla: Determing the SLA Domain currently assigned to the MSSQL Instance '{}'.".format(mssql_instance_name))

                    mssql_summary = self.get(
                        'v1', '/mssql/instance/{}'.format(mssql_id), timeout=timeout)

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

                        patch_resp = self.patch(
                            "v1", "/mssql/instance/{}".format(mssql_id), config, timeout)
                        db_sla_lst.append(patch_resp)
            else:
                raise InvalidParameterException(
                    "Host ID not found for instance '{}'".format(object_name))

            return db_sla_lst

        elif object_type == 'oracle_db':

            oracle_db_id = ''

            self.log(
                'Searching the Rubrik cluster for the current Oracle databases.')
            oracle_db_id = self.object_id(
                object_name, object_type, hostname=hostname)

            if(oracle_db_id):
                self.log(
                    "assign_sla: Determing the SLA Domain currently assigned to the Oracle Database '{}'.".format(object_name))

                oracle_summary = self.get(
                    'internal',
                    '/oracle/db/{}'.format(oracle_db_id),
                    timeout=timeout)

                if (sla_id == oracle_summary['configuredSlaDomainId'] and log_backup_frequency_in_minutes == oracle_summary['logBackupFrequencyInMinutes'] and
                        log_retention_hours == oracle_summary['logRetentionHours'] and num_channels == oracle_summary['numChannels']):
                    return "No change required. The Oracle Database '{}' is already assigned to the '{}' SLA Domain with the following log settings:" \
                        " log_backup_frequency_in_minutes: {}, log_retention_hours: {} and num_channels: {}.".format(
                            object_name, sla_name, log_backup_frequency_in_minutes, log_retention_hours, num_channels)

                else:
                    self.log(
                        "assign_sla: Assigning the Oracle Database '{}' to the '{}' SLA Domain.".format(
                            object_name, sla_name))

                    config = {}
                    if log_backup_frequency_in_minutes is not None:
                        config['logBackupFrequencyInMinutes'] = log_backup_frequency_in_minutes
                    if log_retention_hours is not None:
                        config['logRetentionHours'] = log_retention_hours
                    if num_channels is not None:
                        config['numChannels'] = num_channels

                    config['configuredSlaDomainId'] = sla_id

                    patch_resp = self.patch(
                        "internal", "/oracle/db/{}".format(oracle_db_id), config, timeout)
            else:
                raise InvalidParameterException(
                    "Database ID not found for instance '{}'".format(object_name))

            return patch_resp

        elif object_type == 'oracle_host':

            host_id = ''

            self.log('Searching the Rubrik cluster for the current Oracle hosts.')
            host_id = self.object_id(object_name, object_type)

            if(host_id):
                self.log(
                    "assign_sla: Determing the SLA Domain currently assigned to the Oracle Host '{}'.".format(object_name))

                oracle_summary = self.get(
                    'internal',
                    '/oracle/host/{}'.format(host_id),
                    timeout=timeout)

                if (sla_id == oracle_summary['configuredSlaDomainId'] and log_backup_frequency_in_minutes == oracle_summary['logBackupFrequencyInMinutes'] and
                        log_retention_hours == oracle_summary['logRetentionHours'] and num_channels == oracle_summary['numChannels']):
                    return "No change required. The Oracle Host '{}' is already assigned to the '{}' SLA Domain with the following log settings:" \
                        " log_backup_frequency_in_minutes: {}, log_retention_hours: {} and num_channels: {}.".format(
                            object_name, sla_name, log_backup_frequency_in_minutes, log_retention_hours, num_channels)

                else:
                    self.log(
                        "assign_sla: Assigning the Oracle Host '{}' to the '{}' SLA Domain.".format(
                            object_name, sla_name))

                    config = {}
                    if log_backup_frequency_in_minutes is not None:
                        config['logBackupFrequencyInMinutes'] = log_backup_frequency_in_minutes
                    if log_retention_hours is not None:
                        config['logRetentionHours'] = log_retention_hours
                    if num_channels is not None:
                        config['numChannels'] = num_channels

                    config['configuredSlaDomainId'] = sla_id

                    patch_resp = self.patch(
                        "internal", "/oracle/host/{}".format(host_id), config, timeout)
            else:
                raise InvalidParameterException(
                    "Host ID not found for instance '{}'".format(object_name))

            return patch_resp

        elif object_type == "volume_group":

            volume_group_id = self.object_id(
                windows_host, "volume_group", timeout=timeout)
            physical_host_id = self.object_id(
                windows_host, "physical_host", host_os="windows", timeout=timeout)

            self.log("assign_sla: Getting a list of all volumes on the '{}' Windows host.".format(
                windows_host))
            host_volumes = self.get(
                "internal", "/host/{}/volume".format(physical_host_id), timeout=timeout)

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

            self.log(
                "assign_sla: Getting details of the current volume group on the Windows host.")
            volume_group_details = self.get(
                "internal", "/volume_group/{}".format(volume_group_id), timeout=timeout)

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
                self.log("assign_sla: Assigning the vSphere VM '{}' to the '{}' SLA Domain.".format(
                    object_name, sla_name))
                return self.patch("internal", "/volume_group/{}".format(volume_group_id), config, timeout=timeout)

    def vsphere_live_mount(self, vm_name, date='latest', time='latest', host='current', remove_network_devices=False, power_on=True, timeout=15):  # pylint: ignore
        """Live Mount a vSphere VM from a specified snapshot. If a specific date and time is not provided, the last snapshot taken will be used.
        Arguments:
            vm_name {str} -- The name of the vSphere VM to Live Mount.
        Keyword Arguments:
            date {str} -- The date of the snapshot you wish to Live Mount formated as `Month-Day-Year` (ex: 1-15-2014). If `latest` is specified, the last snapshot taken will be used. (default: {'latest'})
            time {str} -- The time of the snapshot you wish to Live Mount formated as `Hour:Minute AM/PM` (ex: 1:30 AM). If `latest` is specified, the last snapshot taken will be used. (default: {'latest'})
            host {str} -- The hostname or IP address of the ESXi host to Live Mount the VM on. By default, the current host will be used. (default: {'current'})
            remove_network_devices {bool} -- Flag that determines whether to remove the network interfaces from the Live Mounted VM. Set to `True` to remove all network interfaces. (default: {False})
            power_on {bool} -- Flag that determines whether the VM should be powered on after the Live Mount. Set to `True` to power on the VM. Set to `False` to mount the VM but not power it on. (default: {True})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})
        Returns:
            dict -- The full response of `POST /v1/vmware/vm/snapshot/{snapshot_id}/mount`.
        """

        self.function_name = inspect.currentframe().f_code.co_name

        if isinstance(remove_network_devices, bool) is False:
            raise InvalidTypeException(
                "The 'remove_network_devices' argument must be True or False.")
        elif isinstance(power_on, bool) is False:
            raise InvalidTypeException(
                "The 'power_on' argument must be True or False.")
        elif date != 'latest' and time == 'latest' or date == 'latest' and time != 'latest':
            raise InvalidParameterException(
                "The date and time arguments most both be 'latest' or a specific date and time.")

        self.log(
            "vsphere_live_mount: Searching the Rubrik cluster for the vSphere VM '{}'.".format(vm_name))
        vm_id = self.object_id(vm_name, 'vmware', timeout=timeout)

        self.log(
            "vsphere_live_mount: Getting a list of all Snapshots for vSphere VM '{}'.".format(vm_name))
        vm_summary = self.get(
            'v1', '/vmware/vm/{}'.format(vm_id), timeout=timeout)

        if date == 'latest' and time == 'latest':
            number_of_snapshots = len(vm_summary['snapshots'])
            snapshot_id = vm_summary['snapshots'][number_of_snapshots - 1]['id']
        else:
            self.log(
                "vsphere_live_mount: Converting the provided date/time into UTC.")
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
            time {str} -- The time of the snapshot you wish to Instantly Recover formated as `Hour:Minute AM/PM`  (ex: 1:30 AM). If 'latest' is specified, the last snapshot taken will be used. (default: {'latest'})
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

        self.function_name = inspect.currentframe().f_code.co_name

        if isinstance(remove_network_devices, bool) is False:
            raise InvalidTypeException(
                "The 'remove_network_devices' argument must be True or False.")
        elif isinstance(power_on, bool) is False:
            raise InvalidTypeException(
                "The 'power_on' argument must be True or False.")
        elif isinstance(disable_network, bool) is False:
            raise InvalidTypeException(
                "The 'disable_network' argument must be True or False.")
        elif isinstance(keep_mac_addresses, bool) is False:
            raise InvalidTypeException(
                "The 'keep_mac_addresses' argument must be True or False.")
        elif isinstance(preserve_moid, bool) is False:
            raise InvalidTypeException(
                "The 'preserve_moid' argument must be True or False.")
        elif date != 'latest' and time == 'latest' or date == 'latest' and time != 'latest':
            raise InvalidParameterException(
                "The date and time arguments most both be 'latest' or a specific date and time.")

        self.log(
            "vsphere_instant_recovery: Searching the Rubrik cluster for the vSphere VM '{}'.".format(vm_name))
        vm_id = self.object_id(vm_name, 'vmware', timeout=timeout)

        self.log(
            "vsphere_instant_recovery: Getting a list of all Snapshots for vSphere VM '{}'.".format(vm_name))
        vm_summary = self.get(
            'v1', '/vmware/vm/{}'.format(vm_id), timeout=timeout)

        if date == 'latest' and time == 'latest':
            number_of_snapshots = len(vm_summary['snapshots'])
            snapshot_id = vm_summary['snapshots'][number_of_snapshots - 1]['id']
        else:
            self.log(
                "vsphere_instant_recovery: Converting the provided date/time into UTC.")
            snapshot_date_time = self._date_time_conversion(date, time)

            current_snapshots = {}
            for snapshot in vm_summary['snapshots']:
                current_snapshots[snapshot['id']] = snapshot['date']

            self.log(
                "vsphere_instant_recovery: Searching for the provided snapshot.")
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

        if self.function_name == "":
            self.function_name = inspect.currentframe().f_code.co_name

        from datetime import datetime
        import pytz

        # Validate the Date formating
        try:
            datetime.strptime(date, '%m-%d-%Y')
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

        self.log(
            "_date_time_conversion: Converting the provided time to the 24-hour clock.")
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

        self.function_name = inspect.currentframe().f_code.co_name

        valid_object_type = ['vmware']

        if object_type not in valid_object_type:
            raise InvalidParameterException("The pause_snapshots() object_type argument must be one of the following: {}.".format(
                valid_object_type))

        if object_type == 'vmware':

            self.log("pause_snapshots: Searching the Rubrik cluster for the vSphere VM '{}'.".format(
                object_name))
            vm_id = self.object_id(object_name, object_type, timeout=timeout)

            self.log("pause_snapshots: Determing the current pause state of the vSphere VM '{}'.".format(
                object_name))
            api_request = self.get(
                'v1', '/vmware/vm/{}'.format(vm_id), timeout=timeout)

            if api_request['blackoutWindowStatus']['isSnappableBlackoutActive']:
                return "No change required. The {} VM '{}' is already paused.".format(object_type, object_name)
            else:
                self.log("pause_snapshots: Pausing Snaphots for the vSphere VM '{}'.".format(
                    object_name))
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

        self.function_name = inspect.currentframe().f_code.co_name

        valid_object_type = ['vmware']

        if object_type not in valid_object_type:
            raise InvalidParameterException("The resume_snapshots() object_type argument must be one of the following: {}.".format(
                valid_object_type))

        if object_type == 'vmware':

            self.log("resume_snapshots: Searching the Rubrik cluster for the vSphere VM '{}'.".format(
                object_name))
            vm_id = self.object_id(object_name, object_type, timeout=timeout)

            self.log("resume_snapshots: Determing the current pause state of the vSphere VM '{}'.".format(
                object_name))
            api_request = self.get(
                'v1', '/vmware/vm/{}'.format(vm_id), timeout=timeout)

            if not api_request['blackoutWindowStatus']['isSnappableBlackoutActive']:
                return "No change required. The '{}' object '{}' is currently not paused.".format(
                    object_type, object_name)
            else:
                self.log("resume_snapshots: Resuming Snaphots for the vSphere VM '{}'.".format(
                    object_name))
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

        self.function_name = inspect.currentframe().f_code.co_name

        self.log(
            "begin_managed_volume_snapshot: Searching the Rubrik cluster for the Managed Volume '{}'.".format(name))
        managed_volume_id = self.object_id(
            name, 'managed_volume', timeout=timeout)

        self.log(
            "begin_managed_volume_snapshot: Determing the state of the Managed Volume '{}'.".format(name))
        managed_volume_summary = self.get(
            'internal', '/managed_volume/{}'.format(managed_volume_id), timeout=timeout)

        if not managed_volume_summary['isWritable']:
            self.log(
                "begin_managed_volume_snapshot: Setting the Managed Volume '{}' to a writeable state.".format(name))
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

        self.function_name = inspect.currentframe().f_code.co_name

        self.log(
            "end_managed_volume_snapshot: Searching the Rubrik cluster for the Managed Volume '{}'.".format(name))
        managed_volume_id = self.object_id(
            name, 'managed_volume', timeout=timeout)

        self.log(
            "end_managed_volume_snapshot: Determing the state of the Managed Volume '{}'.".format(name))
        managed_volume_summary = self.get(
            "internal", "/managed_volume/{}".format(managed_volume_id), timeout=timeout)

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
            self.log(
                "end_managed_volume_snapshot: Searching the Rubrik cluster for the SLA Domain '{}'.".format(sla_name))
            sla_id = self.object_id(sla_name, 'sla', timeout=timeout)

            config = {}
            config['retentionConfig'] = {}
            config['retentionConfig']['slaId'] = sla_id

        return self.post("internal", "/managed_volume/{}/end_snapshot".format(managed_volume_id), config, timeout)

    def get_sla_objects(self, sla, object_type, timeout=15):
        """Retrieve the name and ID of a specific object type.
        Arguments:
            sla {str} -- The name of the SLA Domain you wish to search.
            object_type {str} -- The object type you wish to search the SLA for. (choices: {vmware, hyper-v, mssql_db, ec2_instance, oracle_db, vcd, managed_volume, ahv, nas_share, linux_and_unix_host, windows_host})
        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster. (default: {15})
        Returns:
            dict -- The `name:id` of each object in the provided SLA Domain.
        """

        if self.function_name == "":
            self.function_name = inspect.currentframe().f_code.co_name

        valid_object_type = ['vmware', 'hyper-v',
                             'mssql_db', 'ec2_instance', 'oracle_db', 'vcd', 'managed_volume', 'ahv', 'nas_share', 'linux_and_unix_host', 'windows_host']

        if object_type not in valid_object_type:
            raise InvalidParameterException(
                "The get_sla_object() object_type argument must be one of the following: {}.".format(valid_object_type))

        sla_id = self.object_id(sla, "sla", timeout=timeout)
        vm_name_id = {}

        if object_type == "nas_share":
            # The REST API does not have an easy way to filter by SLA so we will use the GQL call
            operation_name = "NasAssignedSLA"

            query = """
             NasAssignedSLA($effectiveSlaDomainId: String) {
                nasShareConnection(effectiveSlaDomainId: $effectiveSlaDomainId) {
                    nodes {
                    id
                    hostname

                    }
                }
                }
            """

            variables = {
                "effectiveSlaDomainId": sla_id
            }

            all_vms_in_sla = self.query(query, operation_name, variables)

            for vm in all_vms_in_sla["nasShareConnection"]["nodes"]:
                vm_name_id[vm["hostname"]] = vm["id"]

        elif object_type == "linux_and_unix_host" or object_type == "windows_host":
            # The REST API does not have an easy way to filter by SLA so we will use the GQL call
            operation_name = "PhysicalHostSLA"

            query = """
             PhysicalHostSLA($effectiveSlaDomainId: String, $operatingSystemType: String, $status: String) {
                hostConnection(effectiveSlaDomainId: $effectiveSlaDomainId, operatingSystemType: $operatingSystemType,  status: $status) {
                    nodes {
                    id
                    hostname
                    }
                }
                }
            """

            if object_type == "linux_and_unix_host":
                operatingSystemType = "UnixLike"
            else:
                operatingSystemType = "Windows"

            variables = {
                "status": "Connected",
                "effectiveSlaDomainId": sla_id,
                "operatingSystemType": operatingSystemType,

            }

            all_vms_in_sla = self.query(query, operation_name, variables)

            for vm in all_vms_in_sla["hostConnection"]["nodes"]:
                vm_name_id[vm["hostname"]] = vm["id"]

        else:

            api_call = {
                "vmware": {
                    "api_version": "v1",
                    "api_endpoint": "/vmware/vm"
                },
                "hyper-v": {
                    "api_version": "internal",
                    "api_endpoint": "/hyperv/vm"
                },
                "mssql_db": {
                    "api_version": "v1",
                    "api_endpoint": "/mssql/db"
                },
                "ec2_instance": {
                    "api_version": "internal",
                    "api_endpoint": "/aws/ec2_instance"
                },
                "oracle_db": {
                    "api_version": "internal",
                    "api_endpoint": "/oracle/db"
                },
                "vcd": {
                    "api_version": "internal",
                    "api_endpoint": "/vcd/vapp"
                },
                "managed_volume": {
                    "api_version": "internal",
                    "api_endpoint": "/managed_volume"
                },
                "ahv": {
                    "api_version": "internal",
                    "api_endpoint": "/nutanix/vm"
                },


            }

            all_vms_in_sla = self.get(
                api_call[object_type]["api_version"],
                api_call[object_type]["api_endpoint"] +
                "?effective_sla_domain_id={}&is_relic=false".format(sla_id),
                timeout=timeout)

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

        self.function_name = inspect.currentframe().f_code.co_name

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
            if not isinstance(param, int) and param is not None:
                raise InvalidParameterException(
                    "All 'frequency' and 'retention' parameters must be integers.")

        if not isinstance(retention_on_brik_in_days, int) and retention_on_brik_in_days is not None:
            raise InvalidParameterException(
                "The 'retention_on_brik_in_days' parameter must be integer.")

        # Make sure at least one frequency and retention is populated
        if all(value is None for value in all_params):
            raise InvalidParameterException(
                "You must populate at least one frequency and retention.")

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
            if hourly_frequency is not None:
                config["frequencies"]["hourly"] = {}
                config["frequencies"]["hourly"]["frequency"] = hourly_frequency
                config["frequencies"]["hourly"]["retention"] = hourly_retention

            if daily_frequency is not None:
                config["frequencies"]["daily"] = {}
                config["frequencies"]["daily"]["frequency"] = daily_frequency
                config["frequencies"]["daily"]["retention"] = daily_retention

            if monthly_frequency is not None:
                config["frequencies"]["monthly"] = {}
                config["frequencies"]["monthly"]["dayOfMonth"] = "LastDay"
                config["frequencies"]["monthly"]["frequency"] = monthly_frequency
                config["frequencies"]["monthly"]["retention"] = monthly_retention

            if yearly_frequency is not None:
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
            archival_location_id = self.object_id(
                archive_name, "archival_location", timeout=timeout)

            # convert retention in days to seconds
            retention_on_brik_in_seconds = retention_on_brik_in_days * 86400
            if instant_archive is False:
                archival_threshold = retention_on_brik_in_seconds
            else:
                archival_threshold = 1

            config["localRetentionLimit"] = retention_on_brik_in_seconds

            config["archivalSpecs"] = [{
                "locationId": archival_location_id,
                "archivalThreshold": archival_threshold
            }]

        if sla_id is not False:
            self.log(
                "create_sla: Getting the configuration details for the SLA Domain {} already on the Rubrik cluster.".format(name))
            if v2_sla is True:
                current_sla_details = self.get(
                    "v2", "/sla_domain/{}".format(sla_id), timeout=timeout)
            else:
                current_sla_details = self.get(
                    "v1", "/sla_domain/{}".format(sla_id), timeout=timeout)

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
                raise InvalidParameterException(
                    "The Rubrik cluster already has an SLA Domain named '{}' whose configuration does not match the values provided.".format(name))

        self.log("create_sla: Creating the new SLA")
        if v2_sla is True:
            return self.post("v2", "/sla_domain", config, timeout=timeout)
        else:
            return self.post("v1", "/sla_domain", config, timeout=timeout)

    def delete_sla(self, name, timeout=15):
        """Delete an SLA from the Rubrik Cluster
        Arguments:
            name {[type]} -- The name of the SLA you wish to delete.
        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection to the Rubrik cluster. (default: {15})
        Returns:
            dict -- The full API response for `DELETE /v1/sla_domain`.
            dict -- The full API response for `DELETE /v2/sla_domain`.
        """

        self.function_name = inspect.currentframe().f_code.co_name

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

        if self.function_name == "":
            self.function_name = inspect.currentframe().f_code.co_name

        if start <= end:
            return start <= point_in_time <= end
        else:
            return start <= point_in_time or point_in_time <= end

    def sql_live_mount(self, db_name, sql_instance, sql_host, mount_name, date='latest', time='latest', timeout=30):  # pylint: ignore
        """Live Mount a database from a specified recovery point.
        Arguments:
            db_name {str} -- The name of the database to Live Mount.
            sql_instance {str} -- The SQL instance name with the database you wish to Live Mount.
            sql_host {str} -- The SQL Host of the database/instance to Live Mount.
            mount_name {str} -- The name given to the Live Mounted database i.e. AdventureWorks_Clone.
        Keyword Arguments:
            date {str} -- The recovery_point date to recovery to formated as `Month-Day-Year` (ex: 1-15-2014). If `latest` is specified, the last snapshot taken will be used. (default: {'latest'})
            time {str} -- The recovery_point time to recovery to formated as `Hour:Minute AM/PM` (ex: 1:30 AM). If `latest` is specified, the last snapshot taken will be used. (default: {'latest'})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {30})
        Returns:
            dict -- The full response of `POST /v1/mssql/db/{id}/mount`.
        """
        if date != 'latest' and time == 'latest' or date == 'latest' and time != 'latest':
            raise InvalidParameterException(
                "The date and time arguments most both be 'latest' or a specific date and time.")

        if self.function_name == "":
            self.function_name = inspect.currentframe().f_code.co_name

        mssql_id = self._validate_sql_db(db_name, sql_instance, sql_host)

        recovery_point = self._validate_sql_recovery_point(
            mssql_id, date, time)

        try:
            if not recovery_point['is_recovery_point']:
                raise InvalidParameterException(
                    "The database '{}' does not have a recovery_point taken on {} at {}.".format(
                        db_name, date, time))
        except NameError:
            pass
        else:
            config = {}
            config['recoveryPoint'] = {
                'timestampMs': recovery_point['recovery_timestamp']}
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

        self.function_name = inspect.currentframe().f_code.co_name

        self.log("vsphere_live_unmount: Searching the Rubrik cluster for the Live Mount vSphere VM '{}'.".format(
            mounted_vm_name))
        mounted_vm_id = self.object_id(
            mounted_vm_name, 'vmware', timeout=timeout)

        self.log(
            "vsphere_live_unmount: Getting the vSphere VM mount information from the Rubrik cluster.")
        mount_summary = self.get(
            'v1', '/vmware/vm/snapshot/mount', timeout=timeout)

        self.log("vsphere_live_unmount: Getting the mount ID of the vSphere VM '{}'.".format(
            mounted_vm_name))
        for mountedvm in mount_summary['data']:
            if mountedvm['mountedVmId'] == mounted_vm_id:
                mount_id = mountedvm['id']
                break
        else:
            raise InvalidParameterException(
                "The mounted vSphere VM '{}' does not exist, please provide a valid instance".format(mounted_vm_name))

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

        self.function_name = inspect.currentframe().f_code.co_name

        mounted_db_id = self._validate_sql_db(
            mounted_db_name, sql_instance, sql_host)

        self.log(
            "sql_live_unmount: Getting the MSSQL mount information from the Rubrik cluster.")
        mount_summary = self.get('v1', '/mssql/db/mount', timeout=timeout)

        self.log("sql_live_unmount: Getting the mount ID of the mounted database '{}'.".format(
            mounted_db_name))
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

        self.function_name = inspect.currentframe().f_code.co_name

        self.log(
            "get_vsphere_live_mount: Searching the Rubrik cluster for the mounted vSphere VM '{}'.".format(vm_name))
        vm_id = self.object_id(vm_name, 'vmware', timeout=timeout)

        self.log(
            "get_vsphere_live_mount: Getting Live Mounts of vSphere VM {}.".format(vm_name))
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

        self.function_name = inspect.currentframe().f_code.co_name

        self.log("get_vsphere_live_mount_names: Searching the Rubrik cluster for the mounted vSphere VM '{}'.".format(vm_name))
        vm_id = self.object_id(vm_name, 'vmware', timeout=timeout)

        self.log(
            "get_vsphere_live_mount_names: Getting Live Mounts of vSphere VM {}.".format(vm_name))
        mounted_vm = self.get(
            'v1', '/vmware/vm/snapshot/mount?vm_id={}'.format(vm_id), timeout)
        mounted_vm_name = []
        for vm in mounted_vm['data']:
            try:
                vm_moid = vm['mountedVmId']
                split_moid = vm_moid.split('-')
                moid = split_moid[-2] + '-' + split_moid[-1]
                self.log(
                    "get_vsphere_live_mount_names: Getting summary of VM with moid '{}'.".format(moid))
                vm_data = self.get(
                    'v1', '/vmware/vm?moid={}'.format(moid), timeout)
                mounted_vm_name.append(vm_data['data'][0]['name'])
            except KeyError:
                self.log(
                    "get_vsphere_live_mount_names: A Live Mount of vSphere VM '{}' is in progress.".format(vm_name))
                continue
        return mounted_vm_name

    def _validate_sql_db(self, db_name, sql_instance, sql_host, timeout=30):  # pylint: ignore
        """Checks whether a database exist on an SQL Instance and Host.
        Arguments:
            db_name {str} -- The name of the database.
            sql_instance {str} -- The SQL instance.
            sql_host {str} -- The SQL server hostname.
        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {30})
        Returns:
            str -- The ID of the MSSQL database.
        """

        self.function_name = inspect.currentframe().f_code.co_name

        mssql_host_id = self.object_id(
            sql_host, 'physical_host', timeout=timeout)

        self.log(
            "_validate_sql_db: Getting the list of instances on host {}.".format(sql_host))
        mssql_instance = self.get(
            'v1', '/mssql/instance?primary_cluster_id=local&root_id={}'.format(mssql_host_id), timeout=timeout)

        for instance in mssql_instance['data']:
            if instance['name'] == sql_instance:
                sql_instance_id = instance['id']
                break
        else:
            raise InvalidParameterException(
                "The SQL instance {} does not exist, please provide a valid instance".format(sql_instance))

        self.log(
            "_validate_sql_db: Getting the list of databases on the instance {}, on host {}.".format(
                sql_instance,
                sql_host))
        mssql_db = self.get(
            'v1',
            '/mssql/db?primary_cluster_id=local&instance_id={}'.format(
                sql_instance_id),
            timeout=timeout)

        for db in mssql_db['data']:
            if db['name'] == db_name:
                mssql_id = db['id']
                break
        else:
            raise InvalidParameterException(
                "The database {} does not exist, please provide a valid database".format(db_name))
        return mssql_id

    def get_sql_live_mount(self, db_name, sql_instance=None, sql_host=None, timeout=30):  # pylint: ignore
        """Retrieve the Live Mounts for a MSSQL source database.
        Arguments:
            db_name {str} -- The name of the source database with Live Mounts.
        Keyword Arguments:
            sql_instance {str} -- The SQL instance name of the source database.
            sql_host {str} -- The SQL host name of the source database/instance.
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {30})
        Returns:
            dict -- The full response of `GET /v1/mssql/db/mount?source_database_id={id}`.
        """

        self.function_name = inspect.currentframe().f_code.co_name

        mssql_id = self._validate_sql_db(db_name, sql_instance, sql_host)

        self.log(
            "get_sql_live_mount: Getting the live mounts for mssql db id'{}'.".format(mssql_id))
        return self.get('v1', '/mssql/db/mount?source_database_id={}'.format(mssql_id), timeout)

    def _validate_sql_recovery_point(self, mssql_id, date, time, timeout=30):  # pylint: ignore
        """Check whether the data and time provided is a valid recovery point for an MSSQL database
        Arguments:
            mssql_id {str} -- The ID of the database.
            date {str} -- The recovery_point date formated as `Month-Day-Year` (ex: 1-15-2014).
            time {str} -- The recovery_point time  formated as `Hour:Minute AM/PM` (ex: 1:30 AM).
        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {30})
        Returns:
            dict -- A dictionary with values {'is_recovery_point': bool, 'recovery_timestamp': datetime}.
        """

        if self.function_name == "":
            self.function_name = inspect.currentframe().f_code.co_name

        is_recovery_point = False
        if date and time == 'latest':
            latest_data = self.get(
                'v1', '/mssql/db/{}/snapshot'.format(mssql_id), timeout=timeout)
            try:
                latest_date_time = latest_data['data'][0]['date']
            except:
                raise InvalidParameterException(
                    "The database with ID {} does not have any existing snapshots.".format(mssql_id))
            # Parsing latest snapshot time string value to a datetime object as YYYY-MM-DDTHH:MM
            data_str = datetime.strptime(
                latest_date_time[:16], '%Y-%m-%dT%H:%M')
            # Create date & time strings from datetime object as MM-DD-YYYY & HH:MM AM/PM
            date_str, time_str = [data_str.strftime(
                '%m-%d-%Y'), data_str.strftime('%I:%M %p')]
            # Convert the date & time to cluster timezone, see _date_time_conversion function for details
            recovery_date_time = self._date_time_conversion(date_str, time_str)
            # Parse again to datetime object
            recovery_date_time = datetime.strptime(
                recovery_date_time, '%Y-%m-%dT%H:%M')
            # Create recovery timestamp in (ms) as integer from datetime object
            recovery_timestamp = int(recovery_date_time.strftime('%s')) * 1000
            is_recovery_point = True
        else:
            self.log(
                "_validate_sql_recovery_point: Getting the recoverable range for db ID:'{}'.".format(mssql_id))
            range_summary = self.get(
                'v1', '/mssql/db/{}/recoverable_range'.format(mssql_id), timeout=timeout)

            self.log(
                "_validate_sql_recovery_point: Converting the provided date/time into UTC.")
            # Convert the date & time to cluster timezone, see _date_time_conversion function for details
            recovery_date_time = self._date_time_conversion(date, time)
            # Parse to datetime object
            recovery_date_time = datetime.strptime(
                recovery_date_time, '%Y-%m-%dT%H:%M')
            # Create recovery timestamp in (ms) as integer from datetime object
            recovery_timestamp = int(recovery_date_time.strftime('%s')) * 1000

            for range in range_summary['data']:
                start_str, end_str = [range['beginTime'], range['endTime']]
                # Parsing the range beginTime and endTime values to a datetime object as YYYY-MM-DDTHH:MM
                start, end = [datetime.strptime(start_str[:16], '%Y-%m-%dT%H:%M'),
                              datetime.strptime(end_str[:16], '%Y-%m-%dT%H:%M')]

                self.log(
                    "_validate_sql_recovery_point: Searching for the provided recovery_point.")
                is_recovery_point = self._time_in_range(
                    start, end, recovery_date_time)
                if not is_recovery_point:
                    continue
                else:
                    break

        return {
            "is_recovery_point": is_recovery_point,
            "recovery_timestamp": recovery_timestamp
        }

    def sql_instant_recovery(self, db_name, date, time, sql_instance=None, sql_host=None, finish_recovery=True, max_data_streams=0, timeout=30):  # pylint: ignore
        """Perform an instant recovery for MSSQL database from a specified recovery point.
        Arguments:
            db_name {str} -- The name of the database to instantly recover.
            date {str} -- The recovery_point date to recover to formated as `Month-Day-Year` (ex: 1-15-2014).
            time {str} -- The recovery_point time to recover to formated as `Hour:Minute AM/PM` (ex: 1:30 AM).
        Keyword Arguments:
            sql_instance {str} -- The SQL instance name with the database to instantly recover.
            sql_host {str} -- The SQL Host of the database/instance to instantly recover.
            finish_recovery {bool} -- A Boolean value that determines the recovery option to use during database restore. When this value is 'true', the database is restored using the RECOVERY option and is fully functional at the end of the restore operation. When this value is 'false', the database is restored using the NORECOVERY option and remains in recovering mode at the end of the restore operation.
            max_data_streams {int} -- Maximum number of parallel data streams that can be used to copy data to the target system.
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {30})
        Returns:
            dict -- The full response of `POST /v1/mssql/db/{id}/restore`.
        """

        self.function_name = inspect.currentframe().f_code.co_name

        mssql_id = self._validate_sql_db(db_name, sql_instance, sql_host)

        recovery_point = self._validate_sql_recovery_point(
            mssql_id, date, time)

        try:
            if recovery_point['is_recovery_point'] == False:
                raise InvalidParameterException(
                    "The database '{}' does not have a recovery_point taken on {} at {}.".format(
                        db_name, date, time))
        except NameError:
            pass
        else:
            config = {}
            config['recoveryPoint'] = {
                'timestampMs': recovery_point['recovery_timestamp']}
            config['finish_recovery'] = finish_recovery
            config['max_data_streams'] = max_data_streams

            self.log(
                "sql_instant_recovery: Performing instant recovery of {} to recovery_point {} at {}.".format(
                    db_name,
                    date,
                    time))

            return self.post('v1', '/mssql/db/{}/restore'.format(mssql_id), config, timeout)

    def vcenter_refresh_vm(self, vm_name, timeout=15):  # pylint: ignore
        """Refresh a single vSphere VM metadata.
        Arguments:
            vm_name {str} -- The name of the vSphere VM.
        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})
        Returns:
            no content.
        """

        self.function_name = inspect.currentframe().f_code.co_name

        self.log(
            "vcenter_refresh_vm: Searching the Rubrik cluster for the vSphere VM '{}'.".format(vm_name))
        data = self.get('v1', '/vmware/vm?name={}'.format(vm_name), timeout)
        if data['data'] == []:
            raise InvalidParameterException(
                "The vSphere VM '{}' does not exist.".format(vm_name))
        else:
            vcenter_id = data['data'][0]['infraPath'][0]['id']
            vm_id = data['data'][0]['id']

        self.log(
            "vcenter_refresh_vm: Getting the MOID for vSphere VM {}.".format(vm_name))
        split_moid = vm_id.split('-')
        moid = split_moid[-2] + '-' + split_moid[-1]
        config = {'vmMoid': moid}
        self.log(
            "vcenter_refresh_vm: Refreshing vSphere VM {} metadata.".format(vm_name))
        self.post(
            'internal', '/vmware/vcenter/{}/refresh_vm'.format(vcenter_id), config, timeout)

    def get_vsphere_vm(self, name=None, is_relic=None, effective_sla_domain_id=None, primary_cluster_id=None, limit=None, offset=None, moid=None, sla_assignment=None, guest_os_name=None, sort_by=None, sort_order=None, timeout=15):  # pylint: ignore
        """Get summary of all the VMs. Each keyword argument is a query parameter to filter the VM details returned i.e. you can query for a specific VM name, is_relic, effective_sla_domain etc.
        Keyword Arguments:
            name {str} -- Search by using a virtual machine name.
            is_relic {bool} -- Filter by the isRelic field of the virtual machine. When this parameter is not set, return both relic and non-relic virtual machines.
            effective_sla_domain_id {str} -- Filter by ID of effective SLA Domain.
            primary_cluster_id {str} -- Filter by primary cluster ID, or local.
            limit {int} -- Limit the number of matches returned.
            offset {int} -- Ignore these many matches in the beginning.
            moid {str} -- Search by using a virtual machine managed object ID.
            sla_assignment {str} -- Filter by SLA Domain assignment type. (Direct, Derived, Unassigned)
            guest_os_name {str} -- Filters by the name of operating system using infix search.
            sort_by {str} -- Sort results based on the specified attribute. (effectiveSlaDomainName, name, moid, folderPath, infraPath)
            sort_order {str} -- Sort order, either ascending or descending. (asc, desc)
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})
        Returns:
            dict -- The full response of `GET /v1/vmware/vm?{query}`
        """

        if self.function_name == "":
            self.function_name = inspect.currentframe().f_code.co_name

        parameters = {'effective_sla_domain_id': effective_sla_domain_id,
                      'primary_cluster_id': primary_cluster_id,
                      'limit': limit,
                      'offset': offset,
                      'is_relic': is_relic,
                      'name': name,
                      'moid': moid,
                      'sla_assignment': sla_assignment,
                      'guest_os_name': guest_os_name,
                      'sort_by': sort_by,
                      'sort_order': sort_order}
        parameters = {key: value for key,
                      value in parameters.items() if value is not None}

        self.log("get_vsphere_vm: checking the provided query parameters.")
        valid_sla_assignment = ['Derived', 'Direct', 'Unassigned']
        for key, value in parameters.items():
            if key == 'sla_assignment' and value not in valid_sla_assignment:
                raise InvalidParameterException(
                    'The sla_assignment parameter must be one of the following: {}'.format(valid_sla_assignment))

        valid_sort_by = ['effectiveSlaDomainName',
                         'name', 'moid', 'folderPath', 'infraPath']
        for key, value in parameters.items():
            if key == 'sort_by' and value not in valid_sort_by:
                raise InvalidParameterException(
                    'The sort_by parameter must be one of the following: {}'.format(valid_sort_by))

        valid_sort_order = ['asc', 'desc']
        for key, value in parameters.items():
            if key == 'sort_order' and value not in valid_sort_order:
                raise InvalidParameterException(
                    'The sort_order parameter must be one of the following: {}'.format(valid_sort_order))

        for key, value in parameters.items():
            if key == 'is_relic' and not isinstance(value, bool):
                raise InvalidParameterException(
                    'The is_relic paremeter must be a boolean: True or False')

        for key, value in parameters.items():
            if ((key == 'limit') or (key == 'offset')) and not isinstance(value, int):
                raise InvalidParameterException(
                    'The limit and offset paremeter must be an integer')

        # String joins by iterating through the key-value pairs in the parameters dictionary and concatenating it into a query
        query = '&'.join(['%s=%s' % kv for kv in parameters.items()])

        self.log("get_vsphere_vm: Get summary of all the VMs.")
        return self.get('v1', '/vmware/vm?{}'.format(query), timeout)

    def get_vsphere_vm_snapshot(self, vm_name, timeout=15):  # pylint: ignore
        """Retrieve summary information for the snapshots of a virtual machine.
        Arguments:
            vm_name {str} -- Name of the virtual machine.
        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection with the Rubrik cluster before returning a timeout error. (default: {15})
        Returns:
            dict -- The full response of `GET /v1/vmware/vm/{vm_id}/snapshot`
        """

        if self.function_name == "":
            self.function_name = inspect.currentframe().f_code.co_name

        self.log(
            "get_vsphere_vm_snapshot: Searching the Rubrik cluster for the vSphere VM '{}'.".format(vm_name))
        vm_id = self.object_id(vm_name, 'vmware', timeout=timeout)

        self.log("get_vsphere_vm_snapshot: Getting summary information for the snapshots of virtual machine {}".format(vm_id))
        return self.get('v1', '/vmware/vm/{}/snapshot'.format(vm_id), timeout)

    def get_vsphere_vm_details(self, vm_name, timeout=15):  # pylint: ignore
        """Retrieve details for a virtual machine.
        Arguments:
            vm_name {str} -- Name of the virtual machine.
        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection with the Rubrik cluster before returning a timeout error. (default: {15})
        Returns:
            dict -- The full response of `GET /v1/vmware/vm/{vm_id}`
        """

        if self.function_name == "":
            self.function_name = inspect.currentframe().f_code.co_name

        self.log(
            "get_vsphere_vm_details: Searching the Rubrik cluster for the vSphere VM '{}'.".format(vm_name))
        vm_id = self.object_id(vm_name, 'vmware', timeout=timeout)

        self.log(
            "get_vsphere_vm_details: Getting details of virtual machine {}".format(vm_id))
        return self.get('v1', '/vmware/vm/{}'.format(vm_id), timeout)

    def get_vsphere_vm_file(self, vm_name, path, timeout=15):  # pylint: ignore
        """Search for a file in the snapshots of a virtual machine. Specify the file by full path prefix or filename prefix.
        Arguments:
            vm_name {str} -- Name of the virtual machine.
            path {str} -- The path query. Use either a path prefix or a filename prefix.
        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection with the Rubrik cluster before returning a timeout error. (default: {15})
        Returns:
            dict -- The full response of `GET /v1/vmware/vm/{vm_id}/search?path={path}`
        """

        if self.function_name == "":
            self.function_name = inspect.currentframe().f_code.co_name

        self.log(
            "get_vsphere_vm_file: Searching the Rubrik cluster for the vSphere VM '{}'.".format(vm_name))
        vm_id = self.object_id(vm_name, 'vmware', timeout=timeout)

        self.log(
            "get_vsphere_vm_file: Search for file/path {} in the snapshots of a virtual machine {}".format(path, vm_id))
        return self.get('v1', '/vmware/vm/{}/search?path={}'.format(vm_id, path), timeout)

    def get_sql_db(self, db_name=None, instance=None, hostname=None, availability_group=None, effective_sla_domain=None, primary_cluster_id='local', sla_assignment=None, limit=None, offset=None, is_relic=None, is_live_mount=None, is_log_shipping_secondary=None, sort_by=None, sort_order=None, timeout=15):  # pylint: ignore
        """Retrieves summary information for SQL databases. Each keyword argument is a query parameter to filter the database details returned i.e. you can query for a specific database name, hostname, instance, is_relic, effective_sla_domain etc.
        Keyword Arguments:
            db_name {str} -- Filter by a substring of the database name.
            instance {str} -- The SQL instance name of the database.
            hostname {str} -- The SQL host name of the database.
            availability_group {str} -- Filter by the name of the Always On Availability Group.
            effective_sla_domain {str} -- Filter by the name of the effective SLA Domain.
            primary_cluster_id {str} -- Filter by primary cluster ID, or local.
            sla_assignment {str} -- Filter by SLA Domain assignment type. (Direct, Derived, Unassigned)
            limit {int} -- Limit the number of matches returned.
            offset {int} -- Ignore these many matches in the beginning.
            is_relic {bool} -- Filter database summary information by the value of the isRelic field.
            is_live_mount {bool} -- Filter database summary information by the value of the isLiveMount field.
            is_log_shipping_secondary {bool} -- Filter database summary information by the value of the isLogShippingSecondary field.
            sort_by {str} -- Sort results based on the specified attribute. (effectiveSlaDomainName, name)
            sort_order {str} -- Sort order, either ascending or descending. (asc, desc)
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})
        Returns:
            dict -- The full response of `GET /v1/mssql/db?{query}`
        """

        if self.function_name == "":
            self.function_name = inspect.currentframe().f_code.co_name

        if availability_group is not None:
            self.log("get_sql_db: Searching the Rubrik cluster for the ID of the availability_group {}.".format(
                availability_group))
            ag_summary = self.get(
                'internal', '/mssql/availability_group', timeout=timeout)
            for ag in ag_summary['data']:
                if availability_group == ag['name']:
                    availability_group_id = ag['id']
        else:
            availability_group_id = None

        if effective_sla_domain is not None:
            self.log("get_sql_db: Searching the Rubrik cluster for the ID of the SLA Domain '{}'.".format(
                effective_sla_domain))
            effective_sla_domain_id = self.object_id(
                effective_sla_domain, 'sla', timeout=timeout)
        else:
            effective_sla_domain_id = None

        parameters = {'availability_group_id': availability_group_id,
                      'effective_sla_domain_id': effective_sla_domain_id,
                      'primary_cluster_id': primary_cluster_id,
                      'name': db_name,
                      'sla_assignment': sla_assignment,
                      'limit': limit,
                      'offset': offset,
                      'is_relic': is_relic,
                      'is_live_mount': is_live_mount,
                      'is_log_shipping_secondary': is_log_shipping_secondary,
                      'sort_by': sort_by,
                      'sort_order': sort_order}
        parameters = {key: value for key,
                      value in parameters.items() if value is not None}

        self.log("get_sql_db: checking the provided query parameters.")
        valid_sla_assignment = ['Derived', 'Direct', 'Unassigned']
        for key, value in parameters.items():
            if key == 'sla_assignment' and value not in valid_sla_assignment:
                raise InvalidParameterException(
                    'The sla_assignment parameter must be one of the following: {}'.format(valid_sla_assignment))

        valid_sort_by = ['effectiveSlaDomainName', 'name']
        for key, value in parameters.items():
            if key == 'sort_by' and value not in valid_sort_by:
                raise InvalidParameterException(
                    'The sort_by parameter must be one of the following: {}'.format(valid_sort_by))

        valid_sort_order = ['asc', 'desc']
        for key, value in parameters.items():
            if key == 'sort_order' and value not in valid_sort_order:
                raise InvalidParameterException(
                    'The sort_order parameter must be one of the following: {}'.format(valid_sort_order))

        for key, value in parameters.items():
            if ((key == 'is_relic') or (key == 'is_live_mount') or (
                    key == 'is_log_shipping_secondary')) and not isinstance(value, bool):
                raise InvalidParameterException(
                    'The is_relic, is_live_mount, is_log_shipping_secondary paremeter must be a boolean: True or False')

        for key, value in parameters.items():
            if ((key == 'limit') or (key == 'offset')) and not isinstance(value, int):
                raise InvalidParameterException(
                    'The limit and offset paremeter must be an integer')

        # String joins by iterating through the key-value pairs in the parameters dictionary and concatenating it into a query
        query = '&'.join(['%s=%s' % kv for kv in parameters.items()])

        self.log(
            "get_sql_db: Get summary of all the databases returned by the query.")
        databases = self.get('v1', '/mssql/db?{}'.format(query), timeout)

        result = []

        if instance is None and hostname is None:
            return databases['data']
        elif instance is None and hostname is not None:
            for item in databases['data']:
                if item['rootProperties']['rootName'] == hostname:
                    result.append(item)
        elif instance is not None and hostname is None:
            try:
                for item in databases['data']:
                    for replica in item['replicas']:
                        if replica['instanceName'] == instance:
                            result.append(item)
                        break
            except BaseException:
                pass
            else:
                result = [item for item in databases['data']
                          if replica['instanceName'] == instance]
        elif instance is not None and hostname is not None:
            try:
                for item in databases['data']:
                    for replica in item['replicas']:
                        if item['rootProperties']['rootName'] == hostname and replica['instanceName'] == instance:
                            result.append(item)
                        break
            except BaseException:
                pass
            else:
                result = [
                    item for item in databases['data'] if (
                        item['rootProperties']['rootName'] == hostname and replica['instanceName'] == instance)]
        return result

    def get_sql_db_files(self, db_name, date, time, sql_instance=None, sql_host=None, timeout=15):  # pylint: ignore
        """Provides a list of database files to be restored for the specified restore or export operation. The Data, Log and Filestream files will be retrieved along with name and path information.
        Arguments:
            db_name {str} -- The name of the database.
            date {str} -- The recovery_point date formated as 'Month-Date-Year' (ex: 8-9-2018).
            time {str} -- The recovery_point time formated as `Hour:Minute` (ex: 3:30 AM).
        Keyword Arguments:
            sql_instance {str} -- The SQL instance name with the database.
            sql_host {str} -- The SQL Host of the database/instance.
            timeout {int} -- The number of seconds to wait to establish a connection with the Rubrik cluster before returning a timeout error. (default: {30})
        Returns:
            list -- The full response of `GET /internal/mssql/db/{id}/restore_files?time={recovery_point}`.
        """

        if self.function_name == "":
            self.function_name = inspect.currentframe().f_code.co_name

        mssql_id = self._validate_sql_db(db_name, sql_instance, sql_host)

        recovery_date_time = self._date_time_conversion(date, time)
        recovery_point = datetime.strptime(
            recovery_date_time, '%Y-%m-%dT%H:%M').isoformat()
        valid_recovery_point = self._validate_sql_recovery_point(
            mssql_id, date, time)

        try:
            if valid_recovery_point['is_recovery_point'] == False:
                raise InvalidParameterException(
                    "The database '{}' does not have a recovery_point taken on {} at {}.".format(
                        db_name, date, time))
        except NameError:
            pass
        else:
            self.log(
                "get_sql_db_files: Getting SQL database '{}' files for recovery_point {} {}.".format(
                    db_name,
                    date,
                    time))
            return self.get('internal', '/mssql/db/{}/restore_files?time={}'.format(mssql_id, recovery_point), timeout)

    def sql_db_export(self, db_name, date, time, sql_instance=None, sql_host=None, target_instance_name=None, target_hostname=None, target_database_name=None, target_data_file_path=None, target_log_file_path=None, target_file_paths=None, finish_recovery=True, max_data_streams=2, allow_overwrite=False, timeout=15):  # pylint: ignore
        """Export an SQL database from a specified recovery point to a target SQL Instance and Host. Requires database data and log file name directory paths.
        Arguments:
            db_name {str} -- The name of the database to be exported.
            date {str} -- The recovery_point date formated as 'Month-Date-Year' (ex: 8-9-2018).
            time {str} -- The recovery_point time formated as `Hour:Minute` (ex: 3:30 AM).
        Keyword Arguments:
            sql_instance {str} -- The SQL instance name with the database to be exported.
            sql_host {str} -- The SQL Host of the database/instance to be exported.
            target_instance_name {str} -- Name of the Microsoft SQL instance for the new database.
            target_hostname {str} -- Name of the Microsoft SQL host for the new database.
            target_database_name {str} -- Name of the new database.
            target_data_file_path {str} -- The target path to store all data files.
            target_log_file_path {str} -- The target path to store all log files.
            target_file_paths {list} -- A list of dictionary objects each with key value pairs: {'logicalName': 'Logical name of the database file', 'exportPath': 'The target path for the database file', 'newLogicalName': 'New logical name for the database file', 'newFilename': 'New filename for the database file'}. One target path for each individual database file. Overrides targetDataFilePath and targetLogFilePath.
            finish_recovery {str} -- A Boolean value that determines the recovery option to use during database restore. When this value is 'true', the database is restored using the RECOVERY option and is fully functional at the end of the restore operation. When this value is 'false', the database is restored using the NORECOVERY option and remains in recovering mode at the end of the restore operation.
            max_data_streams {str} -- Maximum number of parallel data streams that can be used to copy data to the target system.
            allow_overwrite {str} -- A Boolean value that determines whether an existing database can be overwritten by a database this is exported from a backup. Set to false to prevent overwrites. This is the default. Set to true to allow overwrites.
            timeout {int} -- The number of seconds to wait to establish a connection with the Rubrik cluster before returning a timeout error. (default: {30})
        Returns:
            dict -- The full response of `POST /v1/mssql/db/{id}/export`.
        """

        self.function_name = inspect.currentframe().f_code.co_name

        if target_file_paths is None:
            if target_data_file_path is None or target_log_file_path is None:
                raise InvalidParameterException(
                    "The 'target_data_file_path' and 'target_log_file_path' parameters must be provided if a 'target_file_paths' dictionary list is not provided.")

        mssql_id = self._validate_sql_db(db_name, sql_instance, sql_host)
        recovery_point = self._validate_sql_recovery_point(
            mssql_id, date, time)

        target_host_id = self.object_id(
            target_hostname, 'physical_host', timeout=timeout)

        self.log("sql_db_export: Getting the instances on target host {}.".format(
            target_hostname))
        mssql_instance = self.get(
            'v1', '/mssql/instance?primary_cluster_id=local&root_id={}'.format(target_host_id), timeout=timeout)

        for instance in mssql_instance['data']:
            if instance['name'] == target_instance_name:
                target_instance_id = instance['id']
                break
        else:
            raise InvalidParameterException(
                "The target SQL instance {} does not exist, please provide a valid target instance".format(target_instance_name))

        try:
            if recovery_point['is_recovery_point'] == False:
                raise InvalidParameterException(
                    "The database '{}' does not have a recovery_point taken on {} at {}.".format(
                        db_name, date, time))
        except NameError:
            pass
        else:
            config = {}
            config['recoveryPoint'] = {
                'timestampMs': recovery_point['recovery_timestamp']}
            config['targetInstanceId'] = target_instance_id
            config['targetDatabaseName'] = target_database_name
            if target_file_paths is not None:
                config['targetFilePaths'] = target_file_paths
            else:
                config['targetDataFilePath'] = target_data_file_path
                config['targetLogFilePath'] = target_log_file_path
            config['finishRecovery'] = finish_recovery
            config['maxDataStreams'] = max_data_streams
            config['allowOverwrite'] = allow_overwrite

            self.log(
                "sql_db_export: Exporting the database '{}' from recovery_point on {} at {} with new name '{}'.".format(
                    db_name,
                    date,
                    time,
                    target_database_name))

            return self.post('v1', '/mssql/db/{}/export'.format(mssql_id), config, timeout)

    def set_esxi_subnets(self, esx_subnets=None, timeout=15):  # pylint: ignore
        """Sets the subnets that should be used to reach the ESXi hosts.
        Keyword Arguments:
            esx_subnets {list} -- Preferred subnets used to reach the ESX hosts.
            timeout {int} -- The number of seconds to wait to establish a connection with the Rubrik cluster before returning a timeout error. (default: {15})
        Returns:
            dict -- The full response of `PATCH /internal/vmware/config/set_esx_subnets`.
        """
        self.log(
            "set_esx_subnets: Getting the existing subnets used to reach the ESXi hosts")
        subnets = (self.get_esxi_subnets())['esxSubnets'].split(',')
        config = {}
        if esx_subnets is None:
            raise InvalidParameterException(
                "The 'esx_subnets' parameter must be provided.")
        elif isinstance(esx_subnets, list):
            if subnets == esx_subnets:
                return "No change required. The subnet list provided is the same as the existing values: {}.".format(
                    subnets)
            else:
                subnet_str = ','.join(esx_subnets)
                config['esxSubnets'] = subnet_str
                self.log(
                    "set_esx_subnets: Setting the subnets that should be used to reach the ESXi hosts: '{}'.".format(
                        esx_subnets))
                return self.patch('internal', '/vmware/config/set_esx_subnets', config, timeout)
        else:
            raise InvalidParameterException(
                "The provided 'esx_subnets' parameter is not a list.")

    def get_esxi_subnets(self, timeout=15):  # pylint: ignore
        """Retrieve the preferred subnets used to reach the ESXi hosts.
        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection with the Rubrik cluster before returning a timeout error. (default: {15})
        Returns:
            dict -- The full response of `GET /internal/vmware/config/esx_subnets`.
        """

        self.log(
            "get_esx_subnets: Retrieving the preferred subnets used to reach the ESXi hosts.")

        return self.get('internal', '/vmware/config/esx_subnets', timeout)

    def get_all_hosts(self, timeout=15):
        """Retrieve information for each host connected to the Rubrik cluster.
        Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})
        Returns:
            dict -- The result of the API call `GET /v1/host`
        """

        self.log(
            'get_all_hosts: Getting information for each host on the Rubrik cluster.')

        return self.get('v1', '/host', timeout=timeout)

    def register_vm(self, name, timeout=15):
        """Register the Rubrik Backup Service on a vSphere VM.
        Arguments:
            name {str} -- The name of the vSphere VM.
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})
        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {30})
        Returns:
            str -- No change required. The VM `name` is already registered.
            dict -- The result of the call for `POST /v1/vmware/vm/{id}/register_agent`.
        """

        vm_id = self.object_id(name, 'vmware', timeout=timeout)

        self.log('register_vm: Determining if the agent state of the VM. ]')
        vm_details = self.get("v1", "/vmware/vm/{}".format(vm_id))

        if vm_details["isAgentRegistered"] is True:
            return "No change required. The VM {} is already registered.".format(name)

        self.log('register_vm: Registering the RBS agent.')
        return self.post('v1', '/vmware/vm/{}/register_agent'.format(vm_id), {}, timeout=timeout)
