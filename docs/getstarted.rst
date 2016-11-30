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

.. note:: There is also a ``DependAtom`` which represents a dependency atom as found in
          ebuilds. It is not covered in this quick start but it behaves, to some extent,
          the same as ``QueryAtom``.

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

    >>> atom = appi.QueryAtom('=dev-lang/python-3*:3.4::gentoo')
    >>> atom
    <QueryAtom: '=dev-lang/python-3.4*:3.4::gentoo'>
    >>> atom.selector
    '='
    >>> atom.category
    'dev-lang'
    >>> atom.package
    'python'
    >>> atom.version
    '3'
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

And much more!
--------------

Now, would you like to get the list of ebuilds that satisfy this atom? Nothing's easier!

.. code-block:: python

    >>> atom = appi.QueryAtom('=dev-lang/python-3*:3.4::gentoo')
    >>> atom.list_matching_ebuilds()
    {<Ebuild: 'dev-lang/python-3.5.2::gentoo'>, <Ebuild: 'dev-lang/python-3.4.3-r1::gentoo'>, <Ebuild: 'dev-lang/python-3.4.5::gentoo'>}
    >>>

.. warning:: **Yes, this returns python 3.5.2!** This version of ``appi`` is still
             experimental and we haven't implemented slot filtering yet.

             This feature is planned in version ``0.1``. See issue `#2`_ if you would like
             to be informed on progress, or if you want to get involved and help us
             implement it.


.. _#2: https://github.com/apinsard/appi/issues/2


Well, this brings us to ebuilds.


Go on with ebuilds
==================

An ``appi.Ebuild`` instance represents the file describing a given version of a given
package.

Check ebuilds validity
----------------------

Just as with atoms, you can check the validity of an ebuild by instantiating it.

.. code-block:: python

    >>> appi.Ebuild('/usr/portage/sys-devel/clang/clang-9999.ebuild')
    <Ebuild: 'sys-devel/clang-9999::gentoo'>
    >>> appi.Ebuild('/home/tony/Workspace/Funtoo/sapher-overlay/x11-wm/qtile/qtile-0.10.6.ebuild')
    <Ebuild: 'x11-wm/qtile-0.10.6::sapher'>
    >>> appi.Ebuild('/usr/portage/sys-devel/clang/9999.ebuild')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/usr/lib64/python3.4/site-packages/appi/ebuild.py", line 58, in __init__
        raise EbuildError("{ebuild} is not a valid ebuild path.", path)
    appi.ebuild.EbuildError: /usr/portage/sys-devel/clang/9999.ebuild is not a valid ebuild path.
    >>> from appi.exception import EbuildError
    >>> try:
    ...     appi.Ebuild('/usr/portage/sys-devel/clang/clang-9999')
    ... except EbuildError:
    ...     False
    ... else:
    ...     True
    ...
    False
