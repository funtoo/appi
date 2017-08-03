# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
from configparser import ConfigParser
from pathlib import Path

from ..base import AppiObject
from ..base.constant import CONF_DIR

__all__ = [
    'Conf', 'Field', 'PathField',
]


class ConfMetaclass(type):
    """Metaclass for Conf. See `appi.conf.base.Conf`."""

    def __getitem__(self, key):
        self._fetch_instances()
        return self._instances[key]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def _fetch_instances(self):
        if self._instances:
            return
        default_section = None
        for conf_file in self.get_conf_files():
            config = ConfigParser()
            config.read(str(conf_file))
            for name, section in config.items():
                if name == 'DEFAULT':
                    if section:
                        default_section = section
                    continue
                self._instances[name] = self(name, section)
        if default_section:
            self.handle_default_section(default_section)

    def handle_default_section(self, section):
        """Override this method to implement the behavior when the default
        section of the conf file is read.
        """

    def list(self, **kwargs):
        self._fetch_instances()
        confs = self._instances.values()
        if kwargs:
            confs = [c for c in confs if c.matches(**kwargs)]
        return confs

    def find(self, **kwargs):
        confs = self.list(**kwargs)
        if len(confs) > 1:
            raise ValueError
        elif not confs:
            return None
        return confs[0]

    def get_conf_files(self, paths=None):
        paths = paths or [self.get_conf_path()]
        expanded_paths = []
        for path in paths:
            if path.is_dir():
                expanded_paths.extend(self.get_conf_files(path.iterdir()))
            else:
                expanded_paths.append(path)
        return expanded_paths

    def get_conf_path(self):
        return Path(CONF_DIR, self.conf_file)


class Conf(AppiObject, metaclass=ConfMetaclass):
    """Interface to access data in standard conf files.

    Each subclass represent a specific conf file.
    Each instance represent a section of the conf file.

    Sections can be accessed as if Conf was a dict. For instance, if
    Foobar is a subclass of Conf, Foobar['baz'] is a Foobar instance
    representing the 'baz' section of the conf file described by the Foobar
    class.
    """

    conf_file = None
    """File to parse, relative to /etc/portage/. May be a directory to
    recursively concatenate all files in it.
    """

    supported_fields = {}
    """Dictionary mapping field names to a `Field` instance describing how to
    handle this field. Field names not in this dictionary will be ignored.
    See `appi.conf.base.Field`.
    """

    _instances = {}
    """Store conf file sections."""

    def __init__(self, name, section):
        self.name = name
        for name, field in self.supported_fields.items():
            field_name = field.name or name
            value = section.get(field_name, field.default)
            setattr(self, name, field.to_python(value))

    def __str__(self):
        return self.name

    def matches(self, **kwargs):
        for k, v in kwargs.items():
            if (k in self.supported_fields and
                    self.supported_fields[k].to_python(v) != getattr(self, k)):
                return False
        return True


class Field(AppiObject):

    def __init__(self, name=None, **kwargs):
        self.name = name
        self.default = kwargs.get('default')
        self.required = kwargs.get('required', False)

    def __str__(self):
        return self.name

    def to_python(self, value):
        if value is None and self.required:
            raise ValueError("The field '{}' is required".format(self.name))
        return value


class PathField(Field):

    def to_python(self, value):
        return Path(value)
