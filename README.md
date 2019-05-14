# Rubrik SDK for Python

| master                                                                                                                                                                            | devel                                                                                                                                                                          |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [![Master Branch Status](https://circleci.com/gh/rubrikinc/rubrik-sdk-for-python/tree/master.svg?style=svg)](https://circleci.com/gh/rubrikinc/rubrik-sdk-for-python/tree/master) | [![Devel Branch Status](https://circleci.com/gh/rubrikinc/rubrik-sdk-for-python/tree/devel.svg?style=svg)](https://circleci.com/gh/rubrikinc/rubrik-sdk-for-python/tree/devel) |


This project provides a Python package that makes it easy to interact with the Rubrik CDM API.

The SDK has been tested against Python 2.7.6 and Python 3.6.4.

# :hammer: Installation

Install from pip:

`pip install rubrik_cdm`

Install from source:
```
$ git clone https://github.com/rubrikinc/rubrik-sdk-for-python
$ cd rubrik-sdk-for-python
$ python setup.py install
```

# :mag: Example

By default, the Rubrik SDK will attempt to read the the Rubrik Cluster credentials from the following environment variables:

* `rubrik_cdm_node_ip`
* `rubrik_cdm_username`
* `rubrik_cdm_password`

```py
import rubrik_cdm
rubrik = rubrik_cdm.Connect()

cluster_version = rubrik.cluster_version()

print(cluster_version)
```

# :blue_book: Documentation 

Here are some resources to get you started! If you find any challenges from this project are not properly documented or are unclear, please [raise an issue](https://github.com/rubrikinc/rubrik-sdk-for-python/issues/new/choose) and let us know! This is a fun, safe environment - don't worry if you're a GitHub newbie! :heart:

* [Quick Start Guide](https://github.com/rubrikinc/rubrik-sdk-for-python/blob/master/docs/quick-start.md)
* [SDK for Python Documentation](https://rubrik.gitbook.io/rubrik-sdk-for-python/)
* [Rubrik API Documentation](https://github.com/rubrikinc/api-documentation)
* [VIDEO: Getting Start with the Rubrik SDK for Python](https://www.youtube.com/watch?v=wd1PxPOd3f8&feature=youtu.be)
* [BLOG: Hello World! Welcoming Rubrik’s Python SDK](https://www.rubrik.com/blog/introducing-rubrik-python-sdk/)

# :muscle: How You Can Help

We glady welcome contributions from the community. From updating the documentation to adding more functions for Python, all ideas are welcome. Thank you in advance for all of your issues, pull requests, and comments! :star:

* [Contributing Guide](CONTRIBUTING.md)
* [Code of Conduct](CODE_OF_CONDUCT.md)

# :pushpin: License

* [MIT License](LICENSE)

# :point_right: About Rubrik Build

We encourage all contributors to become members. We aim to grow an active, healthy community of contributors, reviewers, and code owners. Learn more in our [Welcome to the Rubrik Build Community](https://github.com/rubrikinc/welcome-to-rubrik-build) page.

We'd  love to hear from you! Email us: build@rubrik.com :love_letter:
