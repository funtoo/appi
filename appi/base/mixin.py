# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2

__all__ = [
    'AppiObject',
]


class AppiObject:

    def __repr__(self):
        return "<{}: '{}'>".format(self.__class__.__name__, str(self))

    def __str__(self):
        # Avoid infinite recursion if the class does not define an __str__
        # method since the default implementation is to call __repr__.
        return "an instance has no name"
