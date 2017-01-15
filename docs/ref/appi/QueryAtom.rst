.. _appi.QueryAtom:

==================
``appi.QueryAtom``
==================

A "query atom" is an atom that is used for querying a package, this is the kind
of atoms accepted by ``emerge`` for instance.

There also exist :ref:`DependAtom <appi.DependAtom>` that have a slightly different
format and is used by ``DEPEND`` variables in ebuilds.


QueryAtom(atom_string, strict=True)
-----------------------------------

Create a query atom from its string representation. ``atom_string`` must be a valid
string representation of a query atom. The ``strict`` argument controls the
"strict mode" state. When strict mode is enabled, the package category is mandatory
and an error will be raised if it is missing. When strict mode is disabled, the
package category is optional, which makes, for instance, ``=firefox-50-r1`` a valid
atom.

Raises
~~~~~~

- :ref:`AtomError <appi.exception.AtomError>` if ``atom_string`` is not a valid atom
  taking ``strict`` mode into consideration. Possible error codes:

  - **missing_category** The package category is missing, this can be ignored
    by setting ``strict=False``.
  - **missing_selector** The package version was specified but the version
    selector is missing.
  - **missing_version** The version selector was specified but the package
    version is missing.
  - **unexpected_revision** The version contains a revision number while the
    version selector is ``~``.
  - **unexpected_postfix** The ``*`` postfix is specified but the version
    selector is not ``=``.

Examples
~~~~~~~~

.. code-block:: python

    >>> appi.QueryAtom('>=www-client/firefox-51')
    <QueryAtom: '>=www-client/firefox-51'>
    >>> appi.QueryAtom('=www-client/chromium-57*')
    <QueryAtom: '=www-client/chromium-57*'>
    >>> appi.QueryAtom('www-client/lynx')
    <QueryAtom: 'www-client/lynx'>
    >>> appi.QueryAtom('=www-client/links')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/usr/lib64/python3.5/site-packages/appi/atom.py", line 79, in __init__
        code='missing_version')
    appi.atom.AtomError: =www-client/links misses a version number.
    >>> appi.QueryAtom('google-chrome')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/usr/lib64/python3.5/site-packages/appi/atom.py", line 71, in __init__
        atom_string, code='missing_category')
    appi.atom.AtomError: google-chrome may be ambiguous, please specify the category.
    >>> appi.QueryAtom('google-chrome', strict=False)
    <QueryAtom: 'google-chrome'>


Attributes
----------

- **selector** (``str``) The package selector (``>=``, ``<=``, ``<``, ``=``, ``>`` or ``~``)
- **category** (``str``) The package category
- **package** (``str``) The package name
- **version** (``str``) The package version
- **postfix** (``str``) The package postfix (``*`` is the only possible value)
- **slot** (``str``) The package slot
- **repository** (``str``) The name of the repository

All these attribute, excepted **package**, are optional and may be ``None``.

Examples
~~~~~~~~

.. code-block:: python

    >>> a = appi.QueryAtom('=dev-db/mysql-5.6*:5.6::gentoo')
    >>> a.selector
    '='
    >>> a.category
    'dev-db'
    >>> a.package
    'mysql'
    >>> a.version
    '5.6'
    >>> a.postfix
    '*'
    >>> a.slot
    '5.6'
    >>> a.repository
    'gentoo'
    >>> b = appi.QueryAtom('~postgresql-9.4', strict=False)
    >>> b.selector
    '~'
    >>> b.category
    >>> b.package
    'postgresql'
    >>> b.version
    '9.4'
    >>> b.postfix
    >>> b.slot
    >>> b.repository
    >>>


String Representation
---------------------

The string representation of an atom is the raw atom string itself:
``<selector><category>/<package>-<version><postfix>:<slot>::<repository>``

Examples
~~~~~~~~

.. code-block:: python

    >> str(appi.QueryAtom('dev-db/postgresql'))
    'dev-db/postgresql'
    >>> str(appi.QueryAtom('<dev-db/postgresql-9.6'))
    '<dev-db/postgresql-9.6'
    >>> str(appi.QueryAtom('>=dev-db/postgresql-8.4-r1::gentoo'))
    '>=dev-db/postgresql-8.4-r1::gentoo'
    >>> str(appi.QueryAtom('dev-db/postgresql:9.4'))
    'dev-db/postgresql:9.4'
    >>> a = appi.QueryAtom('=postgresql-9.4-r1', strict=False)
    >>> str(a)
    '=postgresql-9.4-r1'
    >>> a.category = 'dev-db'
    >>> str(a)
    '=dev-db/postgresql-9.4-r1'

.. warning:: This can be useful to change the package category of an existing instance as above
             if you want to read atoms without requiring category and infer it afterwards if it
             is not a ambiguous. **However,** it is not recommended to change other attributes
             values. Validity won't be checked and this can lead to incoherent atoms as
             illustrated below. We don't prevent attributes from being altered, we assume you
             are a sane minded developer who knows what he is doing.

.. code-block:: python

    >>> # /!\ DONT DO THIS /!\
    >>> a.selector = ''
    >>> str(a)
    'dev-db/postgresql-9.4-r1'
    >>> # Why would you anyway?
    >>>


get_version() -> :ref:`appi.Version <appi.Version>`
---------------------------------------------------

``QueryAtom.version`` is a string representing the version of the ebuild.
``get_version()`` returns it as a :ref:`Version <appi.Version>` object.

Examples
~~~~~~~~

.. code-block:: python

    >>> a = appi.QueryAtom('>=media-gfx/image-magick-7.0:0/7.0.4.3')
    >>> a.version
    '7.0'
    >>> a.get_version()
    <Version '7.0'>

get_globpattern() -> ``str``
----------------------------

get_repository() -> :ref:`appi.conf.Repository <appi.conf.Repository>`
----------------------------------------------------------------------

list_matching_ebuilds() -> {:ref:`appi.Ebuild <appi.Ebuild>`, ...}
-----------------------------------------------------------------

matches_existing_ebuild() -> ``bool``
-------------------------------------
