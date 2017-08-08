.. _appi.DependAtom:

===================
``appi.DependAtom``
===================

A "depend atom" is a antom that is used in the ``DEPEND`` ebuild variable.

Its usage is very close to :ref:`QueryAtom <appi.QueryAtom>` to some extent:

- It **can** be prefixed with ``!`` or ``!!``.
- It **cannot** be restricted to a specific repository (``::repo``).
- It **can** be appended a comma-separated list of useflags between brackets.
