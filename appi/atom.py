# -*- coding: utf-8 -*-
from pathlib import Path
import re

from .base.constant import PORTAGE_DIR
from .base.exception import PortageError
from .base.util.decorator import cached
from .ebuild import Ebuild
from .version import Version

__all__ = [
    'Atom', 'QueryAtom', 'AtomError',
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
        - selector: the version selector (>=, <=, <, =, > or ~)
        - ext_prefix: the extended prefix (! or !!)
        - use: the use dependency
        - overlay: not used in this class, but in subclasses

    See also: ebuild(5) man pages
    """

    portage_dir = PORTAGE_DIR

    patterns = dict(map(lambda x: (x[0], '(?P<{}>{})'.format(x[0], x[1])), [
        ('ext_prefix', r'!!?'),
        ('selector', r'>=|<=|<|=|>|~'),
        ('category', r'[a-z0-9]+(-[a-z0-9]+)?'),
        ('package', r'[a-zA-Z0-9+_-]+?'),
        ('version', r'\d+(\.\d+)*[a-z]?(_(alpha|beta|pre|rc|p)\d+)*(-r\d+)?\*?'),
        ('slot', r'\*|=|([0-9a-zA-Z_.-]+(/[0-9a-zA-Z_.-]+)?=?)'),
        ('use', r'[-!]?[a-z][a-z0-9_-]*[?=]?(,[-!]?[a-z][a-z0-9_-]*[?=]?)*'),
        ('overlay', r'[a-za-Z0-9_-]+'),
    ]))

    atom_re = re.compile((
        r'^{ext_prefix}?{selector}?({category}/)?{package}'
        r'(-{version})?(:{slot})?(\[{use}\])?$'
    ).format(**patterns))

    def __init__(self, atom_string, strict=True):
        """Create an Atom object from a raw atom string.
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
        if self.version and self.version[-1] == '*' and self.selector != '=':
            raise AtomError(
                "{atom} is invalid, '*' postfix can only be used with "
                "the '=' selector.", atom_string, code='unexpected_postfix')

    def __str__(self):
        return self.raw_value

    def __repr__(self):
        return "<Atom: '{}'>".format(str(self))

    def get_version(self):
        """Return the version as Version object."""
        version = self.version
        if not version:
            return None
        if version[-1] == '*':
            version = version[:-1]
        return Version(version)

    def get_version_glob_pattern(self):
        if not self.version or self.selector in ['>=', '>', '<', '<=']:
            return '*'
        if self.selector == '~':
            return self.version + '*'
        return self.version

    def get_glob_pattern(self):
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
    def list_matching_ebuilds(self):
        """Return the set of ebuilds matching this atom."""
        paths = Path(self.portage_dir).glob(self.get_glob_pattern())
        return {e for e in (Ebuild(p) for p in paths) if e.matches_atom(self)}

    def matches_existing_ebuild(self):
        """Return True if this atom matches at least one existing ebuild."""
        return bool(self.list_matching_ebuilds())


class QueryAtom(Atom):
    """An atom used for querying an ebuild.
    This kind of atom doesn't accept extended prefix and use dependencies, but
    accepts an overlay restriction.
    """

    atom_re = re.compile((
        r'^{selector}?({category}/)?{package}(-{version})?'
        r'(:{slot})?(::{overlay})?$'
    ).format(**Atom.patterns))
