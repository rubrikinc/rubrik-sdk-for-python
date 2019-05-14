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
This module contains the Rubrik SDK Physical class.
"""

from .api import Api
from .exceptions import InvalidParameterException, InvalidTypeException


class Physical(Api):
    """This class contains methods related to the managment of the Physical objects in the Rubrik cluster."""

    def add_physical_host(self, hostname, timeout=60):
        """Add a physical host to the Rubrik cluster.

        Arguments:
            hostname {str} or [list] -- The hostname(s) or IP Address(es) of the physical host you want to add to the Rubrik cluster.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {60})

        Returns:
            str -- No change requird. The host '`hostname`' is already connected to the Rubrik cluster.
            dict -- The full API response for `POST /v1/host`.
        """
        count_of_hosts = len(hostname)

        if(count_of_hosts == 0):
            raise InvalidParameterException("The provided hostname list is empty.")

        self.log('Searching the Rubrik cluster for the current hosts.')
        current_hosts = self.get('v1', '/host', timeout=timeout)

        if isinstance(hostname, list):

            for host in current_hosts['data']:
                for single_host in hostname:
                    if host['hostname'] == single_host:
                        hostname.remove(single_host)
                        self.log("The host '{}' is already connected to the Rubrik cluster. '{}' skipped.".format(
                            single_host, single_host))

            config = []

            self.log("Adding '{}' Physical Host(s)".format(count_of_hosts))

            if count_of_hosts != 0:
                for hosts in hostname:
                    config += [{
                        'hostname': hosts,
                        'hasAgent': True
                    }]

                self.log("Adding the following physical host(s): '{}'".format(hostname))
                return self.post('internal', '/host/bulk', config, timeout)
            else:
                return "No Change Required. All Hosts Already added or supplied list was empty"
        else:
            for host in current_hosts['data']:
                if host['hostname'] == hostname:
                    return "No change required. The host '{}' is already connected to the Rubrik cluster.".format(
                        hostname)

            config = {}
            config['hostname'] = hostname
            config['hasAgent'] = True

            self.log("Adding the host '{}' to the Rubrik cluster.".format(hostname))
            return self.post('v1', '/host', config, timeout)

    def delete_physical_host(self, hostname, timeout=120):
        """Delete a physical host from the Rubrik cluster.

        Arguments:
            hostname {str} -- The hostname or IP Address of the physical host you wish to remove from the Rubrik cluster.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {120})

        Returns:
            str -- No change required. The host '`hostname`' is not connected to the Rubrik cluster.
            dict -- The full API response for `DELETE /v1'/host/{host_id}`.
        """

        self.log('Searching the Rubrik cluster for the current hosts.')
        current_hosts = self.get('v1', '/host', timeout=timeout)

        host_present = False

        for host in current_hosts['data']:
            if host['hostname'] == hostname:
                host_present = True
                host_id = host['id']
                break

        if not host_present:
            return "No change required. The host '{}' is not connected to the Rubrik cluster.".format(
                hostname)

        self.log(
            "Deleting the host '{}' from the Rubrik cluster.".format(hostname))
        return self.delete('v1', '/host/{}'.format(host_id), timeout=timeout)

    def create_physical_fileset(self, name, operating_system, include, exclude, exclude_exception, follow_network_shares=False, backup_hidden_folders=False, timeout=15):  # pylint: ignore
        """Create a Fileset for a Linux or Windows machine.

        Arguments:
            name {str} -- The name of the Fileset you wish to create.
            operating_system {str} -- The operating system type of the Fileset you are creating. (choices: {Linux, Windows.})
            include {list} -- The full paths or wildcards that define the objects to include in the Fileset backup (ex: ['/usr/local', '*.pdf']).
            exclude {list} -- The full paths or wildcards that define the objects to exclude from the Fileset backup (ex: ['/user/local/temp', '*.mov', '*.mp3']).
            exclude_exception {list} -- The full paths or wildcards that define the objects that are exempt from the `excludes` variables. (ex. ['/company/*.mp4').

        Keyword Arguments:
            follow_network_shares {bool} -- Include or exclude locally-mounted remote file systems from backups. (default: {False})
            backup_hidden_folders {bool} -- Include or exclude hidden folders inside locally-mounted remote file systems from backups. (default: {False})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            str -- No change required. The Rubrik cluster already has a `operating_system` Fileset named '`name`' configured with the provided variables.
            dict -- The full response for the `POST /internal/fileset_template/bulk` API endpoint.
        """

        valid_operating_system = ['Linux', 'Windows']

        if operating_system not in valid_operating_system:
            raise InvalidParameterException("The create_physical_fileset() operating_system argument must be one of the following: {}.".format(
                valid_operating_system))

        if isinstance(follow_network_shares, bool) is False:
            raise InvalidTypeException(
                "The 'follow_network_shares' argument must be True or False.")
        elif isinstance(backup_hidden_folders, bool) is False:
            raise InvalidTypeException(
                "The 'backup_hidden_folders' argument must be True or False.")
        elif isinstance(include, list) is False:
            raise InvalidTypeException("The 'include' argument must be a list object.")
        elif isinstance(exclude, list) is False:
            raise InvalidTypeException("The 'exclude' argument must be a list object.")
        elif isinstance(exclude_exception, list) is False:
            raise InvalidTypeException(
                "The 'exclude_exception' argument must be a list object.")

        config = {}
        config['name'] = name
        config['includes'] = sorted(include)
        config['excludes'] = sorted(exclude)
        config['exceptions'] = sorted(exclude_exception)
        config['allowBackupHiddenFoldersInNetworkMounts'] = backup_hidden_folders
        config['allowBackupNetworkMounts'] = follow_network_shares
        config['operatingSystemType'] = operating_system

        self.log("create_fileset: Searching the Rubrik cluster for all current {} Filesets.".format(
            operating_system))
        current_filesets = self.get(
            'v1', '/fileset_template?primary_cluster_id=local&operating_system_type={}&name={}'.format(operating_system, name), timeout=timeout)

        current_config = {}
        if current_filesets['data']:
            current_config['name'] = current_filesets['data'][0]['name']
            current_config['includes'] = sorted(
                current_filesets['data'][0]['includes'])
            current_config['excludes'] = sorted(
                current_filesets['data'][0]['excludes'])
            current_config['exceptions'] = sorted(
                current_filesets['data'][0]['exceptions'])
            current_config['allowBackupHiddenFoldersInNetworkMounts'] = current_filesets['data'][0]['allowBackupHiddenFoldersInNetworkMounts']
            current_config['operatingSystemType'] = current_filesets['data'][0]['operatingSystemType']
            current_config['allowBackupNetworkMounts'] = current_filesets['data'][0]['allowBackupNetworkMounts']

        if current_config == config:
            return "No change required. The Rubrik cluster already has a {} Fileset named '{}' configured with the provided variables.".format(
                operating_system, name)

        # Add the config dict to a list
        model = []
        model.append(config)

        self.log("create_fileset: Creating the '{}' Fileset.".format(name))
        return self.post(
            'internal',
            '/fileset_template/bulk',
            model,
            timeout=timeout)

    def create_nas_fileset(self, name, share_type, include, exclude, exclude_exception, follow_network_shares=False, timeout=15):  # pylint: ignore
        """Create a NAS Fileset.

        Arguments:
            name {str} -- The name of the Fileset you wish to create.
            share_type {str} -- The type of NAS Share you wish to backup. (choices: {NFS, SMB})
            include {list} -- The full paths or wildcards that define the objects to include in the Fileset backup.
            exclude {list} -- The full paths or wildcards that define the objects to exclude from the Fileset backup.
            exclude_exception {list} -- The full paths or wildcards that define the objects that are exempt from the `excludes` variables.

        Keyword Arguments:
            follow_network_shares {bool} -- Include or exclude locally-mounted remote file systems from backups. (default: {False})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            str -- No change required. The Rubrik cluster already has a NAS Fileset named '`name`' configured with the provided variables.
            dict -- The full response for the `POST /internal/fileset_template/bulk` API endpoint.
        """

        valid_share_type = ['NFS', 'SMB']

        if share_type not in valid_share_type:
            raise InvalidParameterException("The create_fileset() share_type argument must be one of the following: {}.".format(
                valid_share_type))

        if isinstance(follow_network_shares, bool) is False:
            raise InvalidTypeException(
                "The 'follow_network_shares' argument must be True or False.")
        elif isinstance(include, list) is False:
            raise InvalidTypeException("The 'include' argument must be a list object.")
        elif isinstance(exclude, list) is False:
            raise InvalidTypeException("The 'exclude' argument must be a list object.")
        elif isinstance(exclude_exception, list) is False:
            raise InvalidTypeException(
                "The 'exclude_exception' argument must be a list object.")

        config = {}
        config['name'] = name
        config['includes'] = sorted(include)
        config['excludes'] = sorted(exclude)
        config['exceptions'] = sorted(exclude_exception)
        config['allowBackupHiddenFoldersInNetworkMounts'] = follow_network_shares
        config['shareType'] = share_type

        self.log(
            "create_fileset: Searching the Rubrik cluster for all current NAS Filesets.")
        current_filesets = self.get(
            'v1', '/fileset_template?primary_cluster_id=local&operating_system_type=NONE&name={}'.format(name), timeout=timeout)

        current_config = {}
        if current_filesets['data']:
            current_config['name'] = current_filesets['data'][0]['name']
            current_config['includes'] = sorted(
                current_filesets['data'][0]['includes'])
            current_config['excludes'] = sorted(
                current_filesets['data'][0]['excludes'])
            current_config['exceptions'] = sorted(
                current_filesets['data'][0]['exceptions'])
            current_config['allowBackupHiddenFoldersInNetworkMounts'] = current_filesets['data'][0]['allowBackupHiddenFoldersInNetworkMounts']
            current_config['shareType'] = current_filesets['data'][0]['shareType']

        if current_config == config:
            return "No change required. The Rubrik cluster already has a NAS Fileset named '{}' configured with the provided variables.".format(
                name)

        # Add the config dict to a list
        model = []
        model.append(config)

        self.log("create_fileset: Creating the '{}' Fileset.".format(name))
        return self.post(
            'internal',
            '/fileset_template/bulk',
            model,
            timeout=timeout)

    def assign_physical_host_fileset(self, hostname, fileset_name, operating_system, sla_name, include=None, exclude=None, exclude_exception=None, follow_network_shares=False, backup_hidden_folders=False, timeout=30):  # pylint: ignore
        """Assign a Fileset to a Linux or Windows machine. If you have multiple Filesets with identical names, you will need to populate the Filesets properties (i.e this functions keyword arguments)
        to find a specific match. Filesets with identical names and properties are not supported.

        Arguments:
            hostname {str} -- The hostname or IP Address of the physical host you wish to associate to the Fileset.
            fileset_name {str} -- The name of the Fileset you wish to assign to the Linux or Windows host.
            operating_system {str} -- The operating system of the physical host you are assigning a Fileset to. (choices: {Linux, Windows})
            sla_name {str} -- The name of the SLA Domain to associate with the Fileset.

        Keyword Arguments:
            include {list} -- The full paths or wildcards that define the objects to include in the Fileset backup (ex: ['/usr/local', '*.pdf']). (default: {None})
            exclude {list} -- The full paths or wildcards that define the objects to exclude from the Fileset backup (ex: ['/user/local/temp', '*.mov', '*.mp3']). (default: {None})
            exclude_exception {list} -- The full paths or wildcards that define the objects that are exempt from the `excludes` variables. (ex: ['/company/*.mp4']). (default: {None})
            follow_network_shares {bool} -- Include or exclude locally-mounted remote file systems from backups. (default: {False})
            backup_hidden_folders {bool} -- Include or exclude hidden folders inside locally-mounted remote file systems from backups. (default: {False})
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {30})

        Returns:
            str -- No change required. The `operating_system` Fileset '`fileset_name`' is already assigned to the SLA Domain '`sla_name`' on the physical host '`hostname`'.
            tuple -- When a new Fileset is created the following tuple will be returned: (Full API response from `POST /v1/fileset`, Full API response from `POST /v1/fileset/{id}`)
            dict -- When the Fileset already exsits but is assigned to the wrong the SLA the Full API response from `POST `v1/fileset/{id}` is returned.
        """

        valid_operating_system = ['Linux', 'Windows']

        if operating_system not in valid_operating_system:
            raise InvalidParameterException("The create_physical_fileset() operating_system argument must be one of the following: {}.".format(
                valid_operating_system))

        if include is None:
            include = []

        if exclude is None:
            exclude = []

        if exclude_exception is None:
            exclude_exception = []

        if isinstance(follow_network_shares, bool) is False:
            raise InvalidTypeException(
                "The 'follow_network_shares' argument must be True or False.")
        elif isinstance(backup_hidden_folders, bool) is False:
            raise InvalidTypeException(
                "The 'backup_hidden_folders' argument must be True or False.")
        elif isinstance(include, list) is False:
            raise InvalidTypeException("The 'include' argument must be a list object.")
        elif isinstance(exclude, list) is False:
            raise InvalidTypeException("The 'exclude' argument must be a list object.")
        elif isinstance(exclude_exception, list) is False:
            raise InvalidTypeException(
                "The 'exclude_exception' argument must be a list object.")

        self.log(
            "assign_physical_host_fileset: Searching the Rubrik cluster for the {} physical host {}.".format(
                operating_system,
                hostname))
        current_hosts = self.get(
            'v1', '/host?operating_system_type={}&primary_cluster_id=local&hostname={}'.format(operating_system, hostname), timeout=timeout)

        if current_hosts['total'] >= 1:
            for host in current_hosts['data']:
                if host['hostname'] == hostname:
                    host_id = host['id']
                    break
        try:
            host_id
        except NameError:
            raise InvalidParameterException(
                "The Rubrik cluster is not connected to a {} physical host named '{}'.".format(
                    operating_system, hostname))

        self.log("assign_physical_host_fileset: Searching the Rubrik cluster for all current {} Filesets.".format(
            operating_system))
        current_filesets_templates = self.get(
            'v1', '/fileset_template?primary_cluster_id=local&operating_system_type={}&name={}'.format(operating_system, fileset_name), timeout=timeout)

        number_of_matches = 0
        if current_filesets_templates['total'] == 0:
            raise InvalidParameterException(
                "The Rubrik cluster does not have a {} Fileset named '{}'.".format(
                    operating_system, fileset_name))
        elif current_filesets_templates['total'] > 1:
            for fileset_template in current_filesets_templates['data']:
                if fileset_template['name'] == fileset_name:
                    number_of_matches += 1

            if number_of_matches > 1:
                # If there are multiple Filesets with the same name us all of
                # the possible config values to try and find the correct
                # Fileset
                number_of_matches = 0
                for fileset_template in current_filesets_templates['data']:
                    if fileset_template['name'] == fileset_name \
                            and fileset_template['includes'] == include \
                            and fileset_template['excludes'] == exclude \
                            and fileset_template['exceptions'] == exclude_exception \
                            and fileset_template['allowBackupHiddenFoldersInNetworkMounts'] == follow_network_shares \
                            and fileset_template['allowBackupNetworkMounts'] == backup_hidden_folders:
                        fileset_template_id = fileset_template['id']
                        number_of_matches = 1

                try:
                    fileset_template_id
                except NameError:
                    if number_of_matches > 0:
                        # If no unique matches are found provide an error
                        # message
                        if include != [] \
                                or exclude != [] \
                                or exclude_exception != [] \
                                or follow_network_shares\
                                or backup_hidden_folders:
                            # Error message that first checks to see if any of
                            # the extra variables are populated with anything
                            # besides the default (aka the user tried to be as
                            # unique as possible)
                            raise InvalidParameterException(
                                "The Rubrik cluster contains multiple {} Filesets named '{}' that match all of the populate function arguments. Please use a unique Fileset.".format(
                                    operating_system, fileset_name))
                        else:
                            raise InvalidParameterException(
                                "The Rubrik cluster contains multiple {} Filesets named '{}'. Please populate all function arguments to find a more specific match.".format(
                                    operating_system, fileset_name))
                    raise InvalidParameterException(
                        "The Rubrik cluster contains multiple {} Filesets named '{}'. Please populate all function arguments to find a more specific match.".format(
                            operating_system,
                            fileset_name))

        if current_filesets_templates['total'] == 1 or number_of_matches == 1:
            for fileset_temmplate in current_filesets_templates['data']:
                if fileset_temmplate['name'] == fileset_name:
                    fileset_template_id = fileset_temmplate['id']

        self.log(
            "assign_physical_host_fileset: Searching the Rubrik cluster for the SLA Domain '{}'.".format(sla_name))
        sla_id = self.object_id(sla_name, 'sla', timeout=timeout)

        self.log("assign_physical_host_fileset: Getting the properties of the {} Fileset.".format(
            fileset_name))
        current_fileset = self.get(
            'v1', '/fileset?primary_cluster_id=local&host_id={}&is_relic=false&template_id={}'.format(host_id, fileset_template_id), timeout=timeout)

        if current_fileset['total'] == 0:
            self.log(
                "assign_physical_host_fileset: Assigning the '{}' Fileset to the {} physical host '{}'.".format(
                    fileset_name,
                    operating_system,
                    hostname))

            config = {}
            config['hostId'] = host_id
            config['templateId'] = fileset_template_id

            create_fileset = self.post('v1', '/fileset', config, timeout)
            fileset_id = create_fileset['id']

            config = {}
            config['configuredSlaDomainId'] = sla_id
            assign_sla = self.patch(
                'v1', '/fileset/{}'.format(fileset_id), config, timeout)

            return (create_fileset, assign_sla)
        elif current_fileset['total'] == 1 and current_fileset['data'][0]['configuredSlaDomainId'] != sla_id:

            self.log(
                "assign_physical_host_fileset: Assigning the '{}' SLA Domain to the '{}' Fileset attached to the {} physical host '{}'.".format(
                    sla_name,
                    fileset_name,
                    operating_system,
                    hostname))
            fileset_id = current_fileset['data'][0]['id']
            config = {}
            config['configuredSlaDomainId'] = sla_id
            return self.patch(
                'v1',
                '/fileset/{}'.format(fileset_id),
                config,
                timeout)

        elif current_fileset['total'] == 1 and current_fileset['data'][0]['configuredSlaDomainId'] == sla_id:
            return "No change required. The {} Fileset '{}' is already assigned to the SLA Domain '{}' on the physical host '{}'.".format(
                operating_system, fileset_name, sla_name, hostname)
