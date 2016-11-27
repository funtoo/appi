# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
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

    def get_regex(self):
        if self.regex:
            return self.regex
        if self.choices:
            return '|'.join(map(re.escape, self.choices))
        return None


class Meta:

    def __init__(self, **kwargs):
        self.attributes = kwargs.get('attributes', [])


class AppiObjectMetaclass(type):
    # TODO This would deservere some clarification and comments

    def __new__(mcs, name, bases, attrs):
        parents = [b for b in bases if isinstance(b, AppiObjectMetaclass)]
        if not parents:
            return super().__new__(mcs, name, bases, attrs)

        new_class = super().__new__(mcs, name, bases, attrs)
        meta = attrs.pop('Meta', None) or getattr(new_class, 'Meta', None)

        exclude = getattr(meta, 'exclude', [])
        attributes = reduce(operator.add, [
            p._meta.attributes for p in parents if hasattr(p, '_meta')], [])

        for attr, value in attrs.items():
            if isinstance(value, Attribute) and attr not in exclude:
                value.name = attr
                attributes.append(value)

        new_class._meta = Meta(
            attributes=[a for a in attributes if a.name not in exclude],
        )

        return new_class


class AppiObject(metaclass=AppiObjectMetaclass):

    def __repr__(self):
        return "<{}: '{}'>".format(self.__class__.__name__, str(self))

    def __str__(self):
        # Avoid infinite recursion if the class does not define an __str__
        # method since the default implementation is to call __repr__.
        return "an instance has no name"
