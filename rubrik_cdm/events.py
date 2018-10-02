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


class Events(_API):
    """This class contains methods related to Cluster/Object Events from the Rubrik Cluster."""

    def get_events(self, limit=10, status=None, event_type=None, object_type=None, object_name=None, before_date=None, after_date=None):
        """Return a list of Events matching the specified criteria.

        Keyword Arguments:
            limit {int} -- The limit of Events to return. Accepted limit is between 1-15. (Default 10)
            status {str} -- Filter the events by Status (Choices: {Failure}, {Warning}, {Running}, {Success}, {Canceled}, {Canceling})
            event_type {str} -- Filter the events by Event Type (Choices: {Archive}, {Audit}, {AuthDomain}, {Backup}, {CloudNativeSource}, {Configuration}, {Diagnostic}, {Instantiate}, {Maintenance}, {NutanixCluster}, {Recovery}, {Replication}, {StorageArray}, {System}, {Vcd}, {VCenter})
            object_type {str} -- Filter the events by Object Type (Choices: {VmwareVm}, {Mssql}, {LinuxFileset}, {WindowsFileset}, {WindowsHost}, {LinuxHost}, {StorageArrayVolumeGroup}, {VolumeGroup}, {NutanixVm}, {AwsAccount}, {Ec2Instance})
            object_name {str} -- Filter the events by Object Name (Can be the name of a VM, Host, Fileset, Mssql Database, etc)
            before_date {datetime} -- Only show events before specified date. (Ex. 2018-10-01)
            after_date {datetime} -- Only show events after specified date. (Ex. 2018-10-01)

        Returns:
            dict -- The `data` object within the API response for `GET /internal/event/` after applying the specified filters.
        """
        valid_limit = range(1, 16)
        valid_status = [
            None,
            "Failure",
            "Warning",
            "Running",
            "Success",
            "Canceled",
            "Canceling",
        ]
        valid_event_type = [
            None,
            "Archive",
            "Audit",
            "AuthDomain",
            "Backup",
            "CloudNativeSource",
            "Configuration",
            "Diagnostic",
            "Instantiate",
            "Maintenance",
            "NutanixCluster",
            "Recovery",
            "Replication",
            "StorageArray",
            "System",
            "Vcd",
            "VCenter",
        ]
        valid_object_type = [
            None,
            "VmwareVm",
            "Mssql",
            "LinuxFileset",
            "WindowsFileset",
            "WindowsHost",
            "LinuxHost",
            "StorageArrayVolumeGroup",
            "VolumeGroup",
            "NutanixVm",
            "AwsAccount",
            "Ec2Instance",
        ]

        if limit not in valid_limit:
            sys.exit(
                "Error: Event Limit must be between {} and {}".format(
                    valid_limit[0], len(valid_limit)
                )
            )

        if status not in valid_status:
            sys.exit(
                "Error: Event Status must be one of the following - {}".format(
                    valid_status
                )
            )

        if event_type not in valid_event_type:
            sys.exit(
                "Error: Event Type must be one of the following - {}".format(
                    valid_event_type
                )
            )

        if object_type not in valid_object_type:
            sys.exit(
                "Error: Event Object must be one of the following - {}".format(
                    valid_object_type
                )
            )

        self.log("Querying the Rubrik API for the specified event criteria")
        event_data = {}
        event_data["limit"] = limit
        event_data["status"] = status
        event_data["event_type"] = event_type
        event_data["object_name"] = object_name
        event_data["before_date"] = before_date
        event_data["after_date"] = after_date
        event_url = "/event?"
        for param in event_data:
            if event_data[param]:
                event_url += "{}={}&".format(param, event_data[param])
        api_request = self.get("internal", event_url)
        return api_request["data"]
