""" Collection of methods that interace with the raw graphql """

def _build_graphql_maps(self):
    from os import listdir
    from os.path import isfile, join
    try:
        # Assemble GraphQL query/mutation hash and name map
        _graphql_query = {}
        _graphql_file_type_map = {}
        _file_query_prefix = 'query'
        _file_suffix = '.graphql'
        _file_mutation_prefix = 'mutation'
        for _f in [_f for _f in listdir(self._data_path) if isfile(join(self._data_path, _f))]:
            _query_name = None
            if _f.endswith(_file_suffix):
                _graphql_file = None
                if _f.startswith(_file_query_prefix):
                    _query_name = _f.replace(_file_suffix, '').replace('{}_'.format(_file_query_prefix), '')
                    _graphql_file = open("{}{}".format(self._data_path, _f), 'r').read()
                    _graphql_query[_query_name] = """{}""".format(_graphql_file)
                elif _f.startswith(_file_mutation_prefix):
                    _query_name = _f.replace(_file_suffix, '').replace('{}_'.format(_file_mutation_prefix), '')
                    _graphql_file = open("{}{}".format(self._data_path, _f), 'r').read()
                    _graphql_query[_query_name] = """{}""".format(_graphql_file)
                _graphql_file_type_map[_query_name] = self._get_query_names_from_graphql_query(_graphql_file)
        return _graphql_query,  _graphql_file_type_map
    except Exception as e:
        print(e)

def _get_query_names_from_graphql_query(self, _graphql_query_text):
    try:
        import re
        _o = re.findall(r' +(\S+) ?\(.*', _graphql_query_text)
        return _o
    except Exception as e:
        print(e)

def _dump_nodes(self, request, query_name):
    try:
        _o = []
        for _query_returned in request['data']:
            if 'edges' in request['data'][_query_returned]:
                for _node_returned in request['data'][_query_returned]['edges']:
                    _o.append(_node_returned['node'])
            else:
                return request['data'][_query_returned]
        return _o
    except Exception as e:
        print(e)