import inspect
import rubrik
import os
import sys


def print_doc_string(doc_string):

    for line in doc_string:
        markdown.write(line.strip() + '\n\n')


rubrk_sdk_functions = inspect.getmembers(rubrik.Connect, inspect.isfunction)

function_examples = {}
function_documentation = {}
for function in rubrk_sdk_functions:
    function_documentation[function[0]] = function[1].__doc__
    function_code = inspect.getsource(function[1])
    if '@staticmethod' in function_code:
        function_code = function_code.replace('@staticmethod\n', '')
        function_code = function_code.splitlines()[0].replace(
            'self, ', '').replace('self', '').replace(':', '').strip()

    else:

        function_code = function_code.splitlines()[0].replace(
            'self, ', '').replace('self', '').replace(':', '').strip()

    function_examples[function[0]] = function_code


for function_name, function_doc_string in function_documentation.items():
    if 'init' not in function_name:
        markdown = open('{}.md'.format(function_name), 'w')
        markdown.write('# {}\n\n'.format(function_name))

        doc_string = function_documentation[function_name]
        doc_string = doc_string.splitlines()

        filter_lines = []

        for index, line in enumerate(doc_string):
            if 'Arguments' in line:
                filter_lines.append(index)
            if 'Returns' in line:
                filter_lines.append(index)

        arguments = []
        keyword_arguments = []
        returns = []
        desctiption = []

        try:
            arguments_start = filter_lines[0]
            keyword_arguments_start = filter_lines[1]
            returns_start = filter_lines[2]
        except:
            pass

        # Doc Sring Returns
        for index, line in enumerate(doc_string):
            # Parse the function description
            if len(filter_lines) >= 0:
                if index < arguments_start:
                    if len(line) is not 0:
                        desctiption.append(line.replace('\n', ''))

            # Parse the function arguments
            if len(filter_lines) >= 1:
                try:
                    if arguments_start + 1 <= index <= keyword_arguments_start - 1:
                        if len(line) is not 0:
                            arguments.append(line)
                except:
                    if len(line) is not 0:
                        arguments.append(line)

            # Parse the function keyword arguments
            if len(filter_lines) >= 2:
                if keyword_arguments_start + 1 <= index <= returns_start - 1:
                    if len(line) is not 0:
                        keyword_arguments.append(line)

            # Parse the function return value(s)
            if len(filter_lines) >= 3:
                if index >= returns_start + 1:
                    if len(line) is not 0:
                        returns.append(line)

        # print(index, line)
        if desctiption:
            if len(desctiption) > 1:
                # Combine the multi-line description into a single line
                parse_desctiption = ''.join(desctiption).split()
                parse_desctiption = ' '.join(parse_desctiption)
                desctiption = []
                desctiption.append(parse_desctiption)
            print_doc_string(desctiption)

        for function, function_code_example in function_examples.items():
            if function_name is function:
                markdown.write('```py\n')
                markdown.write(function_code_example)
                markdown.write('\n```\n\n')

        if arguments:
            markdown.write('## Arguments\n')
            print_doc_string(arguments)

        if keyword_arguments:
            markdown.write('\n## Keyword Arguments\n')
            print_doc_string(keyword_arguments)

        if returns:
            markdown.write('\n## Returns\n')
            print_doc_string(returns)

        markdown.close()


base_api_functions_search = inspect.getmembers(rubrik.api.Api, inspect.isfunction)
base_api_functions = []
for function in base_api_functions_search:
    # If first character of the function name...
    base_api_functions.append(function[0])
del base_api_functions[0]

cluster_functions_search = inspect.getmembers(rubrik.cluster.Cluster, inspect.isfunction)
cluster_functions = []
for function in cluster_functions_search:
    if function[0] not in base_api_functions:
        cluster_functions.append(function[0])
for function in cluster_functions:
    if function[0] is '_':
        cluster_functions.remove(function)

data_management_search = inspect.getmembers(rubrik.data_management.Data_Management, inspect.isfunction)
data_management_functions = []
for function in data_management_search:
    if function[0] not in base_api_functions:
        data_management_functions.append(function[0])
for function in data_management_functions:
    if function[0] is '_':
        data_management_functions.remove(function)

combined_function_list = base_api_functions + cluster_functions + data_management_functions

connect_functions_search = inspect.getmembers(rubrik.rubrik.Connect, inspect.isfunction)
connect_functions = []
for function in connect_functions_search:
    if function[0] not in combined_function_list:
        connect_functions.append(function[0])
del connect_functions[0]


markdown = open('SUMMARY.md', 'w')
markdown.write('# Summary\n\n')

markdown.write('### Getting Started\n\n')
markdown.write('* [Quick Start](README.md)\n\n')

markdown.write('### Base API Calls\n')
for function in base_api_functions:
    if function[0] is not '_':
        markdown.write('* [{}]({}.md)\n'.format(function, function))

markdown.write('\n### Cluster Functions\n')
for function in cluster_functions:
    markdown.write('* [{}]({}.md)\n'.format(function, function))

markdown.write('\n### Data Management Functions\n')
for function in data_management_functions:
    markdown.write('* [{}]({}.md)\n'.format(function, function))

markdown.write('\n### SDK Helper Functions\n')
for function in connect_functions:
    if function[0] is not '_':
        markdown.write('* [{}]({}.md)\n'.format(function, function))

markdown.close()
