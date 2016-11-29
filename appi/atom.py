# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
from functools import reduce
from pathlib import Path
import re

from .base import AppiObject, Attribute
from .base.exception import PortageError
from .base.util.decorator import cached
from .conf import Repository
from .ebuild import Ebuild
from .version import Version

__all__ = [
    'DependAtom', 'QueryAtom', 'AtomError',
]


class AtomError(PortageError):
    """Error related to an atom."""

    default_code = 'invalid'

    def __init__(self, message, atom, **kwargs):
        self.atom = atom
        super().__init__(message, atom=atom, **kwargs)


class AtomMetaclass(type(AppiObject)):

    def __new__(mcs, name, bases, attrs):
        parents = [b for b in bases if isinstance(b, AtomMetaclass)]
        if not parents:
            return super().__new__(mcs, name, bases, attrs)

        new_cls = super().__new__(mcs, name, bases, attrs)
        patterns = dict(map(
            lambda x: (x.name, '(?P<{}>{})'.format(x.name, x.get_regex())),
            new_cls._meta.attributes
        ))
        new_cls.atom_re = re.compile(new_cls.atom_re.format(**patterns))
        return new_cls


class BaseAtom(AppiObject, metaclass=AtomMetaclass):

    package = Attribute(
        help="The package name",
        regex=r'[a-zA-Z0-9+_-]+?',
        examples=['appi', 'portage', 'python'],
    )
    category = Attribute(
        help="The category name",
        regex=r'[a-z0-9]+(-[a-z0-9]+)?',
        examples=['dev-python', 'sys-apps', 'dev-lang'],
    )
    version = Attribute(
        help="The version number",
        regex=r'\d+(\.\d+)*[a-z]?(_(alpha|beta|pre|rc|p)\d+)*(-r\d+)?',
        examples=['0.1.0', '2.4.3-r1', '3.4.5'],
        type=Version,
    )
    slot = Attribute(
        help="The slot, subslot and slot operator",
        regex=r'\*|=|([0-9a-zA-Z_.-]+(/[0-9a-zA-Z_.-]+)?=?)',
        examples=['0=', '4.8.10', '3.4/3.4m'],
    )
    selector = Attribute(
        help="The version selector",
        choices=['<', '<=', '=', '>=', '>', '~'],
    )
    postfix = Attribute(
        help="The version postfix",
        choices=['*'],
    )

    def __init__(self, atom_string, strict=True):
        """Create an Atom object from a raw atom string.

        If `strict` is True, then the package category is required.
        """
        match = self.atom_re.match(atom_string)
        if not match:
            raise AtomError("{atom} is not a valid atom.", atom_string)

        self.raw_value = atom_string
        for k, v in match.groupdict().items():
            setattr(self, k, v)

        if strict and not self.category:
            raise AtomError(
                "{atom} may be ambiguous, please specify the category.",
                atom_string, code='missing_category')
        if self.version and not self.selector:
            raise AtomError(
                "Missing version selector, did you mean \"={atom}\"?",
                atom_string, code='missing_selector')
        if self.selector and not self.version:
            raise AtomError(
                "{atom} misses a version number.", atom_string,
                code='missing_version')
        if self.selector == '~' and '-r' in self.version:
            raise AtomError(
                "{atom} is invalid, you can't give a revision number with "
                "the '~' selector.", atom_string, code='unexpected_revision')
        if self.version and self.postfix == '*' and self.selector != '=':
            raise AtomError(
                "{atom} is invalid, '*' postfix can only be used with "
                "the '=' selector.", atom_string, code='unexpected_postfix')
    __init__.raises = [
        (AtomError, "the `atom_string` is not valid."),
    ]

    def __str__(self):
        return self.raw_value

    def get_version_glob_pattern(self) -> str:
        if not self.version or self.selector in ['>=', '>', '<', '<=']:
            return '*'
        if self.selector == '~' or self.postfix == '*':
            return self.version + '*'
        return self.version

    def get_glob_pattern(self) -> str:
        """Return a glob pattern that will match ebuild files that *MAY* match this atom.
        All matching ebuilds will be matched by the glob pattern,
        but not all files matched by the glob pattern will match the atom.
        """
        params = {
            'pkg': self.package,
            'cat': self.category or '*',
            'ver': self.get_version_glob_pattern(),
        }
        return '{cat}/{pkg}/{pkg}-{ver}.ebuild'.format(**params)

    @cached
    def list_matching_ebuilds(self) -> set:
        """Return the set of ebuilds matching this atom."""
        glob_pattern = self.get_glob_pattern()
        if getattr(self, 'repository', None):
            repository = self.get_repository()
            if not repository:
                return set()
            locations = [repository.location]
        else:
            locations = Repository.list_locations()
        paths = reduce(lambda x, y: x+y, (
            list(Path(d).glob(glob_pattern)) for d in locations))
        return {e for e in (Ebuild(p) for p in paths) if e.matches_atom(self)}

    def matches_existing_ebuild(self) -> bool:
        """Return True if this atom matches at least one existing ebuild."""
        return bool(self.list_matching_ebuilds())


class DependAtom(BaseAtom):
    """An atom used in ebuild dependencies."""

    prefix = Attribute(
        description="The extended prefix",
        choices=['!', '!!'],
    )
    use = Attribute(
        description="The USE dependencies",
        regex=r'[a-zA-Z0-9+_-]+?',
        examples=['appi', 'portage', 'python'],
    )

    atom_re = (r'^{prefix}?{selector}?({category}/)?{package}'
               r'(-{version}{postfix}?)?(:{slot})?(\[{use}\])?$')


class QueryAtom(BaseAtom):
    """An atom used for querying an ebuild.

    This kind of atom doesn't accept extended prefix and use dependencies, but
    accepts an overlay restriction.
    """

    repository = Attribute(
        description="The repository to fetch ebuilds",
        regex=r'[a-zA-Z0-9_-]+',
        examples=['gentoo', 'sapher', 'sabayon'],
    )

    atom_re = (r'^{selector}?({category}/)?{package}'
               r'(-{version}{postfix}?)?(:{slot})?(::{repository})?$')
