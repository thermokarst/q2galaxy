import os
import xml.etree.ElementTree as xml
import xml.dom.minidom as dom

import bs4  # TODO: can remove?

import qiime2.sdk as sdk

import q2galaxy.env

INPUT_FILE = 'inputs.json'
OUTPUT_FILE = 'outputs.json'


def XMLNode(name_, _text=None, **attrs):
    e = xml.Element(name_, attrs)
    if _text is not None:
        e.text = _text
    return e


def extract_requirements(project_name):
    requirements = XMLNode('requirements')
    for dep, version in q2galaxy.env.extract_environment(project_name).items():
        r = XMLNode('requirement', dep, type='package', version=version)
        requirements.append(r)
    return requirements


def get_tool_id(action):
    return action.get_import_path().replace('.', '_')


def template_all(directory):
    pm = sdk.PluginManager()
    for name, plugin in pm.plugins.items():
        for action in plugin.actions.keys():
            write_tool(directory, name.replace('-', '_'), action)


def write_tool(directory, plugin_id, action_id):
    pm = sdk.PluginManager()
    plugin = pm.plugins[plugin_id.replace('_', '-')]
    action = plugin.actions[action_id]

    filename = os.path.join(directory, get_tool_id(action) + '.xml')

    tool = make_tool(plugin, plugin_id, action, plugin.version)

    with open(filename, 'w') as fh:
        xmlstr = dom.parseString(xml.tostring(tool)).toprettyxml(indent="   ")
        fh.write(xmlstr)


def make_config():
    configfiles = XMLNode('configfiles')
    configfiles.append(XMLNode('inputs', name='inputs', data_style='paths'))
    return configfiles


def make_tool(plugin, plugin_id, action, version):
    signature = action.signature

    inputs = XMLNode('inputs')
    for name, spec in signature.inputs.items():
        param = make_input_param(name, spec)
        inputs.append(param)
    for name, spec in signature.parameters.items():
        # TODO: translate these
        #param = make_parameter_param(name, spec)
        #inputs.append(param)
        pass

    outputs = XMLNode('outputs')
    for name, spec in signature.outputs.items():
        output = make_output(name, spec)
        outputs.append(output)

    tool = XMLNode('tool', id=get_tool_id(action),
                   name=make_tool_name(plugin_id, action.id),
                   version=version,
                   profile='18.09')
    tool.append(extract_requirements(plugin.project_name))
    tool.append(XMLNode('description', action.name))
    tool.append(make_command(plugin_id, action.id))
    tool.append(make_version_command(plugin_id))
    tool.append(make_config())
    tool.append(inputs)
    tool.append(outputs)
    tool.append(XMLNode('help', action.description))
    return tool


def make_input_param(name, spec):
    param = XMLNode('param', type='data', format='qza', name=name)
    options = XMLNode(
        'options', options_filter_attribute='metadata.semantic_type')
    param.append(options)

    if spec.has_description():
        param.set('help', spec.description)
    if spec.has_default() and spec.default is None:
        param.set('optional', 'true')

    for t in spec.qiime_type:
        options.append(XMLNode('filter', type='add_value', value=repr(t)))

    return param


def make_parameter_param(name, spec):
    pass


def make_output(name, spec):
    if qiime2.sdk.util.is_visualization_type(spec.qiime_type):
        ext = 'qzv'
    else:
        ext = 'qza'
    file_name = '.'.join([name, ext])
    return XMLNode('data', format=ext, name=name, from_work_dir=file_name)


def make_command(plugin_id, action_id):
    return XMLNode('command',
                   f"q2galaxy run {plugin_id} {action_id} '$inputs'")


def make_version_command(plugin_id):
    return XMLNode('version_command', f'q2galaxy version {plugin_id}')


def make_citations(citations):
    # TODO: split our BibTeX up into single entries
    pass


def make_tool_name(plugin_id, action_id):
    return plugin_id.replace('_', '-') + ' ' + action_id.replace('_', '-')
