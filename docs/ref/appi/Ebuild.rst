.. _appi.Version:

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

- ``category`` (``str``) The package category
- ``package`` (``str``) The package name
- ``version`` (``str``) The package version
- ``repository`` (``appi.Repository``) The package repository if available (``None`` otherwise)

Examples
~~~~~~~~

.. code-block:: python

    >>> e = appi.Ebuild('/usr/portage/www-client/brave/brave-0.12.15.ebuild')
    >>> e.category
    'www-client'
    >>> e.package
    'brave'
    >>> e.version
    '0.12.15'
    >>> e.repository
    <Repository 'gentoo'>
    >>> f = appi.Ebuild('/tmp/www-client/brave/brave-0.12.15.ebuild')
    >>> f.repository
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
-------------

``Ebuild.version`` is a string representing the version of the ebuild. ``get_version()`` returns it
as a :ref:`Version <appi.Version>` object.

Examples
~~~~~~~~

.. code-block:: python

    >>> e = Ebuild('/usr/portage/media-libs/libcaca/libcaca-0.99_beta19.ebuild')
    >>> e.version
    '0.99_beta19'
    >>> e.get_version()
    <Version '0.99_beta19'>

matches_atom(atom) -> ``bool``
------------------

Return ``True`` if the ebuild matches the given ``atom``.

.. warning:: This method still lacks SLOT check. It should be implemented in version ``0.1``.

Examples
~~~~~~~~

.. code-block:: python

    >>> e = Ebuild('/usr/portage/media-gfx/blender/blender-2.72b-r4.ebuild')
    >>> e.matches_atom(QueryAtom('=media-gfx/blender-2.72b-r4'))
    True
    >>> e.matches_atom(QueryAtom('media-gfx/gimp'))
    False
    >>> e.matches_atom(QueryAtom('~media-gfx/blender-2.72b'))
    True
    >>> e.matches_atom(QueryAtom('>media-gfx/blender-2.72'))
    True
    >>> e.matches_atom(QueryAtom('<=media-gfx/blender-2.72'))
    False
    >>> e.matches_atom(QueryAtom('=media-gfx/blender-2*'))
    True
    >>>
