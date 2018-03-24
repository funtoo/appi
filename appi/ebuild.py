# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
from hashlib import sha1
import os
from pathlib import Path
import re

from .base import constant, AppiObject
from .base.exception import PortageError
from .conf import Repository, Profile
from .util import extract_bash_file_vars
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
        - location
        - useflags
        - slot
        - subslot
        - vars

    You can access to more information through the `vars` property, such as the
    description, the home page, and the license of the ebuild.
    """

    path_re = re.compile(
        r'^(?P<repo_location>/.*/)'
        r'(?P<category>[^/]+?)/(?P<package>[^/]+?)/(?P<package_check>[^/]+?)-'
        r'(?P<version>\d+(\.\d+)*[a-z]?(_(alpha|beta|pre|rc|p)\d*)*(-r\d+)?)'
        r'\.ebuild$'
    )
    pkg_db_re = re.compile(
        constant.PACKAGE_DB_PATH + '/'
        r'(?P<category>[^/]+?)/(?P<package>[^/]+?)'
        r'-(?P<version>\d+(\.\d+)*[a-z]?(_(alpha|beta|pre|rc|p)\d*)*(-r\d+)?)/'
        r'.*\.ebuild$'
    )

    def __init__(self, path):
        """Create an Ebuild object from an ebuild path.
        The path may be either absolute, or relative from a portage directory.
        Raise `EbuildError` if the path does not describe a valid ebuild.
        """
        path = str(path)
        if path.startswith(constant.PACKAGE_DB_PATH + '/'):
            match = self.pkg_db_re.match(path)
            if not match:
                raise EbuildError("{ebuild} is not a valid ebuild path.", path)
            group_dict = match.groupdict()
            for k, v in group_dict.items():
                setattr(self, k, v)
            with (self.db_dir / 'repository').open(encoding='utf-8') as f:
                self.repo_name = f.read().strip()
            self.repository = Repository.get(self.repo_name)
        else:
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
            self.repo_name = self.repository.name if self.repository else None
        self.location = Path(path)

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
        """Return True if this ebuild matches the given atom."""
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
        if atom.slot:
            m = re.search(r'^(.+?)(?:/(.+?))?(?:[=*])?$', atom.slot)
            slot = m.group(1)
            subslot = m.group(2)
            if slot != self.slot or (subslot and subslot != self.subslot):
                return False
        return True

    def __hash__(self):
        return int(sha1(str(self).encode('utf-8')).hexdigest(), 16)

    def __eq__(self, other):
        return hash(self) == hash(other)

    @property
    def vars(self):
        """A dictionnary containing ebuild raw variables."""
        if not hasattr(self, '_vars'):
            self._parse_ebuild_file()
        return self._vars

    @property
    def useflags(self):
        """The set of useflags supported by this ebuild according to IUSE."""
        return set(re.findall('[+-]?([^\s]+)', self.vars['IUSE']))

    @property
    def slot(self):
        """The slot of the package."""
        return re.search(r'^(.+?)(?:/(.+))?$', self.vars['SLOT']).group(1)

    @property
    def subslot(self):
        """The subslot of the package if any. None otherwise"""
        return re.search(r'^(.+?)(?:/(.+))?$', self.vars['SLOT']).group(2)

    @property
    def db_dir(self):
        """The directory where information about this package installation
        can be found (if it is installed).
        """
        dirname = '{}-{}'.format(self.package, self.version)
        return Path(constant.PACKAGE_DB_PATH) / self.category / dirname

    def get_ebuild_env(self):
        """Return a dictionnary of ebuild predefined read-only variables."""
        # TODO How to fill commented out variables? Should it be filled?
        # Cf. GitLab#12
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

    def _parse_ebuild_file(self):
        """Execute the ebuild file and export ebuild-related variables to
        `self._vars` dictionnary.
        """
        make_conf = Profile.get_system_make_conf()
        path = Path(constant.BIN_PATH, 'ebuild.sh')
        repo_locations = (str(l) for l in Repository.list_locations())
        ebuild_vars = {
            'EAPI', 'DESCRIPTION', 'HOMEPAGE', 'SRC_URI', 'LICENSE', 'SLOT',
            'KEYWORDS', 'IUSE', 'REQUIRED_USE', 'RESTRICT', 'DEPEND',
            'RDEPEND', 'PDEPEND', 'S', 'PROPERTIES', 'DOCS', 'HTML_DOCS',
        }
        context = dict(
            os.environ,
            PORTAGE_PIPE_FD='2',  # TODO How to set something else than stderr?
                                  # Cf. GitLab#12
            PORTAGE_ECLASS_LOCATIONS=' '.join(repo_locations),
            EBUILD=str(self.location),
            EBUILD_PHASE='depend',  # TODO Is this an ideal phase?
                                    # Cf. GitLab#12
            PORTAGE_BIN_PATH=constant.BIN_PATH,
            PORTAGE_TMPDIR=make_conf['PORTAGE_TMPDIR'],
        )
        context.update(self.get_ebuild_env())
        self._vars = extract_bash_file_vars(path, ebuild_vars, context)

    def is_installed(self):
        """Return True if this ebuild is installed. False otherwise."""
        if self.repo_name and self.db_dir.exists():
            with (self.db_dir / 'repository').open(encoding='utf-8') as f:
                return f.read().strip() == self.repo_name
        return False

    def is_in_tree(self):
        """Return True if this ebuild is available in the repository.
        False otherwise.
        """
        if self.repository:
            location = (
                self.repository['location'] / self.category / self.package /
                '{}-{}.ebuild'.format(self.package, self.version)
            )
            if location.exists():
                return True
        return False
