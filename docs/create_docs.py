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

import inspect

import jinja2
import rubrik_cdm
import logging

# Define the logging params
console_output_handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] -- %(message)s")
console_output_handler.setFormatter(formatter)

log = logging.getLogger(__name__)
log.addHandler(console_output_handler)
# Uncomment to enable debug logging
# log.setLevel(logging.DEBUG)

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
    ]

    class_functions = {}

    excluded = ['__init__']

    for c in classes:
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

        if value_type[0] is not '':
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
        if value_type[0] is not '':
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
        if line[0] is not '':
            try:
                return_values.append({'type': line[0], 'description': line[1]})
            except:
                log.debug("Found malformed section")
                return ""
            else:
                return return_values


def parse_docstring(docstring):
    sections = {
        'description': [],
        'arguments': [],
        'keyword_arguments': [],
        'returns': []
    }

    #log.debug('Parsing: {}'.format(docstring))
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
                sections[current_section].append(line.strip())

    return {
        'description': ' '.join(sections['description']),
        'arguments': _parse_arguments(sections['arguments']),
        'keyword_arguments': _parse_keyword_arguments(sections['keyword_arguments']),
        'returns': _parse_return_values(sections['returns'])
    }


def generate_function_doc(env, name, obj):
    skip = ['setup_cluster']
    # Don't generate docs for functions with custom documentation
    if name in skip:
        log.debug('Skipping function documentation for {}'.format(name))
        return

    sections = parse_docstring(obj.__doc__)

    # Grab the function definition, removing whitepsace and any pylint directives
    funcdef = inspect.getsource(obj).partition('\n')[0]
    funcdef = funcdef.partition('#')[0].strip()
    
    if funcdef == "@staticmethod":
        funcdef = ""

    example_code = None
    template = env.get_template('function.md.j2')

    log.debug('Generating function documentation for {}'.format(name))
    try:
        if not _is_internal_function(name):
            with open("../sample/{}.py".format(name)) as code:
                example_code = code.read()
    except Exception as err:
        log.debug(err)
        log.debug('Skipping code example for {}'.format(name))
        with open('{}.md'.format(name), 'w') as md:
            md.write(template.render(
                name=name,
                funcdef=funcdef, 
                description=sections['description'],
                arguments=sections['arguments'],
                keyword_arguments=sections['keyword_arguments'],
                returns=sections['returns'],
                example=""
            ))
    else:
        with open('{}.md'.format(name), 'w') as md:
            md.write(template.render(
                name=name,
                funcdef=funcdef,
                description=sections['description'],
                arguments=sections['arguments'],
                keyword_arguments=sections['keyword_arguments'],
                returns=sections['returns'],
                example=example_code
            ))
    log.debug('Wrote {}.md'.format(name))


def _sorted(functions):
    return sorted(functions, key=lambda f: f[0])


def generate_summary_doc(env, functions):
    all_internal_functions = []
    for fns in functions.values():
        all_internal_functions += fns['private']

    template = env.get_template('SUMMARY.md.j2')

    with open('SUMMARY.md', 'w') as md:
        md.write(template.render(
            base_functions=_sorted(functions['Api']['public']), 
            bootstrap_functions=_sorted(functions['Bootstrap']['public']),
            cluster_functions=_sorted(functions['Cluster']['public']),
            cloud_functions=_sorted(functions['Cloud']['public']),
            data_management_functions=_sorted(functions['Data_Management']['public']),
            physical_functions=_sorted(functions['Physical']['public']),
            helper_functions=_sorted(functions['Connect']['public']),
            internal_functions=_sorted(all_internal_functions)
        ))


if __name__ == "__main__":
    # Create template environment
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('create_docs', 'templates'),
        trim_blocks=True,
        lstrip_blocks=True
    )

    # Get all functions defined in the SDK, both public and internal ones
    sdk_functions = get_sdk_functions()

    # Generate the function documentation files
    for class_fns in sdk_functions.values():
        for fn in (class_fns['public'] + class_fns['private']):
            generate_function_doc(env, fn[0], fn[1])
    
    # Generate the summary (side navigation) file
    generate_summary_doc(env, sdk_functions)
