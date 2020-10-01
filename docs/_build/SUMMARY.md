# Table of contents

* [Introduction](README.md)

## Getting Started

* [Quick Start](getting-started/readme.md)

## Base API Calls

* [delete](base-api-calls/delete.md)
* [get](base-api-calls/get.md)
* [job\_status](base-api-calls/job_status.md)
* [patch](base-api-calls/patch.md)
* [post](base-api-calls/post.md)
* [put](base-api-calls/put.md)
* [query](base-api-calls/query.md)

## Bootstrap Functions

* [setup\_cluster](bootstrap-functions/setup_cluster.md)
* [status](bootstrap-functions/status.md)

## Cluster Functions

* [add\_floating\_ips](cluster-functions/add_floating_ips.md)
* [add\_guest\_credential](cluster-functions/add_guest_credential.md)
* [add\_vcenter](cluster-functions/add_vcenter.md)
* [cluster\_node\_id](cluster-functions/cluster_node_id.md)
* [cluster\_node\_ip](cluster-functions/cluster_node_ip.md)
* [cluster\_node\_name](cluster-functions/cluster_node_name.md)
* [cluster\_support\_tunnel](cluster-functions/cluster_support_tunnel.md)
* [cluster\_version](cluster-functions/cluster_version.md)
* [configure\_cluster\_location](cluster-functions/configure_cluster_location.md)
* [configure\_dns\_servers](cluster-functions/configure_dns_servers.md)
* [configure\_login\_banner](cluster-functions/configure_login_banner.md)
* [configure\_ntp](cluster-functions/configure_ntp.md)
* [configure\_replication\_nat](cluster-functions/configure_replication_nat.md)
* [configure\_replication\_private](cluster-functions/configure_replication_private.md)
* [configure\_search\_domain](cluster-functions/configure_search_domain.md)
* [configure\_smtp\_settings](cluster-functions/configure_smtp_settings.md)
* [configure\_syslog](cluster-functions/configure_syslog.md)
* [configure\_timezone](cluster-functions/configure_timezone.md)
* [configure\_vlan](cluster-functions/configure_vlan.md)
* [create\_user](cluster-functions/create_user.md)
* [delete\_guest\_credential](cluster-functions/delete_guest_credential.md)
* [delete\_proxy](cluster-functions/delete_proxy.md)
* [end\_user\_authorization](cluster-functions/end_user_authorization.md)
* [get\_all\_vcenters](cluster-functions/get_all_vcenters.md)
* [get\_floating\_ips](cluster-functions/get_floating_ips.md)
* [minimum\_installed\_cdm\_version](cluster-functions/minimum_installed_cdm_version.md)
* [read\_only\_authorization](cluster-functions/read_only_authorization.md)
* [refresh\_vcenter](cluster-functions/refresh_vcenter.md)
* [remove\_floating\_ips](cluster-functions/remove_floating_ips.md)
* [update\_proxy](cluster-functions/update_proxy.md)

## Cloud Functions

* [add\_aws\_native\_account](cloud-functions/add_aws_native_account.md)
* [aws\_s3\_cloudon](cloud-functions/aws_s3_cloudon.md)
* [aws\_s3\_cloudout](cloud-functions/aws_s3_cloudout.md)
* [azure\_cloudon](cloud-functions/azure_cloudon.md)
* [azure\_cloudout](cloud-functions/azure_cloudout.md)
* [update\_aws\_native\_account](cloud-functions/update_aws_native_account.md)
* [update\_aws\_s3\_cloudout](cloud-functions/update_aws_s3_cloudout.md)

## Data Management Functions

* [assign\_sla](data-management-functions/assign_sla.md)
* [begin\_managed\_volume\_snapshot](data-management-functions/begin_managed_volume_snapshot.md)
* [create\_sla](data-management-functions/create_sla.md)
* [delete\_sla](data-management-functions/delete_sla.md)
* [end\_managed\_volume\_snapshot](data-management-functions/end_managed_volume_snapshot.md)
* [get\_all\_hosts](data-management-functions/get_all_hosts.md)
* [get\_esxi\_subnets](data-management-functions/get_esxi_subnets.md)
* [get\_sla\_objects](data-management-functions/get_sla_objects.md)
* [get\_sql\_db](data-management-functions/get_sql_db.md)
* [get\_sql\_db\_files](data-management-functions/get_sql_db_files.md)
* [get\_sql\_live\_mount](data-management-functions/get_sql_live_mount.md)
* [get\_vsphere\_live\_mount](data-management-functions/get_vsphere_live_mount.md)
* [get\_vsphere\_live\_mount\_names](data-management-functions/get_vsphere_live_mount_names.md)
* [get\_vsphere\_vm](data-management-functions/get_vsphere_vm.md)
* [get\_vsphere\_vm\_details](data-management-functions/get_vsphere_vm_details.md)
* [get\_vsphere\_vm\_file](data-management-functions/get_vsphere_vm_file.md)
* [get\_vsphere\_vm\_snapshot](data-management-functions/get_vsphere_vm_snapshot.md)
* [object\_id](data-management-functions/object_id.md)
* [on\_demand\_snapshot](data-management-functions/on_demand_snapshot.md)
* [pause\_snapshots](data-management-functions/pause_snapshots.md)
* [register\_vm](data-management-functions/register_vm.md)
* [resume\_snapshots](data-management-functions/resume_snapshots.md)
* [set\_esxi\_subnets](data-management-functions/set_esxi_subnets.md)
* [sql\_db\_export](data-management-functions/sql_db_export.md)
* [sql\_instant\_recovery](data-management-functions/sql_instant_recovery.md)
* [sql\_live\_mount](data-management-functions/sql_live_mount.md)
* [sql\_live\_unmount](data-management-functions/sql_live_unmount.md)
* [vcenter\_refresh\_vm](data-management-functions/vcenter_refresh_vm.md)
* [vsphere\_instant\_recovery](data-management-functions/vsphere_instant_recovery.md)
* [vsphere\_live\_mount](data-management-functions/vsphere_live_mount.md)
* [vsphere\_live\_unmount](data-management-functions/vsphere_live_unmount.md)

## Physical Host Functions

* [add\_host\_share](physical-host-functions/add_host_share.md)
* [add\_nas\_share\_to\_host](physical-host-functions/add_nas_share_to_host.md)
* [add\_physical\_host](physical-host-functions/add_physical_host.md)
* [assign\_physical\_host\_fileset](physical-host-functions/assign_physical_host_fileset.md)
* [create\_nas\_fileset](physical-host-functions/create_nas_fileset.md)
* [create\_physical\_fileset](physical-host-functions/create_physical_fileset.md)
* [delete\_physical\_host](physical-host-functions/delete_physical_host.md)

## SDK Helper Functions

* [log](sdk-helper-functions/log.md)
* [exceptions](sdk-helper-functions/exceptions.md)

## Internal Functions

* [\_api\_validation](internal-functions/_api_validation.md)
* [\_authorization\_header](internal-functions/_authorization_header.md)
* [\_common\_api](internal-functions/_common_api.md)
* [\_date\_time\_conversion](internal-functions/_date_time_conversion.md)
* [\_header](internal-functions/_header.md)
* [\_platform\_user\_agent](internal-functions/_platform_user_agent.md)
* [\_time\_in\_range](internal-functions/_time_in_range.md)
* [\_validate\_sql\_db](internal-functions/_validate_sql_db.md)
* [\_validate\_sql\_recovery\_point](internal-functions/_validate_sql_recovery_point.md)

