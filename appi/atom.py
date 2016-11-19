# -*- coding: utf-8 -*-
from pathlib import Path
import re

from .base.constant import PORTAGE_DIR
from .base.exception import PortageError
from .base.util.decorator import cached
from .ebuild import Ebuild

__all__ = [
    'Atom', 'SimpleAtom', 'AtomError',
]


class AtomError(PortageError):
    """Error related to an atom."""

    default_code = 'invalid'

    def __init__(self, message, atom, **kwargs):
        self.atom = atom
        super().__init__(message, atom=atom, **kwargs)


class Atom:
    """An ebuild atom with the following properties:

        - package: the package name
        - category: the category name
        - version: the version number
        - slot: the slot, subslot and slot operator
        - prefix: the version selector (>=, <=, <, =, > or ~)
        - ext_prefix: the extended prefix (! or !!)
        - use: the use dependency

    See also: ebuild(5) man pages
    """

    portage_dir = PORTAGE_DIR

    patterns = dict(map(lambda x: (x[0], '(?P<{}>{})'.format(x[0], x[1])), [
        ('ext_prefix', r'!!?'),
        ('prefix', r'>=|<=|<|=|>|~'),
        ('category', r'[a-z0-9]+(-[a-z0-9]+)?'),
        ('package', r'[a-zA-Z0-9+_-]+?'),
        ('version', r'[0-9]+(\.[0-9]+)*[a-z]?(_(alpha|beta|pre|rc|p)[0-9]+)*(-r[0-9]+)?\*?'),
        ('slot', r'\*|=|([0-9a-zA-Z_.-]+(/[0-9a-zA-Z_.-]+)?=?)'),
        ('use', r'[-!]?[a-z][a-z0-9_-]*[?=]?(,[-!]?[a-z][a-z0-9_-]*[?=]?)*'),
    ]))

    atom_re = re.compile((
        r'^{ext_prefix}?{prefix}?({category}/)?{package}'
        r'(-{version})?(:{slot})?(\[{use}\])?$'
    ).format(**patterns))

    def __init__(self, atom_string, strict=True):
        """Create an atom object from a raw atom string.
        If `strict` is `True`, then the package category is required.
        Raise `AtomError` if the atom string is not valid.
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
        if self.version and not self.prefix:
            raise AtomError(
                "Missing version prefix, did you mean \"={atom}\"?",
                atom_string, code='missing_prefix')
        if self.prefix and not self.version:
            raise AtomError(
                "{atom} misses a version number.", atom_string,
                code='missing_version')

    def get_version_glob_pattern(self):
        if not self.version or self.prefix in ['>=', '>', '<', '<=']:
            return '*'
        if self.prefix == '~':
            return self.version + '*'
        return self.version

    def get_glob_pattern(self):
        params = {
            'pkg': self.package,
            'cat': self.category or '*',
            'ver': self.get_version_glob_pattern(),
        }
        return '{cat}/{pkg}/{pkg}-{ver}.ebuild'.format(**params)

    @cached
    def list_matching_ebuilds(self):
        paths = Path(self.portage_dir).glob(self.get_glob_pattern())
        return {e for e in (Ebuild(p) for p in paths) if e.matches_atom(self)}

    def exists(self):
        return bool(self.list_matching_ebuilds())


class SimpleAtom(Atom):
    """An atom that doesn't accept extended prefix and use dependency."""

    atom_re = re.compile((
        r'^{prefix}?({category}/)?{package}(-{version})?(:{slot})?$'
    ).format(**Atom.patterns))
