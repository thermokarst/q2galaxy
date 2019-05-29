from qiime2.plugin import Plugin, SemanticType, TextFileFormat
from qiime2.plugin.model import SingleFileDirectoryFormat


from . import EchoContents


plugin = Plugin(
    name='q2-sundae',
    description='a test suite description',
    short_description='a test suite short description',
    version='0.0.0.dev',
    website='https://github.com/qiime2/q2galaxy',
    package='q2galaxy.test_suite',
    user_support_text='you broke it',
)


class _Undefined(TextFileFormat):
    def _validate_(self, level):
        pass


_UndefinedDir = SingleFileDirectoryFormat(
    '_UndefinedDir', 'echo.txt', _Undefined)

plugin.register_formats(_Undefined, _UndefinedDir)

IceCream = SemanticType('IceCream', field_names=['flavor'])
plugin.register_semantic_types(IceCream)


def _type_macro(name):
    t = SemanticType(name, variant_of=IceCream.field['flavor'])
    plugin.register_semantic_types(t)
    plugin.register_semantic_type_to_format(IceCream[t], _UndefinedDir)
    return t


Chocolate = _type_macro('Chocolate')
Vanilla = _type_macro('Vanilla')
Pistachio = _type_macro('Pistachio')


@plugin.register_transformer
def _1(contents: EchoContents) -> _Undefined:
    results = _Undefined()
    with results.open() as fh:
        fh.write(contents.value)
    return results


@plugin.register_transformer
def _2(ff: _Undefined) -> EchoContents:
    with ff.open() as fh:
        return EchoContents(fh.read())


def look_at_it(serving: EchoContents) -> EchoContents:
    return serving


def artifact_factory_1():
    x = EchoContents(value='neat')
    return Artifact.import_data('IceCream[Vanilla]', x)


def window_shopping(use):
    look_at_it = use.get_action('q2-sundae', 'look_at_it')
    use.scope.add_artifact('tasty', artifact_factory_1)

    use.comment('goodbye world')
    use.action(look_at_it, {'serving': 'tasty'}, {'untouched_serving': 'foo'})
    use.assert_has_line_matching(
        label='just checkin',
        result='foo',
        path='*/data/echo.txt',
        expression='.*',
    )


plugin.methods.register_function(
    function=look_at_it,
    inputs={'serving': IceCream[Vanilla]},
    parameters={},
    outputs=[('untouched_serving', IceCream[Vanilla])],
    input_descriptions={'serving': 'The most perfect ice cream ever.'},
    parameter_descriptions={},
    output_descriptions={'untouched_serving': 'Slightly warmer ice cream.'},
    name='Look at that ice cream!',
    description='Wow! So tasty! Will you _look_ at that ice cream?!',
    examples=[window_shopping],
)
