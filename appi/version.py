# -*- coding: utf-8 -*-
import re

from .base.exception import PortageError

__all__ = [
    'Version', 'VersionError',
]


class VersionError(PortageError):
    """Error related to a package version."""

    default_code = 'invalid'

    def __init__(self, message, version, **kwargs):
        self.version = version
        super().__init__(message, version=version, **kwargs)


class Version:

    version_re = re.compile(
        r'^(?P<base>\d+(\.\d+)*)(?P<letter>[a-z]?)'
        r'(?P<suffix>(_(alpha|beta|pre|rc|p)\d+)*)?(-r(?P<revision>\d+))?$'
    )
    suffix_re = re.compile(r'^(?P<name>[a-z]+)(?P<value>\d+)$')
    suffix_values = {'alpha': -4, 'beta': -3, 'pre': -2, 'rc': -1, 'p': 0}

    selector_to_comp_method = {
        '>=': '__ge__',
        '<=': '__le__',
        '!=': '__ne__',
        '=': '__eq__',
        '<': '__lt__',
        '>': '__gt__',
        '^': 'startswith',
    }

    @classmethod
    def version_tuple_compare(cls, t1, t2):
        if t1 == t2:
            return 0
        if not isinstance(t1, tuple):
            # Here, neither t1 nor t2 is a tuple
            if t1 < t2:
                return -1
            else:
                return 1
        # Here, both t1 and t2 are tuples
        for v1, v2 in zip(t1, t2):
            comp = cls.version_tuple_compare(v1, v2)
            if comp != 0:
                return comp
        if len(t1) < len(t2):
            return -1
        if len(t1) > len(t2):
            return 1
        raise AssertionError("How did you get here anyway?!")

    def __init__(self, version_string):
        match = self.version_re.match(version_string)
        if not match:
            raise VersionError(
                "{version} is not a valid version.", version_string)

        for k, v in match.groupdict().items():
            setattr(self, k, v)

    def __str__(self):
        return '{base}{letter}{suffix}{revision}'.format(
            base=self.base, letter=self.letter or '', suffix=self.suffix or '',
            revision=('-r' + self.revision if self.revision else ''))

    def __repr__(self):
        return "<Version: '{}'>".format(str(self))

    def __abs__(self):
        return Version('{base}{letter}{suffix}'.format(
            base=self.base, letter=self.letter or '',
            suffix=self.suffix or ''))

    def __gt__(self, other):
        return self.compare(other) > 0

    def __lt__(self, other):
        return self.compare(other) < 0

    def __ge__(self, other):
        return self.compare(other) >= 0

    def __le__(self, other):
        return self.compare(other) <= 0

    def __eq__(self, other):
        return self.compare(other) == 0

    def __ne__(self, other):
        return self.compare(other) != 0

    def get_version_tuple(self):
        return (
            self.get_base_tuple(), self.get_letter_tuple(),
            self.get_suffix_tuple(), self.get_revision_tuple(),
        )

    def get_base_tuple(self):
        """Leading 0 can be omitted for the major version number, but should be
        considered as decimal parts for the next version numbers.
        """
        base = self.base.split('.')
        return (int(base[0]),) + tuple(
            map(lambda x: float('0.' + x), base[1:])
        )

    def get_letter_tuple(self):
        return ord(self.letter) - 96 if self.letter else 0

    def get_suffix_tuple(self):
        if not self.suffix:
            return ((0, -1),)
        suffix_tuple = tuple()
        suffixes = self.suffix[1:].split('_')
        for suffix in suffixes:
            match = self.suffix_re.match(suffix)
            suffix_tuple += ((
                self.suffix_values[match.group('name')],
                int(match.group('value'))
            ),)
        return suffix_tuple

    def get_revision_tuple(self):
        return int(self.revision) if self.revision else 0

    def compare(self, other):
        self_tuple = self.get_version_tuple()
        other_tuple = other.get_version_tuple()
        return self.version_tuple_compare(self_tuple, other_tuple)

    def startswith(self, version):
        return str(self).startswith(str(version))
