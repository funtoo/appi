# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
from pathlib import Path
import re

from ..base import AppiObject
from ..base.constant import PORTAGE_DIR, CONF_DIR

__all__ = [
    'Profile',
]


class Profile(AppiObject):

    directory = Path(PORTAGE_DIR, 'profiles')

    @classmethod
    def list(cls):
        base_dir = Path(CONF_DIR, 'make.profile')
        return cls._get_parent_profiles(base_dir)

    @classmethod
    def _get_parent_profiles(cls, base_dir):
        profiles_parent = base_dir / 'parent'
        profiles = []
        if not profiles_parent.exists():
            return profiles

        with profiles_parent.open('r') as f:
            for path in f.readlines():
                path = re.sub(r'#.*$', '', path)
                path = path.strip()
                if not path:
                    continue
                if path.startswith('gentoo:'):
                    path = cls.directory / path.split(':', 1)[1]
                elif path == ':base':
                    path = cls.directory / 'base'
                elif path[0] != '/':
                    path = base_dir / path
                else:
                    path = Path(path)
                path = path.resolve()
                new_profiles = [
                    x for x in cls._get_parent_profiles(path)
                    if x not in profiles
                ]
                profiles.extend(new_profiles)
                profile = cls(path)
                if profile not in profiles:
                    profiles.append(profile)

        return profiles

    def __init__(self, path):
        self.path = Path(path).resolve()

    def __eq__(self, profile):
        return self.path == profile.path

    def __str__(self):
        return str(self.path)
