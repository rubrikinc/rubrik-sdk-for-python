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
