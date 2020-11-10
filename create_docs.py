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

import glob
import inspect
import logging
import os
import shutil
import sys

import jinja2
import rubrik_cdm
import rubrik_polaris


def _is_internal_function(name):
    return name.startswith('_')


def get_sdk_functions():
    classes = [
        rubrik_cdm.api.Api,
        rubrik_cdm.cloud.Cloud, 
        rubrik_cdm.cluster.Cluster, 
        rubrik_cdm.data_management.Data_Management, 
        rubrik_cdm.physical.Physical,
        rubrik_cdm.rubrik_cdm.Connect,
        rubrik_polaris.PolarisClient
    ]

    class_functions = {}

    excluded = ['__init__']

    for c in classes:
        if c == rubrik_polaris.PolarisClient:
            functions = inspect.getmembers(c, 
                lambda o:
                    inspect.isfunction(o) and 
                    o.__name__ not in excluded
            )
        else:
            functions = inspect.getmembers(c, 
                lambda o:
                    inspect.isfunction(o) and 
                    o.__name__ not in excluded and 
                    o.__module__ == c.__module__
            )

        class_functions[c.__name__] = {
            'public': [],
            'private': []
        }
        for f in functions:
            if _is_internal_function(f[0]):
                class_functions[c.__name__]['private'].append(f)
            else:
                class_functions[c.__name__]['public'].append(f)


    # Special care for the Bootstrap class due to it's current design

    included = ['setup_cluster', 'status']

    bootstrap_functions = inspect.getmembers(rubrik_cdm.rubrik_cdm.Bootstrap, 
        lambda o: inspect.isfunction(o) and 
                  o.__name__ in included and 
                  o.__module__ == 'rubrik_cdm.rubrik_cdm'
    )
    class_functions['Bootstrap'] = {
        'public': bootstrap_functions,
        'private': []
    }

    return class_functions


def _parse_arguments(docstring):
    arguments = []

    for line in docstring:
        line = line.replace(' -- ', '').strip().split('}', 1)
        value_type = line[0].split('{', 1)

        if value_type[0] != '':
            function_name = value_type[0]
            python_type = value_type[1]
            description = line[1]

            if '(choices: {' in description:
                choices = description.split("(choices: {")
                choices = choices[1].replace("})", "").strip()

                description = description.split("(choices: {")
                description = description[0]
            else:
                choices = ''
            
            arguments.append({
                'name': function_name,
                'type': python_type,
                'description': description,
                'choices': choices
            })

    return arguments


def _parse_keyword_arguments(docstring):
    keyword_arguments = []

    for line in docstring:
        line = line.replace(' -- ', '').strip().split('}', 1)
        value_type = line[0].split('{', 1)
        if value_type[0] != '':
            name = value_type[0]
            python_type = value_type[1]
            description = line[1]

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

            keyword_arguments.append({
                'name': name,
                'type': python_type,
                'description': description,
                'choices': choices,
                'default': default
            })

    return keyword_arguments


def _parse_return_values(docstring):
    return_values = []

    for line in docstring:
        line = line.strip().split(' -- ', 1)
        if line[0] != '':
            description = ""
            if len(line) > 1:
                description = line[1]
            
            return_values.append({
                'type': line[0], 
                'description': description
            })
    
    return return_values


def _parse_exceptions(docstring):
    exceptions = []

    for line in docstring:
        line = line.strip().split(' -- ', 1)
        if line[0] != '':
            exceptions.append({
                'type': line[0], 
                'description': line[1]
            })
    
    return exceptions


def parse_docstring(docstring):
    sections = {
        'description': [],
        'arguments': [],
        'keyword_arguments': [],
        'returns': [],
        'exceptions': []
    }

    if not docstring:
        return sections

    #log.debug('Parsing: {}'.format(docstring))
    current_section = 'description'
    for line in docstring.splitlines():
        if 'Returns:' in line:
            current_section = 'returns'
            continue
        elif 'Arguments:' in line and 'Keyword' not in line:
            current_section = 'arguments'
            continue
        elif 'Keyword Arguments:' in line:
            current_section = 'keyword_arguments'
            continue
        elif 'Exceptions:' in line:
            current_section = 'exceptions'
            continue
        else:
            if len(line.strip()) > 0:
                sections[current_section].append(line.strip())

    parsed_values = {
        'description': '',
        'arguments': [],
        'keyword_arguments': [],
        'returns': [],
        'exceptions': []
    }

    if sections['description'] != []:
        parsed_values['description'] = ' '.join(sections['description'])

    if sections['arguments'] != []:
        parsed_values['arguments'] = _parse_arguments(sections['arguments'])

    if sections['keyword_arguments'] != []:
        parsed_values['keyword_arguments'] = _parse_keyword_arguments(sections['keyword_arguments'])

    if sections['returns'] != []:
        parsed_values['returns'] = _parse_return_values(sections['returns'])

    if sections['exceptions'] != []:
        parsed_values['exceptions'] = _parse_exceptions(sections['exceptions'])

    return parsed_values


