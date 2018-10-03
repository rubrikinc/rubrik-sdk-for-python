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
This module contains the Rubrik SDK SupportBundle class.
"""

import os
import sys
from datetime import timedelta
import sqlite3
import requests
from dateutil import parser
from .api import Api

_API = Api


class SupportBundle(_API):
    """This Class contains methods related to the generation and download of
    Support Bundles"""

    def _db_q_event_id(self, event_id):
        """Internal method to query the local internal database for existing EventIDs so that duplicate generation jobs are not executed.

        Arguments:
            event_id {str} -- The `eventSeriesId` returned by the `/internal/event` endpoint.

        Returns:
            tuple -- The row(s) from the database containing the EventID in question.
        """
        try:
            data = self.db_curs.execute(  # pylint: disable=no-member
                """SELECT * FROM support_bundle WHERE
                event_id=?""",
                (event_id,),
            )
            return data.fetchall()
        except sqlite3.Error as err:
            sys.exit("Error querying database - {}".format(err))

    def _db_u_bun_state(self, job_id, bun_status):
        """Internal method to update the local internal database with the status of the Bundle.

        Arguments:
            job_id {str} -- JobID of the `SUPPORT_BUNDLE_GENERATOR` job.
            bun_status {str} -- Status of the Bundle
            (`GENERATING` / `DOWNLOADED`).
        """
        try:
            self.db_curs.execute(  # pylint: disable=no-member
                """UPDATE support_bundle
                SET status=?
                WHERE job_id=?""",
                (bun_status, job_id),
            )
            self.conn.commit()  # pylint: disable=no-member
        except sqlite3.Error as err:
            sys.exit("Error updating database - {}".format(err))

    def _db_u_job_state(self, job_id, job_state):
        """Internal method to update the local internal database with the status of the `SUPPORT_BUNDLE_GENERATOR` job.

        Arguments:
            job_id {str} -- JobID of the `SUPPORT_BUNDLE_GENERATOR` job.
            job_state {str} -- Status of the `SUPPORT_BUNDLE_GENERATOR` job as
            retrieved from the `/internal/support/support_bundle` endpoint.
        """
        try:
            self.db_curs.execute(  # pylint: disable=no-member
                """UPDATE support_bundle
                SET job_state=?
                WHERE job_id=?""",
                (job_state, job_id),
            )
            self.conn.commit()  # pylint: disable=no-member
        except sqlite3.Error as err:
            sys.exit("Error updating database - {}".format(err))

    def _db_a_event_id(self, data):
        """Internal method to add a new EventID to the local internal database.

        Arguments:
            data {dict} -- Dictionary containing event_id, job_id, job_state, expiry_time, status.
        """
        try:
            event_id = data["event_id"]
            job_id = data["job_id"]
            job_state = data["state"]
            expiry_time = data["expiry_time"]
            status = data["status"]
            self.db_curs.execute(  # pylint: disable=no-member
                """INSERT INTO support_bundle
                (event_id, job_id, job_state, expiry_time, status)
                VALUES (?, ?, ?, ?, ?)""",
                (event_id, job_id, job_state, expiry_time, status),
            )
            self.conn.commit()  # pylint: disable=no-member
        except sqlite3.Error as err:
            sys.exit("Error adding row - {}".format(err))
        except KeyError as err:
            sys.exit("Error populating data - {}".format(err))

    def _db_d_event_id(self, event_id):
        """Internal method to delete an EventID from the local internal database due to `SUPPORT_BUNDLE_GENERATOR` job failure or age.

        Arguments:
            event_id {str} -- EventID to remove from the database.
        """
        try:
            self.log(  # pylint: disable=no-member
                "Deleting row for Event ID {}".format(event_id)
            )
            self.db_curs.execute(  # pylint: disable=no-member
                """DELETE FROM support_bundle WHERE
                event_id=?""",
                (event_id,),
            )
            self.conn.commit()  # pylint: disable=no-member
        except sqlite3.Error as err:
            sys.exit("Error deleting row - {}".format(err))

    def _db_q_backlog(self):
        """Internal method to query the local internal database for all existing EventIDs that have pending `SUPPORT_BUNDLE_GENERATOR` jobs.

        Returns:
            tuple -- The row(s) from the database containing EventIDs with `SUPPORT_BUNDLE_GENERATOR` jobs in a `GENERATING` status.
        """
        try:
            data = self.db_curs.execute(  # pylint: disable=no-member
                """SELECT * FROM support_bundle WHERE
                status=?""",
                ("GENERATING",),
            )
            return data.fetchall()
        except sqlite3.Error as err:
            sys.exit("Error querying database - {}".format(err))

    def _download(self, bundle_job, bundle_url):
        """Internal method to download the generated Support Bundle to your local machine.

        Arguments:
            bundle_job {str} -- JobID of a `SUPPORT_BUNDLE_GENERATOR` job.
            bundle_url {str} -- URL to the generated Support Bundle as retrieved from the `/internal/support/support_bundle` API endpoint.
        """
        home_dir = os.path.expanduser("~")
        dl_dir = home_dir + "/Downloads/"
        if bundle_url.find("/"):
            file_name = bundle_url.rsplit("/", 1)[1]
            dl_path = dl_dir + file_name
            if not os.path.isfile(dl_path):
                try:
                    dl_req = requests.get(
                        bundle_url, verify=False, allow_redirects=True
                    )
                    self.log(  # pylint: disable=no-member
                        "Downloading to {}".format(dl_path)
                    )
                    open(dl_path, "wb").write(dl_req.content)
                    self._db_u_bun_state(bundle_job, "DOWNLOADED")
                except requests.exceptions.RequestException as err:
                    self.log(  # pylint: disable=no-member
                        "Error while downloading {} - {}".format(
                            bundle_url, err
                        )
                    )
            else:
                self.log(  # pylint: disable=no-member
                    "{} already exists".format(dl_path)
                )
                self._db_u_bun_state(bundle_job, "DOWNLOADED")

    def _status(self, bundle_job):
        """Internal method to retrieve the status of a `SUPPORT_BUNDLE_GENERATOR` job.

        Arguments:
            bundle_job {str} -- JobID of a `SUPPORT_BUNDLE_GENERATOR` job.

        Returns:
            str -- The status of the `SUPPORT_BUNDLE_GENERATOR` job, or an error if the API was unable to find the JobID.
        """
        api_data = self.get(
            "internal", "/support/support_bundle?id={}".format(bundle_job)
        )
        if "Could not find JobInstance" not in api_data:
            job_status = api_data["status"]
            self.log(  # pylint: disable=no-member
                "Job {} Status: {}".format(bundle_job, job_status)
            )
            self._db_u_job_state(bundle_job, job_status)
            if job_status == "SUCCEEDED":
                for data in api_data["links"]:
                    if "rubrik_job" in data["href"]:
                        bundle_url = data["href"]
                        self._download(bundle_job, bundle_url)
        else:
            job_status = api_data
        return job_status

    def _generate(self, event_id):
        """Internal method to generate a Support Bundle for a given EventID.

        Arguments:
            event_id {str} -- The `eventSeriesId` returned by the `/internal/event` endpoint.
        """
        check_event = self._db_q_event_id(event_id)
        if check_event:
            bun_status = check_event[0][-1]
            if bun_status == "GENERATING":
                self.log(  # pylint: disable=no-member
                    "Support Bundle generation for {} is in progress".format(
                        event_id
                    )
                )
                job_status = self._status(check_event[0][1])
                if job_status == "FAILED":
                    self._db_d_event_id(event_id)
                    self._generate(event_id)
                elif "Could not find JobInstance" in job_status:
                    self._db_d_event_id(event_id)
                elif job_status != "SUCCEEDED":
                    self.log(  # pylint: disable=no-member
                        "Request for EventID {} {}".format(
                            event_id, job_status
                        )
                    )
        else:
            self.log(  # pylint: disable=no-member
                "Generating Support Bundle for EventID {}".format(event_id)
            )
            data = {"eventId": "{}".format(event_id)}
            api_data = self.post("internal", "/support/support_bundle", data)
            bundle_info = {}
            start_time = parser.parse(api_data["startTime"])
            expiry_time = start_time + timedelta(hours=24)
            bundle_info["event_id"] = event_id
            bundle_info["job_id"] = api_data["id"]
            bundle_info["state"] = api_data["status"]
            bundle_info["expiry_time"] = expiry_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            bundle_info["status"] = "GENERATING"
            self._db_a_event_id(bundle_info)

    def support_bundle_backlog(self):
        """Process all EventIDs with pending `SUPPORT_BUNDLE_GENERATOR` jobs.
        """
        events = self._db_q_backlog()
        if events:
            self.log(  # pylint: disable=no-member
                "{} Bundles in backlog".format(len(events))
            )
            for event in events:
                event_id = event[0]
                job_id = event[1]
                status = self._status(job_id)
                if status == "FAILED":
                    self._db_d_event_id(event_id)
                    self._generate(event_id)
        else:
            self.log("0 Bundles in backlog")  # pylint: disable=no-member

    def support_bundle(self, event_id=None, events=None):
        """Generate/Download a Support Bundle for the specified EventID(s).

        Keyword Arguments:
            event_id {str} -- EventID (`eventSeriesId`) to generate a Support Bundle for.
            events {dict} -- Dictionary of events returned by the `Events.get_events` method.
        """
        if events:
            for event in events:
                event_id = event["eventSeriesId"]
                self._generate(event_id)
        elif event_id:
            self._generate(event_id)
        else:
            sys.exit(
                "Provide event_id (str) or events (dict) to this method."
            )
