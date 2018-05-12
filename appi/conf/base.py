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
        """Populate `self._instances` if empty.
        Parse conf file and extract sections as `Conf` instances into
        `Conf._instances`.
        """
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
                else:
                    self._instances[name] = self(name, dict(section))
        if default_section:
            self.handle_default_section(default_section)

    def handle_default_section(self, section):
        """Override this method to implement the behavior when the default
        section of the conf file is read.
        """

    def list(self, **kwargs):
        """Return a list of sections of the conf file as `Conf` instances.
        Keyword arguments may be passed to filter fields. For instance,
        Conf.list(foobar='baz'), will only return sections that have a foobar
        field equal to "baz".
        """
        self._fetch_instances()
        confs = self._instances.values()
        if kwargs:
            confs = [c for c in confs if c.matches(**kwargs)]
        return list(confs)

    def find(self, **kwargs):
        """Return the only section which fields match the given keyword
        arguments.
        Return None if no section matched.
        Raise ValueError if more than one section match.
        """
        confs = self.list(**kwargs)
        if len(confs) > 1:
            raise ValueError
        elif not confs:
            return None
        return confs[0]

    def get_conf_files(self, _paths=None):
        """Return a list of paths of files involved in the requested conf.
        `_paths` is only used innerly to recurse over subdirectories, it should
        never be passed elsewhere. Consider this method takes no argument.
        """
        paths = _paths or [self.get_conf_path()]
        expanded_paths = []
        for path in paths:
            if path.is_dir():
                expanded_paths.extend(self.get_conf_files(path.iterdir()))
            else:
                expanded_paths.append(path)
        return expanded_paths

    def get_conf_path(self):
        """Return the full absolute path of the conf file."""
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

    def __init__(self, name, fields):
        self.name = name
        self._fields = fields
        for name, field in self.supported_fields.items():
            field_name = field.name or name
            value = fields.get(field_name, field.default)
            self._fields[name] = field.to_python(value)

    def __getitem__(self, key):
        return self._fields[key]

    def __str__(self):
        return self.name

    def matches(self, **kwargs):
        """Return True if all fields passed as keyword arguments match the
        values of this section fields. False otherwise.
        """
        for k, v in kwargs.items():
            if (k in self.supported_fields and
                    self.supported_fields[k].to_python(v) != self[k]):
                return False
        return True


class Field(AppiObject):
    """A field of a section of a conf file.
    Instances describe the name of the field, its default value and whether it
    is required.
    Field subclasses describe how values of that field should be represented in
    python through the `to_python()` method.
    """

    def __init__(self, name=None, **kwargs):
        self.name = name
        self.default = kwargs.get('default')
        self.required = kwargs.get('required', False)

    def __str__(self):
        return str(self.name)

    def to_python(self, value):
        if value is None and self.required:
            raise ValueError("The field '{}' is required".format(self.name))
        return value


class PathField(Field):
    """A field which python reprsentation is a `pathlib.Path`."""

    def to_python(self, value):
        value = super().to_python(value)
        return Path(value)


class IntegerField(Field):
    """A field which python reprsentation is an `int`."""

    def to_python(self, value):
        value = super().to_python(value)
        return int(value)


class BooleanField(Field):
    """A field which python reprsentation is a `bool`."""

    def __init__(self, name=None, **kwargs):
        self.true = kwargs.pop('true', {True, 'true', 'yes'})
        self.false = kwargs.pop('false', {False, 'false', 'no'})
        super().__init__(name, **kwargs)

    def to_python(self, value):
        value = super().to_python(value)
        if isinstance(value, str):
            value = value.lower()
        if value in self.true:
            return True
        elif value in self.false:
            return False
        raise ValueError((
            "The field '{}' does not recognize '{}' as a valid value."
        ).format(self.name, value))
