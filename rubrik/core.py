class core():
    """[summary]

    """

    def cluster_version(self):
        """Retrieves software version of the Rubrik cluster

        Returns:
            dict -- Software version running on the cluster
        """

        cluster_version_api_version = 'v1'
        cluster_version_api_endpoint = '/cluster/me/version'

        api_request = self.get(cluster_version_api_version, cluster_version_api_endpoint)

        ########### DO NOT MODIFY THESE VALUES - USED IN UNIT TESTS ONLY #########
        assert cluster_version_api_version == 'v1'
        assert cluster_version_api_endpoint == '/cluster/me/version'
        ##########################################################################

        return api_request
