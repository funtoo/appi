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
