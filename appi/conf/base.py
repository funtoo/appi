# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
from configparser import ConfigParser
from pathlib import Path

from ..base.constant import CONF_DIR

__all__ = [
    'Conf', 'Field', 'PathField',
]


class Conf:

    conf_file = None
    supported_attributes = {}

    _instances = {}

    @classmethod
    def _fetch_instances(cls):
        if cls._instances:
            return
        default_section = None
        for conf_file in cls.get_conf_files():
            config = ConfigParser()
            config.read(str(conf_file))
            for name, section in config.items():
                if name == 'DEFAULT':
                    default_section = section
                    continue
                cls._instances[name] = cls(section)
        if default_section:
            cls.handle_default_section(default_section)

    @classmethod
    def handle_default_section(cls, section):
        pass

    @classmethod
    def list(cls):
        cls._fetch_instances()
        return cls._instances

    @classmethod
    def get_conf_files(cls):
        path = cls.get_conf_path()
        if path.is_dir():
            return cls.get_conf_path().iterdir()
        else:
            return [path]

    @classmethod
    def get_conf_path(cls):
        return Path(CONF_DIR, cls.conf_file)

    def __init__(self, section):
        for name, field in self.supported_fields.items():
            field_name = field.name or name
            value = section.get(field_name, field.default)
            setattr(self, name, field.to_python(value))


class Field:

    def __init__(self, name=None, **kwargs):
        self.name = name
        self.default = kwargs.get('default')
        self.required = kwargs.get('required')

    def to_python(self, value):
        if value is None and self.required:
            raise ValueError("The field '{}' is required".format(self.name))
        return value


class PathField(Field):

    def to_python(self, value):
        return Path(value)
