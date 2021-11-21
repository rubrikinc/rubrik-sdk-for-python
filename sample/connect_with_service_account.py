"""Create a session token for a given appliance with a service account,
and retrieve cluster version string from the appliance API.

This sample script needs 3 pieces of information to run:
 1. the location of a service account JSON file (that you downloaded from
    the UI when creating a service account);
 2. the unique identifier of the appliance (typically, the cluster UUID);
 3. the appliance node IP (typically, a cluster node IP address).

 If --sdk is given as a command line option, then the appliance token
 is retrieved using the rubrik_polaris SDK. If not given, then it is
 retrieved with a bare HTTP POST.
"""
from argparse import ArgumentParser
from os import environ
from pathlib import Path
from typing import Dict
import requests
import urllib3
import json
import rubrik_cdm


def get_appliance_token(use_sdk: bool, sa_conf_file, appliance_uuid) -> str:
    if use_sdk:
        from rubrik_polaris import ServiceAccount

        # Create a service account from configuration:
        sa = ServiceAccount.from_json_file(sa_conf_file)

        # Retrieve a token from the appliance:
        session_id, token, expiration = \
            sa.get_appliance_token(appliance_uuid)
    else:
        sa_conf = json.loads(Path(sa_conf_file).expanduser().read_text())
        r = requests.post(
            url=sa_conf['access_token_uri'].replace(
                '/client_token', '/cdm_client_token'),
            json=dict(
                client_id=sa_conf['client_id'],
                client_secret=sa_conf['client_secret'],
                cluster_uuid=appliance_uuid
            ),
            headers={
                'Content-Type': 'application/json;charset=UTF-8',
                'Accept': 'application/json, text/plain'
            }
        )
        # In case of error, response is guaranteed to include error message
        if r.status_code >= 400:
            raise requests.HTTPError(r.text)
        session: Dict[str] = r.json()['session']
        session_id = session['id']
        token = session['token']
        expiration = session['expiration']

    print(f'Appliance token:\n'
          f'  id: {session_id}\n'
          f'  token: {token}\n'
          f'  expiration: {expiration}\n')
    return token


def print_cluster_version(appliance_node_ip, token):
    # Test the appliance token:
    # retrieve the version string from the cluster node:
    environ['rubrik_cdm_node_ip'] = appliance_node_ip
    environ['rubrik_cdm_token'] = token
    environ.pop('rubrik_cdm_username', None)
    environ.pop('rubrik_cdm_password', None)
    rubrik = rubrik_cdm.Connect()
    print('rubrik_cdm.Connect().cluster_version()')
    cluster_version = rubrik.cluster_version()
    print('Cluster version: ', cluster_version)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('conf_file', type=Path,
                        help='Path to service account JSON file.')
    parser.add_argument('uuid',
                        help='Appliance/cluster UUID')
    parser.add_argument('node_ip',
                        help='Appliance/cluster node IP address or hostname')
    parser.add_argument('-k', '--insecure', action="store_true", default=False,
                        help='Allow connections to be insecure.')
    parser.add_argument('-s', '--sdk', action="store_true", default=False,
                        help='Use rubrik_polaris SDK to retrieve token.')
    args = parser.parse_args()
    if args.insecure:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    cluster_token = get_appliance_token(args.sdk, args.conf_file, args.uuid)
    print_cluster_version(args.node_ip, cluster_token)
