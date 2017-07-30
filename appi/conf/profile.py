# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
import os
from pathlib import Path
import re
import subprocess

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

    @classmethod
    def _parse_make_conf_file(cls, path, context=None):
        context = (context or {}).copy()
        cmd = ['bash', '-c', 'source {} && set'.format(path)]
        env = dict(os.environ, **context)
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env)

        raw_vars = {}
        with Path(path).open('r') as f:
            interesting_vars = set(re.findall(
                r'^\s*(?:export\s+)?([a-z][a-z0-9_]*)=', f.read(), re.M | re.I
            ))
        for line in proc.stdout:
            key, _, value = line.partition(b'=')
            key = key.decode('ascii')
            if key in interesting_vars:
                raw_vars[key] = value
        proc.communicate()
        context.update(cls._clean_raw_vars(raw_vars))
        return context

    @classmethod
    def _clean_raw_vars(cls, raw_vars):
        """Extract actual values from raw variables values retrieved with bash
        'set' command.
        """
        cleaned_vars = {}
        for k, v in raw_vars.items():
            v = re.sub(rb'\n$', b'', v)
            v = re.sub(rb"^\$?'(.*)'$", rb'\1', v)
            cleaned_vars[k] = v.decode('unicode_escape')
        return cleaned_vars

    def __init__(self, path):
        self.path = Path(path).resolve()

    def __eq__(self, profile):
        return self.path == profile.path

    def __str__(self):
        return str(self.path)
