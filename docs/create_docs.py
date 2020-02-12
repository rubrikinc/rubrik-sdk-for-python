# Copyright 2018 Rubrik, Inc.
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

import inspect
import rubrik_cdm


def get_sdk_functions():
    classes = [
        rubrik_cdm.api.Api,
        rubrik_cdm.cloud.Cloud, 
        rubrik_cdm.cluster.Cluster, 
        rubrik_cdm.data_management.Data_Management, 
        rubrik_cdm.physical.Physical,
        rubrik_cdm.rubrik_cdm.Connect,
    ]

    class_functions = {}

    excluded = ['__init__']

    for c in classes:
        functions = inspect.getmembers(c, lambda o: inspect.isfunction(o) and o.__name__ not in excluded and o.__module__ == c.__module__)
        class_functions[c.__name__] = {
            'public': [],
            'private': []
        }
        for f in functions:
            if is_internal_function(f[0]):
                class_functions[c.__name__]['private'].append(f)
            else:
                class_functions[c.__name__]['public'].append(f)


    # Special care for the Bootstrap class due to it's current design

    included = ['setup_cluster', 'status']

    bootstrap_functions = inspect.getmembers(rubrik_cdm.Bootstrap, lambda o: inspect.isfunction(o) and o.__name__ in included and o.__module__ == c.__module__)
    class_functions['Bootstrap'] = {
        'public': bootstrap_functions,
        'private': []
    }

    return class_functions


def get_function_signature(fn):
    return fn.__name__ + str(inspect.signature(fn)).replace('self, ', '')


def is_internal_function(name):
    return name.startswith('_')


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


def markdown_function_links(functions):
    return ''.join(map(lambda fn: '* [{}]({}.md)\n'.format(fn, fn), functions))


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


def generate_summary_doc(functions):
    """ Create the SUMMARY (side navigation) document """

    md = open('SUMMARY.md', 'w')

    md.write('# Summary\n')

    md.write('\n### Getting Started\n\n')
    md.write('* [Quick Start](README.md)\n')
    
    md.write('\n### Base API Calls\n\n')
    md.write(markdown_function_links([f[0] for f in functions['Api']['public']]))
    
    md.write('\n### Bootstrap Functions\n\n')
    md.write(markdown_function_links([f[0] for f in functions['Bootstrap']['public']]))
    
    md.write('\n### Cluster Functions\n\n')
    md.write(markdown_function_links([f[0] for f in functions['Cluster']['public']]))
    
    md.write('\n### Cloud Functions\n\n')
    md.write(markdown_function_links([f[0] for f in functions['Cloud']['public']]))
    
    md.write('\n### Data Management Functions\n\n')
    md.write(markdown_function_links([f[0] for f in functions['Data_Management']['public']]))
    
    md.write('\n### Physical Host Functions\n\n')
    md.write(markdown_function_links([f[0] for f in functions['Physical']['public']]))
    
    md.write('\n### SDK Helper Functions\n\n')
    md.write(markdown_function_links([f[0] for f in functions['Connect']['public']]))
    md.write('* [exceptions](exceptions.md)\n')
    
    md.write('\n### Internal Functions\n\n')
    for funcs in functions.values():
        md.write(markdown_function_links([f[0] for f in funcs['private']]))

    md.close()


if __name__ == "__main__":
    sdk_functions = get_sdk_functions()
    
    for funcs in sdk_functions.values():
        [generate_function_doc(f[0], f[1]) for f in funcs['public']+funcs['private']]
    
    generate_summary_doc(sdk_functions)
