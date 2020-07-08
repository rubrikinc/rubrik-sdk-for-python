# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## Types of changes

- **Added** for new features.
- **Changed** for changes in existing functionality.
- **Deprecated** for soon-to-be removed features.
- **Removed** for now removed features.
- **Fixed** for any bug fixes.
- **Security** in case of vulnerabilities.

## Unreleased
## Added

- `get_sla_objects()` now also supports the following object types: hyper-v, mssql_db, ec2_instance, oracle_db, vcd, managed_volume, ahv, nas_share, linux_and_unix_host, windows_host ([Issue 226](https://github.com/rubrikinc/rubrik-sdk-for-python/issues/226))
- `object_id()` now supports the `organization`, `organization_role_id`, `organization_admin_role`, and `mssql_availability_group` `object_type`

## Changed

- The create_sla() function will return a more clear error message when the SLA was found on the Rubrik cluster but with a different configuraiton than the one provided. ([Issue 236](https://github.com/rubrikinc/rubrik-sdk-for-python/issues/236))

## Fixed

- When calling create_sla() an error will not longer be thrown for frequencies and retentions that have a default None value provided ([Issue 232](https://github.com/rubrikinc/rubrik-sdk-for-python/issues/232))
- The `object_id()` function now returns the correct the MSSQL DB and MSSQL Instance. When the object_type is `mssql_instance` the `mssql_host` keyword argument is now required. When the `object_type` is `mssql_db`, both the `mssql_instance` the `mssql_host` keyword arguments are required. 

## v2.0.9

### Added

- get_all_hosts()
- get_all_vcenters()
- Added a new `logging_level` argument to the Connect function that lets users choose which logging level they would like to show in their logs. Note -- this change has limited functionality as all log messages are categorized as `debug` still. Additional enhancements will be added in the next release. ([Issue 222](https://github.com/rubrikinc/rubrik-sdk-for-python/issues/222))

### Changed

- `object_id()` search for vCenter objects now filters based on `primary_cluster_id=local` ([Issue 214](https://github.com/rubrikinc/rubrik-sdk-for-python/issues/214))

### Fixed

- `object_id` will return the ID for all cases using the database name and the database hosts for the `oracle_db` object type ([Issue 199](https://github.com/rubrikinc/rubrik-sdk-for-python/issues/199)) 
- Fixed case-sensitivity for `object_id` ([Issue 216](https://github.com/rubrikinc/rubrik-sdk-for-python/issues/216))
- Incorrect string join on `get_vsphere_vm` & `get_sql_db` trailing & in query ([Issue 221](https://github.com/rubrikinc/rubrik-sdk-for-python/issues/221))
- Better encode special characteres in `GET` requests. ([Issue 227](https://github.com/rubrikinc/rubrik-sdk-for-python/issues/227))