def generate_function_doc(env, name, obj):
    sections = parse_docstring(obj.__doc__)

    # Grab the function definition, removing whitepsace and any pylint directives
    funcdef = inspect.getsource(obj).partition('\n')[0]
    funcdef = funcdef.partition('#')[0].strip()
    
    if funcdef == "@staticmethod":
        funcdef = ""

    example_code = None
    template = env.get_template('function.md.j2')

    module_name = obj.__module__.split('.')[0]
    dest_dir = '{}/{}'.format(BUILD_DIR, module_name)

    log.debug('Generating function documentation for {}'.format(name))
    try:
        if not _is_internal_function(name):
            with open("sample/{}/{}.py".format(module_name, name)) as code:
                example_code = code.read()
    except Exception as err:
        log.debug(err)
        log.debug('Skipping code example for {}'.format(name))
        with open('{}/{}.md'.format(dest_dir, name), 'w') as md:
            md.write(template.render(
                name=name,
                funcdef=funcdef, 
                description=sections['description'],
                arguments=sections['arguments'],
                keyword_arguments=sections['keyword_arguments'],
                returns=sections['returns'],
                exceptions=sections['exceptions'],
                example=""
            ))
    else:
        with open('{}/{}.md'.format(dest_dir, name), 'w') as md:
            md.write(template.render(
                name=name,
                funcdef=funcdef,
                description=sections['description'],
                arguments=sections['arguments'],
                keyword_arguments=sections['keyword_arguments'],
                returns=sections['returns'],
                exceptions=sections['exceptions'],
                example=example_code
            ))
    log.debug('Wrote {}/{}.md'.format(dest_dir, name))


def _split_polaris_functions(functions):
    split_functions = functions
    for f in functions['PolarisClient']['public']:
        module_name = f[1].__module__
        if module_name in split_functions:
            split_functions[module_name].append(f)
        else:
            split_functions[module_name] = [f]

    return split_functions


def _sorted(functions):
    return sorted(functions, key=lambda f: f[0])


def generate_summary_doc(env, functions):
    template = env.get_template('SUMMARY.md.j2')

    functions = _split_polaris_functions(functions)

    with open('{}/SUMMARY.md'.format(BUILD_DIR), 'w') as md:
        md.write(template.render(
            base_functions=_sorted(functions['Api']['public']), 
            bootstrap_functions=_sorted(functions['Bootstrap']['public']),
            cluster_functions=_sorted(functions['Cluster']['public']),
            cloud_functions=_sorted(functions['Cloud']['public']),
            data_management_functions=_sorted(functions['Data_Management']['public']),
            physical_functions=_sorted(functions['Physical']['public']),
            helper_functions=_sorted(functions['Connect']['public']),
            polaris_core_functions=_sorted(functions['rubrik_polaris.lib.common.core']),
            polaris_accounts_functions=_sorted(functions['rubrik_polaris.lib.accounts']),
            polaris_compute_functions=_sorted(functions['rubrik_polaris.lib.compute']),
            polaris_storage_functions=_sorted(functions['rubrik_polaris.lib.storage'])
        ))


if __name__ == "__main__":
    # Define the logging params
    console_output_handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] -- %(message)s")
    console_output_handler.setFormatter(formatter)

    log = logging.getLogger(__name__)
    log.addHandler(console_output_handler)
    # Uncomment to enable debug logging
    # log.setLevel(logging.DEBUG)

    # Create template environment
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('create_docs', 'docs/templates'),
        trim_blocks=True,
        lstrip_blocks=True
    )

    BUILD_DIR = 'docs/_build'
    STATIC_DIR = 'docs/static'

    # Create build directory
    try:
        os.mkdir(BUILD_DIR)
    except FileExistsError:
        # Empty existing directory
        for filename in os.listdir(BUILD_DIR):
            filepath = os.path.join(BUILD_DIR, filename)
            try:
                shutil.rmtree(filepath)
            except OSError:
                os.remove(filepath)

    os.mkdir('{}/rubrik_cdm'.format(BUILD_DIR))
    os.mkdir('{}/rubrik_polaris'.format(BUILD_DIR))
    
    # Get all functions defined in the SDK, both public and internal ones
    sdk_functions = get_sdk_functions()

    # Generate the function documentation files
    for class_fns in sdk_functions.values():
        for fn in class_fns['public']:
            generate_function_doc(env, fn[0], fn[1])
    
    # Generate the summary (side navigation) file
    generate_summary_doc(env, sdk_functions)

    # Copy static markdown files to the build directory
    shutil.copytree(STATIC_DIR, BUILD_DIR, dirs_exist_ok=True)
