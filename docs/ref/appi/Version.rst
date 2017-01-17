.. _appi.Version:

================
``appi.Version``
================

The ``Version`` object is the representation of a package version. It enables to compare
versions.

Version(version_string)
-----------------------

Create a version object from a valid version string.

Raises
~~~~~~

- :ref:`VersionError <appi.exception.VersionError>` if ``version_string`` is not a valid
  version number

Examples
~~~~~~~~

.. code-block:: python

    >>> appi.Version('1.3')
    <Version: '1.3'>
    >>> appi.Version('3.14-r1')
    <Version: '3.14-r1'>
    >>> appi.Version('1.2.3a_rc4_pre5_alpha2-r6')
    <Version: '1.2.3a_rc4_pre5_alpha2-r6'>
    >>> appi.Version('2.0beta')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/usr/lib64/python3.5/site-packages/appi/version.py", line 76, in __init__
        "{version} is not a valid version.", version_string)
    appi.version.VersionError: 2.0beta is not a valid version.
    >>> appi.Version('2.0_beta')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/usr/lib64/python3.5/site-packages/appi/version.py", line 76, in __init__
        "{version} is not a valid version.", version_string)
    appi.version.VersionError: 2.0_beta is not a valid version.
    >>> appi.Version('bonjour')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/usr/lib64/python3.5/site-packages/appi/version.py", line 76, in __init__
        "{version} is not a valid version.", version_string)
    appi.version.VersionError: bonjour is not a valid version.
    >>>

Attributes
----------

- **base** (``str``) The base version number (part before the letter if any)
- **letter** (``str``) The letter version number (a single letter), optional
- **suffix** (``str``) The suffix version number (release, pre-release, patch, ...), optional
- **revision** (``str``) The ebuild revision number, optional

Examples
~~~~~~~~

.. code-block:: python

    >>> v = Version('1.2.3d_rc5_p0-r6')
    >>> v.base
    '1.2.3'
    >>> v.letter
    'd'
    >>> v.suffix
    '_rc5_p0'
    >>> v.revision
    '6'
    >>>

compare(other) -> ``int``
-------------------------

startswith(version) -> ``bool``
-------------------------------

get_upstream_version() -> ``Version``
-------------------------------------
