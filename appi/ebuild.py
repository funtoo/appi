# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
import re

from .base import AppiObject
from .base.exception import PortageError
from .conf import Repository
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


class Ebuild(AppiObject):
    """An ebuild file. It defines the following properties:

        - category
        - package
        - version
        - repository

    This is not yet implemented, but it should also be able to determine some
    properties defined in the ebuild file:

        - use flags
        - slots
        - license
        - home page
        - description
        - ...
    """

    path_re = re.compile(
        r'^(?P<repo_location>/.*/)'
        r'(?P<category>[^/]+?)/(?P<package>[^/]+?)/(?P<package_check>[^/]+?)-'
        r'(?P<version>\d+(\.\d+)*[a-z]?(_(alpha|beta|pre|rc|p)\d+)*(-r\d+)?)'
        r'\.ebuild$'
    )

    def __init__(self, path):
        """Create an Ebuild object from an ebuild path.
        The path may be either absolute, or relative from a portage directory.
        Raise `EbuildError` if the path does not describe a valid ebuild.
        """
        path = str(path)
        match = self.path_re.match(path)
        if not match:
            raise EbuildError("{ebuild} is not a valid ebuild path.", path)

        group_dict = match.groupdict()
        package_check = group_dict.pop('package_check')
        repo_location = group_dict.pop('repo_location')
        for k, v in group_dict.items():
            setattr(self, k, v)

        if self.package != package_check:
            raise EbuildError(
                "Package name mismatch in \"{ebuild}\": {pkg1} != {pkg2}",
                path, pkg1=self.package, pkg2=package_check,
                code='package_name_mismatch')

        self.repository = Repository.find(location=repo_location)

    def __str__(self):
        template = '{cat}/{pkg}-{ver}'
        info = dict(cat=self.category, pkg=self.package, ver=self.version)
        if self.repository:
            template += '::{repo}'
            info['repo'] = self.repository.name
        return template.format(**info)

    def get_version(self):
        """Return the version as Version object."""
        return Version(self.version)

    def matches_atom(self, atom):
        """Return True if this ebuild matches the given atom.
        This method still lacks SLOT check.
        """
        atom_repository = getattr(atom, 'repository', None)
        if atom.category and self.category != atom.category:
            return False
        if self.package != atom.package:
            return False
        if atom_repository and (not self.repository or
                                self.repository.name != atom_repository):
            return False
        if atom.version:
            v1 = self.get_version()
            v2 = atom.get_version()
            selector = atom.selector
            if atom.postfix == '*':
                selector = '^'
            if selector == '~':
                v1 = v1.get_upstream_version()
                selector = '='
            comp_method = Version.selector_to_comp_method[selector]
            if not getattr(v1, comp_method)(v2):
                return False
        return True
