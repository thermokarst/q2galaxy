import os
import json

from .errors import CondaPackageNotFound


def get_conda_prefix():
    conda_prefix = os.getenv('CONDA_PREFIX')
    if conda_prefix is None:
        raise RuntimeError("Not in a conda environment.")

    return conda_prefix


class CondaMeta:
    def __init__(self, prefix):
        self.prefix = prefix
        self.meta = os.path.join(self.prefix, 'conda-meta')
        self._cache = {}

        self.meta_lookup = {}
        for filename in os.listdir(self.meta):
            if filename.endswith('.json'):
                name = filename.rsplit('-', 2)[0]
                self.meta_lookup[name] = os.path.join(self.meta, filename)

    def __getitem__(self, package):
        if package not in self._cache:
            try:
                with open(self.meta_lookup[package]) as fh:
                    self._cache[package] = json.load(fh)
            except KeyError:
                raise CondaPackageNotFound(package)

        return self._cache[package]

    def iter_primary_deps(self, package):
        yield from (dep.split(' ')[0] for dep in self[package]['depends'])

    def iter_deps(self, package, *, include_self=True, _seen=None):
        if _seen is None:
            _seen = set()

        if include_self:
            yield package

        for dependency in self.iter_primary_deps(package):
            if dependency in _seen:
                continue
            else:
                _seen.add(dependency)
                yield from self.iter_deps(dependency, _seen=_seen)

    def get_version(self, package):
        return self[package]['version']


def extract_environment(conda_package):
    prefix = get_conda_prefix()
    meta = CondaMeta(prefix)

    env = {}
    for d in meta.iter_deps(conda_package, include_self=True):
        env[d] = meta.get_version(d)

    return env
