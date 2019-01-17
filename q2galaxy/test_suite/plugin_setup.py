from qiime2.plugin import (
    Plugin, SemanticType, SingleFileDirectoryFormat, TextFileFormat)


from . import EchoContents


plugin = Plugin(
    name='q2galaxy-test-suite',
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

_Squadron = SemanticType('_Squadron', fields='color')
plugin.register_semantic_types(_Squadron)


def _type_macro(name):
    t = SemanticType(name, variant_of=_Squadron.field['color'])
    plugin.register_semantic_types(t)
    plugin.register_semantic_type_to_format(_Squadron[t], _UndefinedDir)
    return t


_Red = _type_macro('_Red')
_Gold = _type_macro('_Gold')
_Green = _type_macro('_Green')


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
