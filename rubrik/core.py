class core():
    """[summary]

    """

    def cluster_version(self):

        api_request = self.get('v1', '/cluster/me/version')
        return api_request
