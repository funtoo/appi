# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
from pathlib import Path
import re

from .base.exception import PortageError
from .base.constant import PORTAGE_DIR
from .version import Version

__all__ = [
    'Ebuild', 'EbuildError',
]


class EbuildError(PortageError):
    """Error related to an ebuild."""

    default_code = 'invalid'

    def __init__(self, message, ebuild, **kwargs):
        self.ebuild = ebuild
        super().__init__(message, ebuild=ebuild, **kwargs)


class Ebuild:
    """An ebuild file. It defines the following properties:

        - category
        - package
        - version

    This is not yet implemented, but it should also be able to determine some
    properties defined in the ebuild file:

        - use flags
        - slots
        - license
        - home page
        - description
        - ...
    """

    portage_dir = PORTAGE_DIR

    path_re = re.compile(
        r'^.*/(?P<category>[^/]+?)/(?P<package>[^/]+?)/(?P<package_check>[^/]+?)-'
        r'(?P<version>\d+(\.\d+)*[a-z]?(_(alpha|beta|pre|rc|p)\d+)*(-r\d+)?)'
        r'\.ebuild$'
    )

    def __init__(self, path):
        """Create an Ebuild object from an ebuild path.
        The path may be either absolute, or relative from a portage directory.
        Raise `EbuildError` if the path does not describe a valid ebuild.
        """
        if not isinstance(path, Path):
            path = str(path)
            if path[0] == '/':
                path = Path(path)
            else:
                path = Path(self.portage_dir) / path
        raw_path = str(path)
        match = self.path_re.match(raw_path)
        if not match:
            raise EbuildError("{ebuild} is not a valid ebuild path.", raw_path)

        group_dict = match.groupdict()
        package_check = group_dict.pop('package_check')
        for k, v in group_dict.items():
            setattr(self, k, v)

        if self.package != package_check:
            raise EbuildError(
                "Package name mismatch in \"{ebuild}\": {pkg1} != {pkg2}",
                raw_path, pkg1=self.package, pkg2=package_check,
                code='package_name_mismatch')

    def __str__(self):
        return '{cat}/{pkg}-{ver}'.format(
            cat=self.category, pkg=self.package, ver=self.version)

    def __repr__(self):
        return "<Ebuild: '{}'>".format(str(self))

    def get_version(self):
        """Return the version as Version object."""
        return Version(self.version)

    def matches_atom(self, atom):
        """Return True if this ebuild matches the given atom.
        This method still lacks SLOT check.
        """
        if atom.category and self.category != atom.category:
            return False
        if self.package != atom.package:
            return False
        if atom.version:
            v1 = self.get_version()
            v2 = atom.get_version()
            selector = atom.selector
            if atom.version[-1] == '*':
                selector = '^'
            elif selector == '~':
                v1 = abs(v1)
                selector = '='
            comp_method = Version.selector_to_comp_method[selector]
            if not getattr(v1, comp_method)(v2):
                return False
        return True
