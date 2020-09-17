""" Collection of methods that interace with the raw graphql """


def build_graphql_maps(self):
    from os import listdir
    from os.path import isfile, join

    # Assemble GraphQL query/mutation hash and name map
    _graphql_query = {}
    _graphql_mutation = {}
    _graphql_file_type_map = {}
    _file_query_prefix = 'query'
    _file_suffix = '.graphql'
    _file_mutation_prefix = 'mutation'
    for f in [f for f in listdir(self.data_path) if isfile(join(self.data_path, f))]:
        query_name = None
        if f.endswith(_file_suffix):
            if f.startswith(_file_query_prefix):
                query_name = f.replace(_file_suffix, '').replace('{}_'.format(_file_query_prefix), '')
                _graphql_file = open("{}{}".format(self.data_path, f), 'r').read()
                _graphql_query[query_name] = """{}""".format(_graphql_file)
            elif f.startswith(_file_mutation_prefix):
                query_name = f.replace(_file_suffix, '').replace('{}_'.format(_file_mutation_prefix), '')
                _graphql_file = open("{}{}".format(self.data_path, f), 'r').read()
                _graphql_mutation[query_name] = """{}""".format(_graphql_file)
            _graphql_file_type_map[query_name] = self._get_query_names_from_graphql_query(_graphql_file)
    return _graphql_query, _graphql_mutation, _graphql_file_type_map

def _get_query_names_from_graphql_query(self, _graphql_query_text):
    import re
    o = re.findall(r'(\S+) ?\(.*\)', _graphql_query_text)
    return o

def _dump_nodes(self, request, query_name):
    o = []
    detail_list = ["assignSla", "takeOnDemandSnapshot", "awsNativeProtectionAccountAdd"]
    for query_returned in request['data']:
        if query_returned in detail_list and query_returned in self.graphql_file_type_map[query_name]:
            return request['data'][query_returned]
        elif query_returned in self.graphql_file_type_map[query_name]:
            for node_returned in request['data'][query_returned]['edges']:
                o.append(node_returned['node'])
    return o