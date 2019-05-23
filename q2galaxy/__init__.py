import json

import click

from .run import action_runner, get_version

from .template import template_all


@click.group()
def root():
    pass


@root.group()
def template():
    pass


@template.command()
def plugin():
    pass


@template.command()
@click.argument('output', type=click.Path(file_okay=False, dir_okay=True,
                                          exists=True))
def all(output):
    template_all(output)


@template.command()
@click.argument('output', type=click.Path(file_okay=False, dir_okay=True,
                                          exists=True))
def tests(output):
    _init_test_plugin()
    template_all(output)


@root.command()
@click.argument('plugin', type=str)
@click.argument('action', type=str)
@click.argument('inputs', type=click.Path(file_okay=True, dir_okay=False,
                                          exists=True))
def run(plugin, action, inputs):
    if plugin == 'q2galaxy_test_suite':
        _init_test_plugin()
    with open(inputs, 'r') as fh:
        config = json.load(fh)
    action_runner(plugin, action, config)


@root.command()
@click.argument('plugin', type=str)
def version(plugin):
    print('%s version %s' % (plugin, get_version(plugin)))


def _init_test_plugin():
    import qiime2.sdk
    from .test_suite.plugin_setup import plugin as test_suite_plugin

    pm = qiime2.sdk.PluginManager(install_plugins=False)
    pm.install_plugin(test_suite_plugin)
