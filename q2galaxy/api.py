import q2galaxy.core.templating as _templating


def action_to_galaxy_xml(action):
    pass


def plugin_to_galaxy_xml(plugin):
    pass


def template_plugin(directory):
    pass


def template_all(directory, skip_no_conda=False):
    for status in template_all_iter(directory):
        if status.error is not None and not skip_no_conda:
            raise status.error


def template_all_iter(directory):
    for 
