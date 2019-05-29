import json

import click

from .run import action_runner, get_version

from .template import template_all


_OUTPUT_DIR = click.Path(file_okay=False, dir_okay=True, exists=True)


@click.group()
def root():
    pass


@root.group()
def template():
    pass


@template.command()
@click.argument('plugin', type=str)
@click.argument('output', type=_OUTPUT_DIR)
def plugin(plugin, output):
    pass


@template.command()
@click.argument('output', type=_OUTPUT_DIR)
def all(output):
    template_all(output)


@template.command()
@click.argument('output', type=_OUTPUT_DIR)
def tests(output):
    pass


@root.command()
@click.argument('plugin', type=str)
@click.argument('action', type=str)
@click.argument('inputs', type=click.Path(file_okay=True, dir_okay=False,
                                          exists=True))
def run(plugin, action, inputs):
    with open(inputs, 'r') as fh:
        config = json.load(fh)
    action_runner(plugin, action, config)


@root.command()
@click.argument('plugin', type=str)
def version(plugin):
    print('%s version %s' % (plugin, get_version(plugin)))


if __name__ == '__main__':
    root()
