# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
from collections import OrderedDict
from functools import reduce
import operator
import re

__all__ = [
    'AppiObject', 'Attribute',
]


class Attribute:

    def __init__(self, **kwargs):
        self.name = None
        self.description = kwargs.get('description')
        self.examples = kwargs.get('examples')
        self.required = kwargs.get('required', False)
        self.regex = kwargs.get('regex')
        self.choices = kwargs.get('choices')
        self.type = kwargs.get('type')

    def get_regex(self):
        if self.regex:
            return self.regex
        if self.choices:
            return '|'.join(map(re.escape, self.choices))
        return None

    def to_python(self, value):
        if self.type and value is not None:
            return self.type(value)
        else:
            return value


class Meta:

    def __init__(self, **kwargs):
        self.attributes = kwargs.get('attributes', OrderedDict())


class AppiObjectMetaclass(type):
    # TODO This would deserve some clarification and comments

    def __new__(mcs, name, bases, attrs):
        parents = [b for b in bases if isinstance(b, AppiObjectMetaclass)]
        if not parents:
            return super().__new__(mcs, name, bases, attrs)

        new_cls = super().__new__(mcs, name, bases, attrs)

        attributes = reduce(operator.add, [
            p._meta.attributes for p in parents if hasattr(p, '_meta')], [])

        for attr, value in attrs.items():
            if isinstance(value, Attribute):
                value.name = attr
                attributes[attr] = value

        new_cls._meta = Meta(attributes=attributes)

        return new_cls


class AppiObject(metaclass=AppiObjectMetaclass):

    def __repr__(self):
        return "<{}: '{}'>".format(self.__class__.__name__, str(self))

    def __str__(self):
        # Avoid infinite recursion if the class does not define an __str__
        # method since the default implementation is to call __repr__.
        return "an instance has no name"

    def __init__(self, **kwargs):
        for k, v in kwargs.item():
            if 
