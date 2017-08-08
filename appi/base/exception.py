# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
__all__ = [
    'AppiError', 'PortageError',
]


class AppiError(Exception):
    """Appi base error.

    All errors thrown by appi will inherit this class.

    AppiError will never be raise itself, its only goal is to serve as a
    catch-all exception for appi errors.
    """

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
    """AppiError related to portage.

    This is a catch-all exception for portage-related appi errors. It will
    never be raised itself.
    """
