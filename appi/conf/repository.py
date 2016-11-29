# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
from .base import Conf, PathField

__all__ = [
    'Repository',
]


class Repository(Conf):

    conf_file = 'repos.conf'
    supported_fields = {
        'location': PathField(required=True),
    }

    _main_repository = None

    @classmethod
    def handle_default_section(cls, section):
        if 'main-repo' in section:
            cls._main_repository = cls._instances[section['main-repo']]

    @classmethod
    def get_main_repository(cls):
        cls._fetch_instances()
        return cls._main_repository

    @classmethod
    def list_locations(cls):
        return (repo.location for repo in cls.list())
