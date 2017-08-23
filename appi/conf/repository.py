# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
from .base import Conf, PathField, IntegerField, BooleanField

__all__ = [
    'Repository',
]


class Repository(Conf):
    """An ebuild repository."""

    conf_file = 'repos.conf'
    supported_fields = {
        'location': PathField(required=True),
        'priority': IntegerField(default=0),
        'auto-sync': BooleanField(default=True),
    }

    _main_repository = None

    @classmethod
    def handle_default_section(cls, section):
        if 'main-repo' in section:
            cls._main_repository = cls._instances[section['main-repo']]

    @classmethod
    def get_main_repository(cls):
        """Return the main repository."""
        cls._fetch_instances()
        return cls._main_repository

    @classmethod
    def list_locations(cls):
        """Return all repository locations as a generator."""
        return (repo['location'] for repo in cls.list())
