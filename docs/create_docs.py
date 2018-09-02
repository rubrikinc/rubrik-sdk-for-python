import inspect
import rubrik
import os
import sys
import reprlib


def print_doc_string(doc_string, section):

    if section is 'arguments':
        for line in doc_string:
            line = line.replace(' -- ', '').strip().split('}', 1)
            value_type = line[0].split('{', 1)
            if value_type[0] is not '':
                function_name = value_type[0]
                python_type = value_type[1]
                description = line[1]
                # Name | Type | Description | Choices |
                if '(choices: {' in description:
                    choices = description.split("(choices: {")
                    choices = choices[1].replace("})", "").strip()

                    description = description.split("(choices: {")
                    description = description[0]

                else:
                    choices = ''
                markdown.write('| {} | {}  | {} |    {}     |\n'.format(
                    function_name, python_type, description, choices))

    elif section is 'keyword_arguments':
        for line in doc_string:
            line = line.replace(' -- ', '').strip().split('}', 1)
            value_type = line[0].split('{', 1)
            if value_type[0] is not '':
                name = value_type[0]
                python_type = value_type[1]
                description = line[1]
                # Name | Type | Description | Choices | Default
                # (default: {'latest'})
                if '(default: {' in description:

                    default = description.split("(default: {")

                    default = default[1].replace("})", "").strip()
                    if "(choices:" in default:
                        default = default.split('(choices')
                        default = default[0]

                    default = default.replace("'", "").replace('"', '')

                else:
                    default = ''

                if '(choices: {' in description:
                    choices = description.split("(choices: {")
                    choices = choices[1].replace("})", "").strip()
                    choices = choices.replace("'", "").replace('"', '')

                else:
                    choices = ''

                if '(default: {' in description:
                    description = description.split("(default: {")
                    description = description[0]

                markdown.write('| {} | {}  | {} |    {}     |    {}     |\n'.format(
                    name, python_type, description, choices, default))

    elif section is 'description':
        for line in doc_string:
            markdown.write(line)
        markdown.write('\n')
    elif section is 'returns':
        markdown.write(
            '| Type | Return Value                                                                                   |\n')
        markdown.write(
            '|------|-----------------------------------------------------------------------------------------------|\n')
        for line in doc_string:
            line = line.strip().split(' -- ', 1)

            if line[0] is not '':
                markdown.write('| {}  | {} |\n'.format(line[0], line[1]))


def doc_string_description(doc_string):
    for index, line in enumerate(doc_string):
        if not line.strip():
            return index


def doc_string_ending(doc_string):
    ending_lines = []
    for index, line in enumerate(doc_string):
        if not line.strip():
            ending_lines.append(index)

    return ending_lines


def doc_string_end_block(ending_lines, starting_line):
    for index in ending_lines:
        if index > starting_line:
            return index


