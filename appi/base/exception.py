# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
__all__ = [
    'AppiError', 'PortageError',
]


class AppiError(Exception):

    default_code = 'unknown'

    def __init__(self, *args, **kwargs):
        try:
            self.message = args[0]
        except IndexError:
            self.message = self.__class__.__name__
        self.code = kwargs.pop('code', self.default_code)
        self.message_context = kwargs

    def __str__(self):
        return self.message.format(**self.message_context)


class PortageError(AppiError):
    pass
