
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

from .api import Api
import inspect


class Organization(Api):
    """This class contains methods related to backup and restore operations for the various objects managed by the Rubrik cluster."""

    def add_organization_protectable_object_mssql_server_host(self, organization_name, mssql_host, timeout=15):
        """Add a MSSQL Server Host to an organization as a protectable object.

        Arguments:
            organization_name {str} -- The name of the organization you wish to add the protectable object to.
            mssql_host {str} -- The name of the MSSQL Host to add to the organization as a protectable object.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            str -- No change required. The MSSQL host {mssql_host} is already assigned to the {organization_name} organization.
            dict -- The full API response for `POST /internal/role/{id}/authorization`
        """

        self.function_name = inspect.currentframe().f_code.co_name

        organization_id = self.object_id(
            organization_name, "organization", timeout=timeout)

        org_admin_id = self.object_id(
            organization_name, "organization_admin_role", timeout=timeout)

        self.log("add_organization_protectable_object_sql_server: Gathering the current MSSQL objects protected by the {} organization.".format(
            organization_name))
        current_mssql_protected_objects = self.get(
            "internal", "/organization/{}/mssql".format(organization_id), timeout=timeout)

        objects_to_protect = []

        sql_host_id = self.object_id(
            mssql_host, "physical_host", timeout=timeout)

        for protected_object in current_mssql_protected_objects["data"]:
            if protected_object["managedId"] == sql_host_id:
                return "No change required. The MSSQL host {} is already assigned to the {} organization.".format(mssql_host, organization_name)

        objects_to_protect.append(sql_host_id)

        config = {
            "authorizationSpecifications": [
                {
                    "privilege": "ManageRestoreSource",
                    "resources": objects_to_protect
                }
            ],
            "roleTemplate": "Organization"
        }

        return self.post("internal", "/role/{}/authorization".format(org_admin_id), config, timeout=timeout)

    def add_organization_protectable_object_sql_server_db(self, organization_name, mssql_db, mssql_host, mssql_instance, timeout=15):
        """Add a MSSQL Database to an organization as a protectable object.

        Arguments:
            organization_name {str} -- The name of the organization you wish to add the protectable object to.
            mssql_db {str} -- The name of the MSSQL DB to add to the organization as a protectable object.
            mssql_instance {str} -- The name of the MSSQL instance where the MSSQL DB lives.
            mssql_host {str} -- The name of the MSSQL host where the MSSQL DB lives.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            str -- No change required. The MSSQL DB {mssql_db} is already assigned to the {organization_name} organization.
            dict -- The full API response for `POST /internal/role/{id}/authorization`
        """

        self.function_name = inspect.currentframe().f_code.co_name

        organization_id = self.object_id(
            organization_name, "organization", timeout=timeout)

        org_admin_id = self.object_id(
            organization_name, "organization_admin_role", timeout=timeout)

        self.log("add_organization_protectable_object_sql_server: Gathering the current MSSQL objects protected by the {} organization.".format(
            organization_name))
        current_mssql_protected_objects = self.get(
            "internal", "/organization/{}/mssql".format(organization_id), timeout=timeout)

        objects_to_protect = []

        db_id = self.object_id(
            mssql_db, "mssql_db", mssql_instance=mssql_instance, mssql_host=mssql_host, timeout=timeout)

        for protected_object in current_mssql_protected_objects["data"]:
            if protected_object["managedId"] == db_id:
                return "No change required. The MSSQL DB {} is already assigned to the {} organization.".format(mssql_db, organization_name)

        objects_to_protect.append(db_id)

        config = {
            "authorizationSpecifications": [
                {
                    "privilege": "ManageRestoreSource",
                    "resources": objects_to_protect
                }
            ],
            "roleTemplate": "Organization"
        }

        return self.post("internal", "/role/{}/authorization".format(org_admin_id), config, timeout=timeout)

    def add_organization_protectable_object_sql_server_availability_group(self, organization_name, mssql_availability_group, timeout=15):
        """Add a MSSQL Availability Group to an organization as a protectable object.

        Arguments:
            organization_name {str} -- The name of the organization you wish to add the protectable object to.
            mssql_availability_group {str} -- The name of the MSSQL Availability Group to add to the organization as a protectable object.

        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})

        Returns:
            str -- No change required. The MSSQL Availability Group {mssql_availability_group} is already assigned to the {organization_name} organization.
            dict -- The full API response for `POST /internal/role/{id}/authorization`
        """

        self.function_name = inspect.currentframe().f_code.co_name

        organization_id = self.object_id(
            organization_name, "organization", timeout=timeout)

        org_admin_id = self.object_id(
            organization_name, "organization_admin_role", timeout=timeout)

        self.log("add_organization_protectable_object_sql_server: Gathering the current MSSQL objects protected by the {} organization.".format(
            organization_name))
        current_mssql_protected_objects = self.get(
            "internal", "/organization/{}/mssql".format(organization_id), timeout=timeout)

        objects_to_protect = []

        ag_id = self.object_id(
            mssql_availability_group, "mssql_availability_group", timeout=timeout)

        for protected_object in current_mssql_protected_objects["data"]:
            if protected_object["managedId"] == ag_id:
                return "No change required. The MSSQL Availability Group {} is already assigned to the {} organization.".format(mssql_availability_group, organization_name)

        objects_to_protect.append(ag_id)

        config = {
            "authorizationSpecifications": [
                {
                    "privilege": "ManageRestoreSource",
                    "resources": objects_to_protect
                }
            ],
            "roleTemplate": "Organization"
        }

        return self.post("internal", "/role/{}/authorization".format(org_admin_id), config, timeout=timeout)
