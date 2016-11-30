===========
Get Started
===========


Let's start python3, and write some ``appi`` calls:

.. code-block:: bash

    $ python3
    Python 3.4.5 (default, Nov 29 2016, 00:11:56) 
    [GCC 5.3.0] on linux
    type "help", "copyright", "credits" or "license" for more information.
    >>> import appi
    >>>


Play with atoms
===============

Something you must be familiar with are "query atoms", these are the strings used to query
atoms with ``emerge`` and such tools. ``appi.QueryAtom`` is a class representing this kind
of atoms, it enables you to check if a string is a valid atom or not.

Check atom validity
-------------------

.. code-block:: python

    >>> appi.QueryAtom('dev-python/appi')
    <QueryAtom: 'dev-python/appi'>
    >>> appi.QueryAtom('=sys-apps/portage-2.4.3-r1')
    <QueryAtom: '=sys-apps/portage-2.4.3-r1'>
    >>> appi.QueryAtom('This is not a valid atom')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/usr/lib64/python3.4/site-packages/appi/atom.py", line 62, in __init__
        raise AtomError("{atom} is not a valid atom.", atom_string)
    appi.atom.AtomError: This is not a valid atom is not a valid atom.
    >>> from appi.exception import AtomError
    >>> try:
    ...     appi.QueryAtom('>=dev-lang/python')
    ... except AtomError:
    ...     False
    ... else:
    ...     True
    ...
    False
    >>>

.. note:: ``QueryAtom`` only checks that the atom string is **valid**, not that an ebuild
          actually exists for this atom.

.. code-block:: python

    >>> appi.QueryAtom('this-package/does-not-exist')
    <QueryAtom: 'this-package/does-not-exist'>
    >>> appi.QueryAtom('~foo/bar-4.2.1')
    <QueryAtom: '~foo/bar-4.2.1'>
    >>>

.. note:: If you try to parse atoms without category name, you will notice that it raises
          an ``AtomError`` while it is actually a valid atom. There is a ``strict`` mode
          enabled by defaut, which makes package category mandatory in order to avoid
          dealing with ambiguous packages. You can easily disable this behavior by setting
          ``strict=False``.o

.. code-block:: python

    >>> appi.QueryAtom('=portage-2.4.3-r1')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/usr/lib64/python3.4/site-packages/appi/atom.py", line 71, in __init__
        atom_string, code='missing_category')
    appi.atom.AtomError: =portage-2.4.3-r1 may be ambiguous, please specify the category.
    >>> appi.QueryAtom('=portage-2.4.3-r1', strict=False)
    <QueryAtom: '=portage-2.4.3-r1'>
    >>>

Inspect atom parts
------------------

``QueryAtom`` does not only check atoms validity, it also extracts its components.

.. code-block:: python

    >>> atom = appi.QueryAtom('=dev-lang/python-3.4*:3.4::gentoo')
    >>> atom
    <QueryAtom: '=dev-lang/python-3.4*:3.4::gentoo'>
    >>> atom.selector
    '='
    >>> atom.category
    'dev-lang'
    >>> atom.package
    'python'
    >>> atom.version
    '3.4'
    >>> atom.postfix
    '*'
    >>> atom.slot
    '3.4'
    >>> atom.repository
    'gentoo'
    >>> atom2 = appi.QueryAtom('foo-bar/baz')
    >>> atom2.selector
    >>> atom2.version
    >>> atom2.category
    'foo-bar'
    >>>
