import inspect
import os
import reprlib
import sys

import rubrik_cdm


def get_all_sdk_functions():
    connect_functions = inspect.getmembers(rubrik_cdm.Connect, 
        lambda o: inspect.isfunction(o) and o.__name__ != '__init__')
    bootstrap_functions = inspect.getmembers(rubrik_cdm.Bootstrap, 
        lambda o: inspect.isfunction(o) and o.__name__ in ['setup_cluster', 'status'])

    return connect_functions + bootstrap_functions


def get_base_api_functions():
    base_api_functions = inspect.getmembers(rubrik_cdm.api.Api, 
        lambda o: inspect.isfunction(o) and o.__name__ != '__init__')
    return base_api_functions


def get_function_signature(fn):
    return fn.__name__ + str(inspect.signature(fn)).replace('self, ', '')


def is_internal_function(name):
    return name.startswith('_')


def get_all_internal_functions():
    connect_internals = inspect.getmembers(rubrik_cdm.Connect, 
        lambda o: inspect.isfunction(o) and is_internal_function(o.__name__) and o.__name__ != '__init__')
    bootstrap_internals = inspect.getmembers(rubrik_cdm.Bootstrap,
        lambda o: inspect.isfunction(o) and is_internal_function(o.__name__) and o.__name__ != '__init__' and o.__name__ not in [fn[0] for fn in connect_internals])

    return connect_internals + bootstrap_internals


def write_doc_section(f, docstring, section):
    if section is 'arguments':
        for line in docstring:
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
                f.write('| {} | {}  | {} |    {}     |\n'.format(
                    function_name, python_type, description, choices))

    elif section is 'keyword_arguments':
        for line in docstring:
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

                f.write('| {} | {}  | {} |    {}     |    {}     |\n'.format(
                    name, python_type, description, choices, default))

    elif section is 'description':
        for line in docstring:
            f.write(line)
        f.write('\n')

    elif section is 'returns':
        f.write('| Type | Return Value                                                                                   |\n')
        f.write('|------|-----------------------------------------------------------------------------------------------|\n')
        for line in docstring:
            line = line.strip().split(' -- ', 1)

            if line[0] is not '':
                f.write('| {}  | {} |\n'.format(line[0], line[1]))


def write_function_links(f, functions):
    for function in functions:
        f.write('* [{}]({}.md)\n'.format(function, function))


def parse_docstring(docstring):
    r = {
        'description': [],
        'arguments': [],
        'keyword_arguments': [],
        'returns': []
    }

    current_section = 'description'
    for line in docstring.splitlines():
        if 'Returns' in line:
            current_section = 'returns'
            continue
        elif 'Arguments' in line and 'Keyword' not in line:
            current_section = 'arguments'
            continue
        elif 'Keyword Arguments' in line:
            current_section = 'keyword_arguments'
            continue
        else:
            if len(line.strip()) > 0:
                r[current_section].append(line.strip())

    return r


def generate_function_doc(name, obj):
    r = parse_docstring(obj.__doc__)
    
    markdown = open('{}.md'.format(name), 'w')
    markdown.write('# {}\n\n'.format(name))

    description = r['description']
    write_doc_section(markdown, [' '.join(description)], 'description')

    arguments, keyword_arguments = r['arguments'], r['keyword_arguments']
    if arguments:
        markdown.write('## Arguments\n')
        markdown.write('| Name        | Type | Description                                                                 | Choices |\n')
        markdown.write('|-------------|------|-----------------------------------------------------------------------------|---------|\n')
        write_doc_section(markdown, arguments, 'arguments')

    if keyword_arguments:
        markdown.write('## Keyword Arguments\n')
        markdown.write('| Name        | Type | Description                                                                 | Choices | Default |\n')
        markdown.write('|-------------|------|-----------------------------------------------------------------------------|---------|---------|\n')
        write_doc_section(markdown, keyword_arguments, 'keyword_arguments')

    returns = r['returns']
    if returns:
        markdown.write('\n## Returns\n')
        write_doc_section(markdown, returns, 'returns')

    if not is_internal_function(name):
        with open("../sample/{}.py".format(name)) as code:
            example_code = code.read()
        markdown.write("## Example\n```py\n{0}```".format(example_code))

    markdown.close()


def get_module_function_names(module, include_internal=True, exclude=[]):
    search = inspect.getmembers(module, 
        lambda o: inspect.isfunction(o) and o.__name__ not in exclude and o.__name__ != '__init__')
    if not include_internal:
        search = [fn for fn in search if not is_internal_function(fn[1].__name__)]

    return [fn[0] for fn in search]


def generate_summary_doc():
    base_api_functions = [fn[0] for fn in get_base_api_functions()]
    cluster_functions = get_module_function_names(rubrik_cdm.cluster.Cluster, exclude=base_api_functions)
    data_management_functions = get_module_function_names(rubrik_cdm.data_management.Data_Management, exclude=base_api_functions)
    physical_functions = get_module_function_names(rubrik_cdm.physical.Physical, exclude=base_api_functions)
    cloud_functions = get_module_function_names(rubrik_cdm.cloud.Cloud, exclude=base_api_functions)
    combined_function_list = base_api_functions + cluster_functions + data_management_functions + physical_functions + cloud_functions
    connect_functions = get_module_function_names(rubrik_cdm.rubrik_cdm.Connect, exclude=combined_function_list)
    bootstrap_functions = get_module_function_names(rubrik_cdm.rubrik_cdm.Bootstrap, exclude=combined_function_list+connect_functions)
    internal_functions = [fn[0] for fn in get_all_internal_functions()]

    # Create the SUMMARY (side navigation) Document

    markdown = open('SUMMARY.md', 'w')
    markdown.write('# Summary\n\n')

    markdown.write('### Getting Started\n\n')
    markdown.write('* [Quick Start](README.md)\n\n')

    markdown.write('### Base API Calls\n')
    write_function_links(markdown, [f for f in base_api_functions if not is_internal_function(f)])

    markdown.write('\n### Bootstrap Functions\n')
    write_function_links(markdown, [f for f in bootstrap_functions if not is_internal_function(f)])

    markdown.write('\n### Cluster Functions\n')
    write_function_links(markdown, cluster_functions)

    markdown.write('\n### Cloud Functions\n')
    write_function_links(markdown, cloud_functions)

    markdown.write('\n### Data Management Functions\n')
    write_function_links(markdown, [f for f in data_management_functions if not is_internal_function(f)])

    markdown.write('\n### Physical Host Functions\n')
    write_function_links(markdown, [f for f in physical_functions if not is_internal_function(f)])

    markdown.write('\n### SDK Helper Functions\n')
    write_function_links(markdown, [f for f in connect_functions if not is_internal_function(f)])

    markdown.write('\n### Internal Functions\n')
    write_function_links(markdown, internal_functions)

    markdown.close()


if __name__ == "__main__":
    sdk_functions = get_all_sdk_functions()
    for name, obj in sdk_functions:
        generate_function_doc(name, obj)

    generate_summary_doc()
