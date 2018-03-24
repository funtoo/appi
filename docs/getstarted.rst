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
          ``strict=False``.

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
    {<Ebuild: 'dev-lang/python-3.4.3-r1::gentoo'>, <Ebuild: 'dev-lang/python-3.4.5::gentoo'>}
    >>>


Well, this brings us to ebuilds.


Go on with ebuilds
==================

An ``appi.Ebuild`` instance represents the file describing a given version of a given
package.

Check ebuild validity
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
    >>> appi.Ebuild('/Unexisting/overlay/path/foo/bar/bar-1.5a_pre5-r12.ebuild')
    <Ebuild: 'foo/bar-1.5a_pre5-r12'>
    >>>


Inspect ebuild parts
--------------------

.. code-block:: python

    >>> e = appi.Ebuild('/usr/portage/sci-libs/gdal/gdal-2.0.2-r2.ebuild')
    >>> e.category
    'sci-libs'
    >>> e.package
    'gdal'
    >>> e.version
    '2.0.2-r2'
    >>> e.repository
    <Repository: 'gentoo'>
    >>> e.repository['location']
    PosixPath('/usr/portage')
    >>>

And much more
-------------

You can check if an ebuild matches a given atom:

.. code-block:: python

    >>> e = appi.Ebuild('/usr/portage/app-portage/gentoolkit/gentoolkit-0.3.2-r1.ebuild')
    >>> e.matches_atom(appi.QueryAtom('~app-portage/gentoolkit-0.3.2'))
    True
    >>> e.matches_atom(appi.QueryAtom('>gentoolkit-0.3.2', strict=False))
    True
    >>> e.matches_atom(appi.QueryAtom('>=app-portage/gentoolkit-1.2.3'))
    False
    >>> e.matches_atom(appi.QueryAtom('=app-portage/chuse-0.3.2-r1'))
    False
    >>>


Finally, let's checkout versions
================================

Atom and ebuild objects both define a ``get_version()`` method that returns the version
number as a ``Version`` object.

.. code-block:: python

    >>> atom = appi.QueryAtom('=x11-wm/qtile-0.10*')
    >>> atom.version
    '0.10'
    >>> atom.get_version()
    <Version: '0.10'>
    >>> [(eb, eb.get_version()) for eb in atom.list_matching_ebuilds()]
    [(<Ebuild: 'x11-wm/qtile-0.10.5::gentoo'>, <Version: '0.10.5'>), (<Ebuild: 'x11-wm/qtile-0.10.6::gentoo'>, <Version: '0.10.6'>)]
    >>>

Inspect version parts
---------------------

.. code-block:: python

    >>> v = Version('3.14a_beta05_p4_alpha11-r16')
    >>> v.base
    '3.14'
    >>> v.letter
    'a'
    >>> v.suffix
    '_beta05_p4_alpha11'
    >>> v.revision
    '16'
    >>>

Compare versions
----------------

.. code-block:: python

    >>> v1 = Version('2.76_alpha1_beta2_pre3_rc4_p5')
    >>> v2 = Version('1999.05.05')
    >>> v3 = Version('2-r5')
    >>> v1 == v2
    False
    >>> v1 > v3
    True
    >>> v1 < v2
    True
    >>> v3.startswith(v1)
    False
    >>> Version('0.0a-r1').startswith(Version('0.0'))
    True
    >>>
