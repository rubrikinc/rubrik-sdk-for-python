import rubrik_cdm
import urllib3
import json
import os

urllib3.disable_warnings()

#os.environ['rubrik_cdm_node_ip'] = 'emea2-rbk01.rubrikdemo.com'
#os.environ['rubrik_cdm_username'] = 'ej.doezie@rubrikdemo.com'
#os.environ['rubrik_cdm_password'] = 'RubrikGoForward!'
os.environ['rubrik_cdm_node_ip'] = '10.10.60.201'
os.environ['rubrik_cdm_username'] = 'admin'
os.environ['rubrik_cdm_password'] = 'RubrikGoForward'

RubrikConn = rubrik_cdm.Connect()
clustervers = RubrikConn.get('v1', '/cluster/me/version')
print "Connected to cluster running version", clustervers['version']

RubrikConn.set_cluster_location("In de tuin van Jerome")


#    def configure_replication(self, username, password, replication_setup,
#                              target_ip=None,
#                              src_gateway = None, tgt_gateway = None,
#                              ca_certificate=None, timeout=30):

# print "Should SUCCEED (Private network)"
# RubrikConn.configure_replication_private('ej.doezie@rubrikdemo.com','L~m4B:e@t',"1.2.3.4")

#print "Should SUCCEED (NAT config)"
#list_src = ["1.2.3.4",[7654]]
#list_dst = ["1.1.3.1",[7654]]
#RubrikConn.configure_replication_nat('ej.doezie@rubrikdemo.com','FakeNews', list_src, list_dst)

##print "Should FAIL (NAT config) on DST port missing"
##list_src = ["1.1.1.1",[902]]
##list_dst = ["1.1.1.2",[]]
##RubrikConn.configure_replication_nat('ej.doezie@rubrikdemo.com','L~m4B:e@t', list_src, list_dst)
