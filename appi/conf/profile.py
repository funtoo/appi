# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
from pathlib import Path
import re

from ..base import AppiObject, constant
from ..util import extract_bash_file_vars
from .repository import Repository

__all__ = [
    'Profile',
]


class Profile(AppiObject):
    """A portage profile.

    Currently, this only allows to retrieve the system make.conf. By "system",
    it is meant: after parsing make.globals, profiles make.defaults and
    /etc/portage/make.conf.

    Across future versions, features will be implemented to retrieve all
    information contained in profile, separately or all profiles aggregated.
    """

    @classmethod
    def list(cls):
        """Return the list of all enabled profiles.
        Sorted in the order they will be parsed in the chain.
        """
        base_dir = Path(constant.CONF_DIR, 'make.profile')
        return cls._get_parent_profiles(base_dir)

    @classmethod
    def _get_parent_profiles(cls, base_dir):
        """Return the list of parent profiles given a profile path."""
        profiles_parent = base_dir / 'parent'
        profiles = []
        if not profiles_parent.exists():
            return profiles

        with profiles_parent.open('r', encoding='utf-8') as f:
            for path in f.readlines():
                path = re.sub(r'#.*$', '', path)
                path = path.strip()
                if not path:
                    continue
                if ':' in path:
                    repo_name, path = path.split(':', 1)
                    if not repo_name:
                        repo = Repository.get_main_repository()
                    else:
                        repo = Repository.get(repo_name)
                    path = repo['location'] / 'profiles' / path
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
    def _sanitize_incremental_var(cls, new_value, old_value):
        """Return alphabetically sorted useflags.
        Negated useflags from `new_value` are removed from old_value.
        Other useflags from `new_value` are appended to old_value.
        `new_value` and `old_value` may be either iterables or strings.
        """
        if isinstance(old_value, str):
            old_value = old_value.split()
        if isinstance(new_value, str):
            new_value = new_value.split()
        flags = set(old_value)
        to_remove = set(x[1:] for x in new_value if x[0] == '-')
        to_append = set(x for x in new_value if x[0] != '-')
        return ' '.join(sorted(flags.difference(to_remove).union(to_append)))

    @classmethod
    def _expand_to_use(cls, context):
        """Return the new list of useflags after expansion of variables in
        USE_EXPAND.
        """
        use = set(context.get('USE', '').split())
        use_expand = set(context.get('USE_EXPAND', '').split())
        unprefixed = context.get('USE_EXPAND_UNPREFIXED', '').split()
        for prefix in use_expand:
            value = set(context.get(prefix, '').split())
            if not value:
                continue
            if prefix not in unprefixed:
                value = set('{}_{}'.format(prefix.lower(), v) for v in value)
            use = value.union({
                u for u in use
                if not u.startswith('{}_'.format(prefix).lower())
            })
        return ' '.join(sorted(use))

    @classmethod
    def _parse_make_conf_file(cls, path, context=None):
        """Read a make.conf-like file and return an updated context."""
        context = context or {}
        incrementals = {
            k: v for k, v in context.items()
            if k in constant.INCREMENTAL_PORTAGE_VARS
        }
        with open(str(path), 'r', encoding='utf-8') as f:
            output_vars = set(re.findall(
                r'^\s*(?:export\s+)?([a-z][a-z0-9_]*)=', f.read(), re.M | re.I
            ))
        context = dict(
            context, **extract_bash_file_vars(path, output_vars, context))
        for incremental in constant.INCREMENTAL_PORTAGE_VARS:
            context[incremental] = cls._sanitize_incremental_var(
                context.get(incremental, ''), incrementals.get(incremental, '')
            )
        context['USE'] = cls._expand_to_use(context)
        return context

    @classmethod
    def get_system_make_conf(cls):
        """Return a dict of system make.conf variables."""
        path = Path(constant.GLOBAL_CONFIG_PATH, 'make.globals')
        context = cls._parse_make_conf_file(path)
        for profile in cls.list():
            path = profile.path / 'make.defaults'
            if path.exists():
                context = Profile._parse_make_conf_file(path, context)
        path = Path(constant.CONF_DIR, 'make.conf')
        profile_only_vars = context.get('PROFILE_ONLY_VARIABLES', '').split()
        backup_vars = {k: context.get(k, '') for k in profile_only_vars}
        context = Profile._parse_make_conf_file(path, context)
        context.update(backup_vars)
        return context

    def __init__(self, path):
        """Create a Profile object from a profile path."""
        self.path = Path(path).resolve()

    def __eq__(self, profile):
        return self.path == profile.path

    def __str__(self):
        return str(self.path)
