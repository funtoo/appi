# -*- coding: utf-8 -*-
import re

__all__ = [
    'Atom', 'SimpleAtom', 'AtomError',
]


class AtomError(Exception):
    """Error related to an atom."""

    def __init__(self, message, atom_string, code=None):
        self.message = message
        self.atom_string = atom_string
        self.code = code or 'invalid'

    def __str__(self):
        return self.message.format(atom=self.atom_string)


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

    patterns = dict(map(lambda x: (x[0], '(?P<{}>{})'.format(x[0], x[1])), [
        ('ext_prefix', r'!!?'),
        ('prefix', r'>=|<=|<|=|>|~'),
        ('category', r'[a-z0-9]+(-[a-z0-9]+)?'),
        ('package', r'[a-zA-Z0-9_-]+'),
        ('version', r'[0-9]+(\.[0-9]+)*[a-z]?(_(alpha|beta|pre|rc|p)[0-9]+)*(-r[0-9]+)?'),
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


class SimpleAtom(Atom):
    """An atom that doesn't accept extended prefix and use dependency."""

    atom_re = re.compile((
        r'^{prefix}?({category}/)?{package}(-{version})?(:{slot})?$'
    ).format(**Atom.patterns))
