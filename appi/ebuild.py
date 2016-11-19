# -*- coding: utf-8 -*-
from pathlib import Path
import re

from .base.exception import PortageError
from .base.constant import PORTAGE_DIR

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

    portage_dir = PORTAGE_DIR

    path_re = re.compile(
        r'^.*/(?P<category>[^/]+?)/(?P<package>[^/]+?)/(?P<package_check>[^/]+?)-'
        r'(?P<version>[0-9]+(\.[0-9]+)*[a-z]?(_(alpha|beta|pre|rc|p)[0-9]+)*(-r[0-9]+)?)'
        r'\.ebuild$'
    )

    def __init__(self, path):
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

    def matches_atom(self, atom):
        if atom.category and self.category != atom.category:
            return False
        if self.package != atom.package:
            return False
        if atom.version:
            pass  # TODO
        return True
