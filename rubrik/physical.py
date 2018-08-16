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
This module contains the Rubrik SDK Physical class.
"""

import sys
from .api import Api

_API = Api


class Physical(_API):
    """This class contains methods related to the managment of the Physical objects in the Rubrik Cluster.
    """

    def add_physical_host(self, hostname, timeout=60):
        """Add a physical host from the Rubrik Cluster.

        Arguments:
            hostname {str} -- The hostname or IP Address of the physical host you wish to add to the Rubrik Cluster.

        Keyword Arguments:
            timeout {int} -- The timeout value for the API call that adds the physical host to the Rubrik Cluster. (default: {60})

        Returns:
            str -- If the physical host is already present on the Rubrik Cluster, a message to that effect will be retuned.
            dict -- The response returned by the API call
        """

        self.log('Searching the Rubrik Cluster for the current hosts.')
        current_hosts = self.get('v1', '/host')

        for host in current_hosts['data']:
            if host['hostname'] == hostname:
                host_present = True
                return "The host '{}' is already connected to the Rubrik Cluster.".format(hostname)

        config = {}
        config['hostname'] = hostname
        config['hasAgent'] = True

        self.log("Adding the host '{}' to the Rubrik Cluster.".format(hostname))
        add_host = self.post('v1', '/host', config, timeout)

        return add_host

    def delete_physical_host(self, hostname, timeout=120):
        """Delete a physical host from the Rubrik Cluster.

        Arguments:
            hostname {str} -- The hostname or IP Address of the physical host you wish to remove from the Rubrik Cluster.

        Keyword Arguments:
            timeout {int} -- The timeout value for the API call that deletes the physical host from the Rubrik Cluster. (default: {120})

        Returns:
            str -- If the physical host is not present on the Rubrik Cluster, a message to that effect will be retuned.
            dict -- The response returned by the API call.
        """

        self.log('Searching the Rubrik Cluster for the current hosts.')
        current_hosts = self.get('v1', '/host')

        host_present = False

        for host in current_hosts['data']:
            if host['hostname'] == hostname:
                host_present = True
                host_id = host['id']
                break

        if host_present is False:
            return "The host '{}' is not connected to the Rubrik Cluster.".format(hostname)

        self.log("Deleting the host '{}' from the Rubrik Cluster.".format(hostname))
        delete_host = self.delete('v1', '/host/{}'.format(host_id), timeout)

        return delete_host

    def create_physical_fileset(self, name, operating_system, include, exclude, exclude_exception, follow_network_shares=False, backup_hidden_folders=False, timeout=15):

        valid_operating_system = ['Linux', 'Windows']

        if operating_system not in valid_operating_system:
            sys.exit("Error: The create_physical_fileset() operating_system argument must be one of the following: {}.".format(
                valid_operating_system))

        if isinstance(follow_network_shares, bool) is False:
            sys.exit("Error: The 'follow_network_shares' argument must be True or False.")
        elif isinstance(backup_hidden_folders, bool) is False:
            sys.exit("Error: The 'backup_hidden_folders' argument must be True or False.")
        elif isinstance(include, list) is False:
            sys.exit("Error: The 'include' argument must be a list object.")
        elif isinstance(exclude, list) is False:
            sys.exit("Error: The 'exclude' argument must be a list object.")

        config = {}
        config['name'] = name
        config['includes'] = sorted(include)
        config['excludes'] = sorted(exclude)
        config['exceptions'] = sorted(exclude_exception)
        config['allowBackupHiddenFoldersInNetworkMounts'] = follow_network_shares
        config['allowBackupNetworkMounts'] = backup_hidden_folders
        config['operatingSystemType'] = operating_system

        self.log("create_fileset: Searching the Rubrik Cluster for all current {} Filesets.".format(operating_system))
        current_filesets = self.get(
            'v1', '/fileset_template?primary_cluster_id=local&operating_system_type={}&name={}'.format(operating_system, name), timeout)

        current_config = {}
        if current_filesets['data']:
            current_config['name'] = current_filesets['data'][0]['name']
            current_config['includes'] = sorted(current_filesets['data'][0]['includes'])
            current_config['excludes'] = sorted(current_filesets['data'][0]['excludes'])
            current_config['exceptions'] = sorted(current_filesets['data'][0]['exceptions'])
            current_config['allowBackupHiddenFoldersInNetworkMounts'] = current_filesets['data'][0]['allowBackupHiddenFoldersInNetworkMounts']
            current_config['operatingSystemType'] = current_filesets['data'][0]['operatingSystemType']
            current_config['allowBackupNetworkMounts'] = current_filesets['data'][0]['allowBackupNetworkMounts']

        if current_config == config:
            return("The Rubrik Cluster already has a {} Fileset named '{}' configured with the provided variables.".format(operating_system, name))

        # Add the config dict to a list
        model = []
        model.append(config)

        self.log("create_fileset: Creating the '{}' Fileset.".format(name))

    def create_nas_fileset(self, name, share_type, include, exclude, exclude_exception, follow_network_shares=False, timeout=15):

        valid_share_type = ['NFS', 'SMB']

        if share_type not in valid_share_type:
            sys.exit("Error: The create_fileset() share_type argument must be one of the following: {}.".format(valid_share_type))

        if isinstance(follow_network_shares, bool) is False:
            sys.exit("Error: The 'follow_network_shares' argument must be True or False.")
        elif isinstance(include, list) is False:
            sys.exit("Error: The 'include' argument must be a list object.")
        elif isinstance(exclude, list) is False:
            sys.exit("Error: The 'exclude' argument must be a list object.")

        config = {}
        config['name'] = name
        config['includes'] = sorted(include)
        config['excludes'] = sorted(exclude)
        config['exceptions'] = sorted(exclude_exception)
        config['allowBackupHiddenFoldersInNetworkMounts'] = follow_network_shares
        config['shareType'] = share_type

        self.log("create_fileset: Searching the Rubrik Cluster for all current NAS Filesets.")
        current_filesets = self.get(
            'v1', '/fileset_template?primary_cluster_id=local&operating_system_type=NONE&name={}'.format(name), timeout=timeout)

        current_config = {}
        if current_filesets['data']:
            current_config['name'] = current_filesets['data'][0]['name']
            current_config['includes'] = sorted(current_filesets['data'][0]['includes'])
            current_config['excludes'] = sorted(current_filesets['data'][0]['excludes'])
            current_config['exceptions'] = sorted(current_filesets['data'][0]['exceptions'])
            current_config['allowBackupHiddenFoldersInNetworkMounts'] = current_filesets['data'][0]['allowBackupHiddenFoldersInNetworkMounts']
            current_config['shareType'] = current_filesets['data'][0]['shareType']

        if current_config == config:
            return("The Rubrik Cluster already has a NAS Fileset named '{}' configured with the provided variables.".format(name))

        # Add the config dict to a list
        model = []
        model.append(config)

        self.log("create_fileset: Creating the '{}' Fileset.".format(name))
        return self.post('internal', '/fileset_template/bulk', model, timeout=timeout)

    def manage_physical_host_protection(self, hostname, fileset_name, operating_system, sla_name, timeout=15):

        # TODO: Add the ability to specify all parms of a fileset in case there are identically named Filesets on the Cluster

        valid_operating_system = ['Linux', 'Windows']

        if operating_system not in valid_operating_system:
            sys.exit("Error: The create_physical_fileset() operating_system argument must be one of the following: {}.".format(
                valid_operating_system))

        self.log("manage_physical_host_protection: Searching the Rubrik Cluster for the {} physical host {}.".format(
            operating_system, hostname))
        current_hosts = self.get(
            'v1', '/host?operating_system_type={}&primary_cluster_id=local&hostname={}'.format(operating_system, hostname), timeout)

        if current_hosts['total'] >= 1:
            for host in current_hosts['data']:
                if host['hostname'] == hostname:
                    host_id = host['id']
                    break
        try:
            host_id
        except NameError:
            sys.exit("Error: The Rubrik Cluster is not connected to a {} physical host named '{}'.".format(
                operating_system, hostname))

        self.log("manage_physical_host_protection: Searching the Rubrik Cluster for all current {} Filesets.".format(
            operating_system))
        current_filesets_templates = self.get('v1', '/fileset_template?primary_cluster_id=local&operating_system_type={}&name={}'.format(
            operating_system, fileset_name), timeout)

        number_of_matches = 0
        if current_filesets_templates['total'] == 0:
            sys.exit("Error: The Rubrik Cluster does not have a {} Fileset named '{}'.".format(operating_system, fileset_name))
        elif current_filesets_templates['total'] > 1:
            for fileset in current_filesets_templates['data']:
                if fileset['name'] == fileset_name:
                    number_of_matches += 1

            if number_of_matches > 1:
                sys.exit(
                    "Error: The Rubrik Cluster contains multiple {} Filesets named '{}'. Please populate all function arguments to find a more specific match.".format(operating_system, fileset_name))

        if current_filesets_templates['total'] == 1 or number_of_matches == 1:
            for template in current_filesets_templates['data']:
                if template['name'] == fileset_name:
                    fileset_template_id = template['id']

        self.log("manage_physical_host_protection: Searching the Rubrik Cluster for the SLA Domain '{}'.".format(sla_name))
        sla_id = self.object_id(sla_name, 'sla')

        self.log("manage_physical_host_protection: Getting the properties of the {} Fileset.".format(fileset_name))
        current_fileset = self.get(
            'v1', '/fileset?primary_cluster_id=local&host_id={}&template_id={}'.format(host_id, fileset_template_id), timeout)

        if current_fileset['total'] == 0:
            self.log("manage_physical_host_protection: Assigning the '{}' Fileset to the {} physical host '{}'.".format(
                fileset_name, operating_system, hostname))

            config = {}
            config['hostId'] = host_id
            config['templateId'] = fileset_template_id

            create_fileset = self.post('v1', '/fileset', config, timeout)
            fileset_id = create_fileset['id']

            config = {}
            config['configuredSlaDomainId'] = sla_id
            assign_sla = self.patch('v1', '/fileset/{}'.format(fileset_id), config, timeout)

            return (create_fileset, assign_sla)
        elif current_fileset['total'] == 1 and current_fileset['data'][0]['configuredSlaDomainId'] != sla_id:
            self.log("manage_physical_host_protection: Assigning the '{}' SLA Domain to the '{}' Fileset attached to the {} physical host '{}'.".format(
                sla_name, fileset_name, operating_system, hostname))
            fileset_id = current_fileset['data'][0]['id']
            config = {}
            config['configuredSlaDomainId'] = sla_id
            assign_sla = self.patch('v1', '/fileset/{}'.format(fileset_id), config, timeout)

            return assign_sla

        elif current_fileset['total'] == 1 and current_fileset['data'][0]['configuredSlaDomainId'] == sla_id:
            return "The {} Fileset '{}' is already assigned to the SLA Domain '{}' on the physical host '{}'.".format(operating_system, fileset_name, sla_name, hostname)
