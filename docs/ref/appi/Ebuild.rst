.. _appi.Ebuild:

===============
``appi.Ebuild``
===============


Ebuild(path)
------------

Create an ebuild object from an absolute path. ``path`` must be a valid ebuild path.
A valid ebuild path starts with the repository location, then a category directory,
a package directory and a package/version file with ``.ebuild`` extension.

Raises
~~~~~~

- :ref:`EbuildError <appi.exception.EbuildError>` if ``path`` is not a valid ebuild path.

Examples
~~~~~~~~

.. code-block:: python

    >>> appi.Ebuild('/usr/portage/x11-wm/qtile/qtile-0.10.6.ebuild')
    <Ebuild 'x11-wm/qtile-0.10.6::gentoo'>
    >>> appi.Ebuild('/home/tony/Workspace/Funtoo/sapher-overlay/x11-wm/qtile/qtile-0.10.6.ebuild')
    <Ebuild 'x11-wm/qtile-0.10.6::sapher'>
    >>> appi.Ebuild('/undefined/x11-wm/qtile/qtile-0.10.6.ebuild')
    <Ebuild 'x11-wm/qtile-0.10.6'>
    >>> appi.Ebuild('/x11-wm/qtile/qtile-0.10.6.ebuild')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/usr/lib/python3.4/site-packages/appi/ebuild.py", line 59, in __init__
        raise EbuildError("{ebuild} is not a valid ebuild path.", path)
    appi.ebuild.EbuildError: /x11-wm/qtile/qtile-0.10.6.ebuild is not a valid ebuild path.
    >>>


Attributes
----------

- **category** (``str``) The package category
- **package** (``str``) The package name
- **version** (``str``) The package version
- **repository** (:ref:`appi.conf.Repository <appi.conf.Repository>`) The package repository
  if available, ``None`` otherwise
- **location** (``pathlib.Path``) The path of the ebuild file
- **useflags** (``set``) The set of useflags supported by this ebuild
- **slot** (``str``) The slot of the package
- **subslot** (``str``) The subslot of the package if any, ``None`` otherwise
- **vars** (``dict``) A dictionnary containing ebuild raw variables such as ``HOMEPAGE``,
  ``LICENSE``, ``DESCRIPTION`` and ``EAPI``
- **db_dir** (``pathlib.Path``) The directory where information about this package installation
  can be found (if it is installed)

Examples
~~~~~~~~

.. code-block:: python

    >>> e = appi.Ebuild('/usr/portage/app-editors/vim-core/vim-core-8.0.0386.ebuild')
    >>> e.category
    'app-editors'
    >>> e.package
    'vim-core'
    >>> e.version
    '8.0.0386'
    >>> e.repository
    <Repository 'gentoo'>
    >>> e.useflags
    {'acl', 'minimal', 'nls'}
    >>> e.slot
    '0'
    >>> e.subslot
    >>> f = appi.Ebuild('/tmp/app-editors/vim-core/vim-core-8.0.0386.ebuild')
    >>> f.repository
    >>> g = appi.Ebuild('/usr/portage/dev-lang/python/python-3.5.3.ebuild')
    >>> g.slot
    '3.5'
    >>> g.subslot
    '3.5m'
    >>> g.vars['LICENSE']
    'PSF-2'
    >>>


String representation
---------------------

The string representation of an ebuild is as following: ``<category>/<name>-<version>``. Also,
if the repository is known, it is appended as ``::<repository>``.

Examples
~~~~~~~~

.. code-block:: python

    >>> str(appi.Ebuild('/usr/portage/dev-python/appi/appi-0.0.ebuild'))
    'dev-python/appi-0.0::gentoo'
    >>> str(appi.Ebuild('/home/tony/Workspace/Funtoo/sapher-overlay/dev-python/appi/appi-1.0.ebuild'))
    'dev-python/appi-1.0::sapher'
    >>> str(appi.Ebuild('/not/a/repository/dev-python/appi/appi-0.1.ebuild')
    'dev-python/appi-0.1'
    >>>

get_version() -> :ref:`appi.Version <appi.Version>`
---------------------------------------------------

``Ebuild.version`` is a string representing the version of the ebuild. ``get_version()`` returns it
as a :ref:`Version <appi.Version>` object.

Examples
~~~~~~~~

.. code-block:: python

    >>> e = appi.Ebuild('/usr/portage/media-libs/libcaca/libcaca-0.99_beta19.ebuild')
    >>> e.version
    '0.99_beta19'
    >>> e.get_version()
    <Version '0.99_beta19'>

matches_atom(atom) -> ``bool``
------------------------------

Return ``True`` if the ebuild matches the given ``atom``.

Examples
~~~~~~~~

.. code-block:: python

    >>> e = appi.Ebuild('/usr/portage/media-gfx/blender/blender-2.72b-r4.ebuild')
    >>> e.matches_atom(appi.QueryAtom('=media-gfx/blender-2.72b-r4'))
    True
    >>> e.matches_atom(appi.QueryAtom('media-gfx/gimp'))
    False
    >>> e.matches_atom(appi.QueryAtom('~media-gfx/blender-2.72b'))
    True
    >>> e.matches_atom(appi.QueryAtom('>media-gfx/blender-2.72'))
    True
    >>> e.matches_atom(appi.QueryAtom('<=media-gfx/blender-2.72'))
    False
    >>> e.matches_atom(appi.QueryAtom('=media-gfx/blender-2*'))
    True
    >>> f = appi.Ebuild('/usr/portage/dev-lang/python/python-3.4.5.ebuild')
    >>> f.matches_atom(appi.QueryAtom('dev-lang/python:3.4/3.4m')
    True
    >>> f.matches_atom(appi.QueryAtom('dev-lang/python:3.4')
    True
    >>> f.matches_atom(appi.QueryAtom('dev-lang/python:3.5')
    False
    >>>

is_installed() -> ``bool``
--------------------------

Return ``True`` if this ebuild is installed. ``False`` otherwise.

is_in_tree() -> ``bool``
--------------------------

Return ``True`` if this ebuild is available in the repository. ``False``
otherwise.
