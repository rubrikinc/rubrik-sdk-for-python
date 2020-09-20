""" Collection of methods that interace with the raw graphql """
import inspect

def _build_graphql_maps(self):
    from os import listdir
    from os.path import isfile, join
    try:
        # Assemble GraphQL query/mutation hash and name map
        _graphql_query = {}
        _graphql_mutation = {}
        _graphql_file_type_map = {}
        _file_query_prefix = 'query'
        _file_suffix = '.graphql'
        _file_mutation_prefix = 'mutation'
        for _f in [_f for _f in listdir(self._data_path) if isfile(join(self._data_path, _f))]:
            _query_name = None
            if _f.endswith(_file_suffix):
                if _f.startswith(_file_query_prefix):
                    _query_name = _f.replace(_file_suffix, '').replace('{}_'.format(_file_query_prefix), '')
                    _graphql_file = open("{}{}".format(self._data_path, _f), 'r').read()
                    _graphql_query[_query_name] = """{}""".format(_graphql_file)
                elif _f.startswith(_file_mutation_prefix):
                    _query_name = _f.replace(_file_suffix, '').replace('{}_'.format(_file_mutation_prefix), '')
                    _graphql_file = open("{}{}".format(self._data_path, _f), 'r').read()
                    _graphql_mutation[_query_name] = """{}""".format(_graphql_file)
                _graphql_file_type_map[_query_name] = self._get_query_names_from_graphql_query(_graphql_file)
        return _graphql_query, _graphql_mutation, _graphql_file_type_map
    except Exception as e:
        print(inspect.stack[3])
        print(e)

def _get_query_names_from_graphql_query(self, graphql_query_text):
    try:
        import re
        _o = re.findall(r' +(\S+) ?\(.*', graphql_query_text)
        return _o
    except Exception as e:
        print(inspect.stack[3])
        print(e)

def _dump_nodes(self, request, query_name):
    try:
        _o = []
        _detail_list = [
            "taskchain_status",
            "assign_sla",
            "on_demand",
            "account_add_aws",
            "account_delete_commit_aws",
            "account_disable_aws",
            "account_delete_initiate_aws",
            "accounts_aws_detail"]
        for _query_returned in request['data']:
            if query_name in _detail_list and _query_returned in self.graphql_file_type_map[query_name]:
                return request['data'][_query_returned]
            elif _query_returned in self.graphql_file_type_map[query_name]:
                for _node_returned in request['data'][_query_returned]['edges']:
                    _o.append(_node_returned['node'])
        return _o
    except Exception as e:
        print(inspect.stack)
        print(e)