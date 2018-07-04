class core():
    """[summary]

    """

    def cluster_version(self):
        """Retrieves software version of the Rubrik cluster

        Returns:
            dict -- Software version running on the cluster
        """

        api_request = self.get('v1', '/cluster/me/version')
        return api_request
