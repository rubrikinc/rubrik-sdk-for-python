#!/usr/bin/env python3

import rubrik_polaris
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--password', dest='password', help = "Polaris Password", required=True)
parser.add_argument('-u', '--username', dest='username', help = "Polaris UserName", required=True)
parser.add_argument('-d', '--domain', dest='domain', help = "Polaris Domain", required=True)
parser.add_argument('-r', '--root', dest='root_domain', help = "Polaris Root Domain")
parser.add_argument('--insecure', help='Deactivate SSL Verification', action="store_true")

args = parser.parse_args()

rubrik = rubrik_polaris.PolarisClient(args.domain, args.username, args.password, root_domain=args.root_domain, insecure=args.insecure)
