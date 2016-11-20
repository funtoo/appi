# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
from functools import wraps

__all__ = 'cached'


def cached(method):
    attr_name = '_cached_{}'.format(method.__name__)

    @wraps(method)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)
    return wrapper
