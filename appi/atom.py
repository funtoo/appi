# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
from functools import reduce
from pathlib import Path
import re

from .base import constant, AppiObject
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


class BaseAtom(AppiObject):
    """An ebuild atom with the following properties:

        - package: the package name
        - category: the category name
        - version: the version number
        - slot: the slot, subslot and slot operator
        - selector: the version selector (>=, <=, <, =, > or ~)
        - prefix: the extended prefix (! or !!)
        - postfix: the extended postfix (*)
        - use: the use dependency
        - repository: not used in this class, but in subclasses
    """

    patterns = dict(map(lambda x: (x[0], '(?P<{}>{})'.format(x[0], x[1])), [
        ('prefix', r'!!?'),
        ('selector', r'>=|<=|<|=|>|~'),
        ('category', r'[a-z0-9]+(-[a-z0-9]+)?'),
        ('package', r'[a-zA-Z0-9+_-]+?'),
        ('version', r'\d+(\.\d+)*[a-z]?(_(alpha|beta|pre|rc|p)\d*)*(-r\d+)?'),
        ('postfix', r'\*'),
        ('slot', r'\*|=|([0-9a-zA-Z_.-]+(/[0-9a-zA-Z_.-]+)?[=*]?)'),
        ('use', r'[-!]?[a-z][a-z0-9_-]*[?=]?(,[-!]?[a-z][a-z0-9_-]*[?=]?)*'),
        ('repository', r'[a-zA-Z0-9_-]+'),
    ]))

    def __init__(self, atom_string, strict=True):
        """Create an Atom object from a raw atom string.
        If `strict` is `True`, then the package category is required.
        Raise `AtomError` if the atom string is not valid.
        """
        match = self.atom_re.match(atom_string)
        if not match:
            raise AtomError("{atom} is not a valid atom.", atom_string)

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

    def get_version(self):
        """Return the version as Version object."""
        version = self.version
        if not version:
            return None
        return Version(version)

    def _get_version_glob_pattern(self):
        """Returns the version part of the glob pattern.

        See BaseAtom.get_glob_pattern()
        """
        if not self.version or self.selector in ['>=', '>', '<', '<=']:
            return '*'
        if self.selector == '~' or self.postfix == '*':
            return self.version + '*'
        return self.version

    def _get_glob_pattern(self):
        """Return a glob pattern that will match ebuild files that *MAY* match this atom.
        All matching ebuilds will be matched by the glob pattern,
        but not all files matched by the glob pattern will match the atom.

        The returned glob pattern starts from repositories root.
        """
        params = {
            'pkg': self.package,
            'cat': self.category or '*',
            'ver': self._get_version_glob_pattern(),
        }
        return '{cat}/{pkg}/{pkg}-{ver}.ebuild'.format(**params)

    @cached
    def list_matching_ebuilds(self):
        """Return the set of ebuilds matching this atom."""
        glob_pattern = self._get_glob_pattern()
        if getattr(self, 'repository', None):
            repository = self.get_repository()
            if not repository:
                return set()
            locations = [repository['location']]
        else:
            locations = Repository.list_locations()
        paths = reduce(lambda x, y: x+y, (
            list(Path(d).glob(glob_pattern)) for d in locations))
        paths += list(Path(constant.PACKAGE_DB_PATH).glob(re.sub(
            r'{0}/({0}-.*)\.ebuild$'.format(re.escape(self.package)),
            r'\1/\1.ebuild', glob_pattern
        )))
        return {e for e in (Ebuild(p) for p in paths) if e.matches_atom(self)}

    def matches_existing_ebuild(self):
        """Return True if this atom matches at least one existing ebuild."""
        return bool(self.list_matching_ebuilds())

    def list_possible_useflags(self):
        """Return the set of useflags supported by at least one of the
        matching ebuilds.
        """
        return set.union(*(e.useflags for e in self.list_matching_ebuilds()))

    def is_installed(self):
        """Return True if any of the matching ebuilds is installed.
        False otherwise.
        """
        for ebuild in self.list_matching_ebuilds():
            if ebuild.is_installed():
                return True
        return False

    def is_in_tree(self):
        """Return True if any of the matching ebuilds is available in the
        repository. False otherwise.
        """
        for ebuild in self.list_matching_ebuilds():
            if ebuild.is_in_tree():
                return True
        return False


class DependAtom(BaseAtom):
    """An atom used in ebuild dependencies."""

    atom_re = re.compile((
        r'^{prefix}?{selector}?({category}/)?{package}(-{version}{postfix}?)?'
        r'(:{slot})?(\[{use}\])?$'
    ).format(**BaseAtom.patterns))

    def __str__(self):
        template = ''
        if self.prefix:
            template += '{prefix}'
        if self.selector:
            template += '{selector}'
        if self.category:
            template += '{category}/'
        template += '{package}'
        if self.version:
            template += '-{version}'
        if self.postfix:
            template += '{postfix}'
        if self.slot:
            template += ':{slot}'
        if self.use:
            template += '[{use}]'
        return template.format(
            prefix=self.prefix, selector=self.selector, category=self.category,
            package=self.package, version=self.version, postfix=self.postfix,
            slot=self.slot, use=self.use)


class QueryAtom(BaseAtom):
    """An atom used for querying an ebuild."""

    atom_re = re.compile((
        r'^{selector}?({category}/)?{package}(-{version}{postfix}?)?'
        r'(:{slot})?(::{repository})?$'
    ).format(**BaseAtom.patterns))

    def __init__(self, atom_string, *args, **kwargs):
        super().__init__(atom_string, *args, **kwargs)
        if self.slot and self.slot[-1] == '*':
            raise AtomError(
                "{atom} is invalid, '*' slot operator is not acceptable for a "
                "QueryAtom.", atom_string, code='unexpected_slot_operator')

    def __str__(self):
        template = ''
        if self.selector:
            template = '{selector}'
        if self.category:
            template += '{category}/'
        template += '{package}'
        if self.version:
            template += '-{version}'
        if self.postfix:
            template += '{postfix}'
        if self.slot:
            template += ':{slot}'
        if self.repository:
            template += '::{repository}'
        return template.format(
            selector=self.selector, category=self.category,
            package=self.package, version=self.version, postfix=self.postfix,
            slot=self.slot, repository=self.repository)

    def get_repository(self):
        """Return the repository as `Repository` object if provided.
        Return None otherwise.
        """
        if not self.repository:
            return None
        return Repository.get(self.repository)
