from os import listdir
from os.path import isfile, join

def build_graphql_maps(self):
    # Assemble GraphQL query/mutation hash and name map
    graphql_query = {}
    graphql_mutation = {}
    graphql_file_type_map = {}
    file_query_prefix = 'query'
    file_suffix = '.graphql'
    file_mutation_prefix = 'mutation'
    for f in [f for f in listdir(self.data_path) if isfile(join(self.data_path, f))]:
        _query_name = None
        if f.endswith(file_suffix):
            if f.startswith(file_query_prefix):
                _query_name = f.replace(file_suffix, '').replace('{}_'.format(file_query_prefix), '')
                graphql_file = open("{}{}".format(self.data_path, f), 'r').read()
                graphql_query[_query_name] = """{}""".format(graphql_file)
            elif f.startswith(file_mutation_prefix):
                _query_name = f.replace(file_suffix, '').replace('{}_'.format(file_mutation_prefix), '')
                graphql_file = open("{}{}".format(self.data_path, f), 'r').read()
                graphql_mutation[_query_name] = """{}""".format(graphql_file)
            graphql_file_type_map[_query_name] = self._get_query_names_from_graphql_query(graphql_file)
    return graphql_query, graphql_mutation, graphql_file_type_map