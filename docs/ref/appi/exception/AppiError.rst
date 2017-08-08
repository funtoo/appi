.. _appi.exception.AppiError:

============================
``appi.exception.AppiError``
============================

Appi base error. All errors thrown by appi will inherit this class.

``AppiError`` will never be raised itself, its only goal is to serve as a
catch-all exception for appi errors.

Any exception inheriting ``AppiError`` will have a ``code`` attribute giving
more programmatically readable information about the error that occurred.
See specific exceptions documentation to get a comprehensive list of applicable
error codes.

Had errors have to be propagated to the user, error messages must be rendered
by casting the exception to string.