def example_code(function_name):
    print()


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

    print(function_name)

    if 'init' not in function_name:
        arguments_start = None
        keyword_argument_start = None
        return_start = None
        arguments_present = False
        arguments_present = False

        markdown = open('{}.md'.format(function_name), 'w')
        markdown.write('# {}\n\n'.format(function_name))

        doc_string = function_documentation[function_name]
        doc_string = doc_string.splitlines()

        description_start = doc_string_description(doc_string)
        ending_lines = doc_string_ending(doc_string)

        for index, line in enumerate(doc_string):
            if 'Arguments' in line and 'Keyword' not in line:
                arguments_start = index
            if 'Keyword Arguments' in line:
                keyword_argument_start = index
            if 'Returns' in line:
                return_start = index

        description = []
        arguments = []
        keyword_arguments = []
        returns = []

        # # Doc Sring Returns
        for index, line in enumerate(doc_string):
            # Parse the function description
            if index < description_start:
                if len(line) is not 0:
                    description.append(line.replace('\n', ''))

            try:
                if arguments_start:
                    argument_ending = doc_string_end_block(ending_lines, arguments_start)
                    if arguments_start + 1 <= index <= argument_ending - 1:
                        if len(line) is not 0:
                            arguments.append(line)
                    arguments_present = True

            except NameError:
                pass

            try:
                if keyword_argument_start:
                    keyword_argument_ending = doc_string_end_block(ending_lines, keyword_argument_start)
                    if keyword_argument_start + 1 <= index <= keyword_argument_ending - 1:
                        if len(line) is not 0:
                            keyword_arguments.append(line)
                    arguments_present = True

            except NameError:
                pass

            try:
                if return_start:
                    return_ending = doc_string_end_block(ending_lines, return_start)
                    if return_start + 1 <= index <= return_ending - 1:
                        if len(line) is not 0:
                            returns.append(line)
            except NameError:
                pass

        if len(description) > 1:
            # Combine the multi-line description into a single line
            parse_description = ''.join(description).split()
            parse_description = ' '.join(parse_description)
            description = []
            description.append(parse_description)
        print_doc_string(description, 'description')

        for function, function_code_example in function_examples.items():
            if function_name is function:
                markdown.write('```py\n')
                markdown.write(function_code_example)
                markdown.write('\n```\n\n')

        if arguments:
            markdown.write('## Arguments\n')

            markdown.write(
                '| Name        | Type | Description                                                                 | Choices |\n')
            markdown.write(
                '|-------------|------|-----------------------------------------------------------------------------|---------|\n')
            print_doc_string(arguments, 'arguments')

        if keyword_arguments:
            markdown.write('## Keyword Arguments\n')

            markdown.write(
                '| Name        | Type | Description                                                                 | Choices | Default |\n')
            markdown.write(
                '|-------------|------|-----------------------------------------------------------------------------|---------|---------|\n')
            print_doc_string(keyword_arguments, 'keyword_arguments')

        if returns:
            markdown.write('\n## Returns\n')
            print_doc_string(returns, 'returns')

        if function_name[0] is not '_':
            with open("../sample/{}.py".format(function_name)) as code:
                example_code = code.read()
            markdown.write('## Example\n')
            markdown.write("```py\n")
            markdown.write(example_code)
            markdown.write("```")

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

physical_search = inspect.getmembers(rubrik.physical.Physical, inspect.isfunction)
physical_functions = []
for function in physical_search:
    if function[0] not in base_api_functions:
        physical_functions.append(function[0])
for function in physical_functions:
    if function[0] is '_':
        physical_functions.remove(function)

cloud_search = inspect.getmembers(rubrik.cloud.Cloud, inspect.isfunction)
cloud_functions = []
for function in cloud_search:
    if function[0] not in base_api_functions:
        cloud_functions.append(function[0])
for function in cloud_functions:
    if function[0] is '_':
        cloud_functions.remove(function)


combined_function_list = base_api_functions + cluster_functions + \
    data_management_functions + physical_functions + cloud_functions

connect_functions_search = inspect.getmembers(rubrik.rubrik.Connect, inspect.isfunction)
connect_functions = []
for function in connect_functions_search:
    if function[0] not in combined_function_list:
        connect_functions.append(function[0])
del connect_functions[0]

# Create the SUMMARY (side navigation) Document
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

markdown.write('\n### Cloud Functions\n')
for function in cloud_functions:
    markdown.write('* [{}]({}.md)\n'.format(function, function))

markdown.write('\n### Data Management Functions\n')
for function in data_management_functions:
    if function[0] is not '_':
        markdown.write('* [{}]({}.md)\n'.format(function, function))

markdown.write('\n### Physical Host Functions\n')
for function in physical_functions:
    if function[0] is not '_':
        markdown.write('* [{}]({}.md)\n'.format(function, function))

markdown.write('\n### SDK Helper Functions\n')
for function in connect_functions:
    if function[0] is not '_':
        markdown.write('* [{}]({}.md)\n'.format(function, function))

markdown.write('\n### Internal Functions\n')
for function in connect_functions:
    if function[0] is '_':
        markdown.write('* [{}]({}.md)\n'.format(function, function))
for function in combined_function_list:
    if function[0] is '_':
        markdown.write('* [{}]({}.md)\n'.format(function, function))

markdown.close()
