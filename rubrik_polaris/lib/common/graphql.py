# Copyright 2020 Rubrik, Inc.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.


"""
Collection of methods that interact with the raw GraphQL.
"""


def _build_graphql_maps(self):
    from os import listdir
    from os.path import isfile, join

    # Assemble GraphQL query/mutation hash and name map
    graphql_query = {}
    graphql_file_type_map = {}

    file_query_prefix = 'query'
    file_mutation_prefix = 'mutation'
    file_suffix = '.graphql'

    graphql_files = [f for f in listdir(self._data_path)
                     if isfile(join(self._data_path, f)) and f.endswith(file_suffix)]

    for f in graphql_files:
        query_name = f.replace(file_suffix, '')
        if f.startswith(file_query_prefix):
            query_name = query_name.replace('{}_'.format(file_query_prefix), '')
        elif f.startswith(file_mutation_prefix):
            query_name = query_name.replace('{}_'.format(file_mutation_prefix), '')

        try:
            graphql_file = open("{}{}".format(self._data_path, f), 'r').read()
            graphql_query[query_name] = """{}""".format(graphql_file)

            graphql_file_type_map[query_name] = self._get_query_names_from_graphql_query(graphql_file)
        except OSError as e:
            raise  # TODO: Should we bail immediately or go on to the next file?

    return graphql_query, graphql_file_type_map


def _get_query_names_from_graphql_query(self, graphql_query_text):
    import re
    return re.findall(r' +(\S+) ?\(.*', graphql_query_text)


def _dump_nodes(self, request):
    nodes = []

    has_edges = False
    for query in request['data']:
        has_edges = has_edges or 'edges' in request['data'][query]
        if has_edges:
            for edge in request['data'][query]['edges']:
                nodes.append(edge['node'])

    if not has_edges and 'data' in request and len(request['data']) > 0:
        return request['data'][0]

    return nodes
