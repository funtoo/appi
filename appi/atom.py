# -*- coding: utf-8 -*-
import re

__all__ = [
    'Atom', 'SimpleAtom', 'AtomError',
]


class AtomError(Exception):
    """Error related to an atom."""

    def __init__(self, message, atom_string):
        self.message = message
        self.atom_string = atom_string

    def __str__(self):
        return self.message.format(atom=self.atom_string)


class Atom:

    patterns = dict(map(lambda x: (x[0], '(?P<{}>{})'.format(x[0], x[1])), [
        ('ext_prefix', r'!!?'),
        ('prefix', r'>=|<=|<|=|>|~'),
        ('category', r'[a-z0-9]+(-[a-z0-9]+)?'),
        ('package', r'[a-zA-Z0-9_-]+'),
        ('version', r'[0-9]+(\.[0-9]+)*[a-z]?(_(alpha|beta|pre|rc|p)[0-9]+)*(-r[0-9]+)?'),
        ('slot', r'\*|=|([0-9a-zA-Z_.-]+(/[0-9a-zA-Z_.-]+)?=?)'),
    ]))

    atom_re = re.compile((
        r'^{ext_prefix}?{prefix}?({category}/)?{package}'
        r'(-{version})?(:{slot})?$'
    ).format(**patterns))

    def __init__(self, atom_string, strict=True):
        match = self.atom_re.match(atom_string)
        if not match:
            raise AtomError("{atom} is not a valid atom.", atom_string)

        self.raw_value = atom_string
        for k, v in match.groupdict().items():
            setattr(self, k, v)

        if strict and not self.category:
            raise AtomError("{atom} may be ambiguous, please specify the category.", atom_string)
        if self.version and not self.prefix:
            raise AtomError("Missing version prefix, did you mean \"={atom}\"?", atom_string)
        if self.prefix and not self.version:
            raise AtomError("{atom} misses a version number.", atom_string)


class SimpleAtom(Atom):

    atom_re = re.compile((
        r'^{prefix}?({category}/)?{package}(-{version})?(:{slot})?$'
    ).format(**Atom.patterns))
