====
appi
====

Another Portage Python Interface

|rtd0.2| |ci| |coverage|

Why not `portage`?
------------------

Mainly, I was having hard time understanding the python ``portage`` module. I found the code
somewhat obscure and lacking documentation. So I decided to start an alternative, bringing my
approach of how I would like the API to be.

So was born ``appi``. It is still at an early stage, but I hope someday it will have enough
features to enable portage-based distributions newcomers to use it and improve it.


Examples
--------

Atom
~~~~

.. code-block:: python

    >>> from appi import QueryAtom
    >>> a = QueryAtom('portage')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/tony/Workspace/Funtoo/appi/appi/atom.py", line 76, in __init__
        atom_string, code='missing_category')
    appi.atom.AtomError: portage may be ambiguous, please specify the category.
    >>> a = QueryAtom('portage', strict=False)
    >>> a.list_matching_ebuilds()
    {<Ebuild: 'sys-apps/portage-2.4.1-r1::gentoo'>, <Ebuild: 'sys-apps/portage-2.4.3-r1::gentoo'>}
    >>> a
    <QueryAtom: 'portage'>
    >>> b = QueryAtom('>=sys-apps/portage-2.4.2')
    >>> b
    <QueryAtom: '>=sys-apps/portage-2.4.2'>
    >>> b.list_matching_ebuilds()
    {<Ebuild: 'sys-apps/portage-2.4.3-r1::gentoo'>}
    >>> # Considering a second repository named "sapher" containing qtile ebuilds
    ...
    >>> QueryAtom('=x11-wm/qtile-9999').list_matching_ebuilds()
    {<Ebuild: 'x11-wm/qtile-9999::gentoo'>, <Ebuild: 'x11-wm/qtile-9999::sapher'>}


Versioning Policy
-----------------

We use the following version format: ``M.m.p``

- **M** is the major version
- **m** is the minor version
- **p** is the patch version

We may also package pre-releases (postfixed with ``_preN``, where **N** is the pre-release version)
and release candidates (postfixed with ``_rcN``, where **N** is the release candidate version).

**Starting from version 1.0.0,** a major version bump means:

- Global refactoring of the code base
- Removal of features deprecated in the previous releases

A minor version bump means:

- New features
- Existing features improvement
- Features deprecation (raising warnings) which will be removed in the next major version

A patch version bump means:

- Bug fixes
- Security fixes

Thus, backward compatibility is maintained across minor versions, but broken at each
major version bump. However:

- Major version bumps should be very rare
- If you pay attention to the few deprecation warnings that may appear across minor version bumps,
  and fix them along the way, upgrading to a new major version will require no work at all.
- Support and patches **will** still be provided for the last two minor versions before
  the curent version.
- Starting from version 2.0.0, the main module will be named ``appiM`` where **M** is the major
  version number (eg. ``appi2``, ``appi3``, ...). This will allow old software not using the
  latest major version to stay available along with newer software using the latest major version.

**Before version 1.0.0,** any minor version bump may break backward compatibility.


Contributing
------------

See `Contributing`_ page.

.. _`Contributing`: https://gitlab.com/apinsard/appi/blob/0.2/CONTRIBUTING.rst

.. |rtd0.2| image:: https://readthedocs.org/projects/appi/badge/?version=0.2
    :alt: Documentation Status
    :target: http://appi.readthedocs.io/en/0.2/?badge=0.2

.. |ci| image:: https://gitlab.com/apinsard/appi/badges/0.2/pipeline.svg
    :alt: Pipeline Status
    :target: https://gitlab.com/apinsard/appi/commits/0.2

.. |coverage| image:: https://gitlab.com/apinsard/appi/badges/0.2/coverage.svg
    :alt: Coverage Report
    :target: https://gitlab.com/apinsard/appi/commits/0.2
