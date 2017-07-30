# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
from pathlib import Path
import re

from ..base import AppiObject, constant
from ..util import extract_bash_file_vars

__all__ = [
    'Profile',
]


class Profile(AppiObject):

    directory = Path(constant.PORTAGE_DIR, 'profiles')

    @classmethod
    def list(cls):
        base_dir = Path(constant.CONF_DIR, 'make.profile')
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

    @classmethod
    def _parse_make_conf_file(cls, path, context=None):
        context = context or {}
        with open(str(path), 'r') as f:
            output_vars = set(re.findall(
                r'^\s*(?:export\s+)?([a-z][a-z0-9_]*)=', f.read(), re.M | re.I
            ))
        return dict(
            context, **extract_bash_file_vars(path, output_vars, context))

    @classmethod
    def get_system_make_conf(cls):
        path = Path(constant.GLOBAL_CONFIG_PATH, 'make.globals')
        context = cls._parse_make_conf_file(path)
        for profile in cls.list():
            path = profile.path / 'make.defaults'
            if path.exists():
                context = Profile._parse_make_conf_file(path, context)
        path = Path(constant.CONF_DIR, 'make.conf')
        return Profile._parse_make_conf_file(path, context)

    def __init__(self, path):
        self.path = Path(path).resolve()

    def __eq__(self, profile):
        return self.path == profile.path

    def __str__(self):
        return str(self.path)
