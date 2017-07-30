# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
import os
import re
import subprocess

from .base import constant, AppiObject
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
        self.path = path

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
        valid_category = not atom.category or self.category == atom.category
        valid_package = self.package == atom.package
        valid_repository = not atom_repository or (
            self.repository and self.repository.name == atom_repository)
        if not (valid_category and valid_package and valid_repository):
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

    @property
    def vars(self):
        """A dictionnary containing ebuild raw variables."""
        if not hasattr(self, '_vars'):
            self._parse_ebuild_file()
        return self._vars

    def get_ebuild_env(self):
        """Return a dictionnary of ebuild predefined read-only variables."""
        # TODO How to fill commented out variables? Should it be filled?
        version = self.get_version()
        upstream_version = str(version.get_upstream_version())
        revision = 'r' + (version.revision or '0')
        return dict(
            P='{}-{}'.format(self.package, upstream_version),
            PN=self.package,
            PV=upstream_version,
            PR=revision,
            PVR=self.version,
            PF='{}-{}'.format(self.package, self.version),
            # A='',
            CATEGORY=self.category,
            # FILESDIR='',
            # WORKDIR='',
            # T='',
            # D='',
            # HOME='',
            # ROOT='',
            # DISTDIR='',
            # EPREFIX='',
            # ED='',
            # EROOT='',
        )

    @classmethod
    def _clean_ebuild_raw_vars(cls, raw_vars):
        """Extract actual values from raw variables values retrieved with bash
        'set' command.
        """
        cleaned_vars = {}
        for k, v in raw_vars.items():
            v = re.sub(rb'\n$', b'', v)
            v = re.sub(rb"^\$?'(.*)'$", rb'\1', v)
            cleaned_vars[k] = v.decode('unicode_escape')
        return cleaned_vars

    def _parse_ebuild_file(self):
        """Execute the ebuild file and export ebuild-related variables to
        `self._vars` dictionnary.
        """
        bin_path = constant.BIN_PATH
        cmd = ['bash', '-c', 'source {}/ebuild.sh && set'.format(bin_path)]
        repo_locations = (str(l) for l in Repository.list_locations())
        env = dict(
            os.environ,
            PORTAGE_PIPE_FD='2',  # TODO How to set something else than stderr?
            PORTAGE_ECLASS_LOCATIONS=' '.join(repo_locations),
            EBUILD=self.path,
            EBUILD_PHASE='depend',  # TODO Is this an ideal phase?
            PORTAGE_BIN_PATH=bin_path,
            PORTAGE_TMPDIR='/var/tmp',  # TODO properly get this path
        )
        env.update(self.get_ebuild_env())
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env)

        raw_vars = {}
        ebuild_vars = {
            'EAPI', 'DESCRIPTION', 'HOMEPAGE', 'SRC_URI', 'LICENSE', 'SLOT',
            'KEYWORDS', 'IUSE', 'REQUIRED_USE', 'RESTRICT', 'DEPEND',
            'RDEPEND', 'PDEPEND', 'S', 'PROPERTIES', 'DOCS', 'HTML_DOCS',
        }
        for line in proc.stdout:
            key, _, value = line.partition(b'=')
            key = key.decode('ascii')
            if key in ebuild_vars:
                raw_vars[key] = value
        proc.communicate()
        self._vars = self._clean_ebuild_raw_vars(raw_vars)
