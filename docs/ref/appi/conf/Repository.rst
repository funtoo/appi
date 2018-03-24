.. _appi.conf.Repository:

========================
``appi.conf.Repository``
========================

An `ebuild repository`_.

.. _ebuild repository: https://wiki.gentoo.org/wiki/Ebuild_repository


Repository.get_main_repository() -> ``Repository``
--------------------------------------------------

Return the main repository.


Repository.list(**kwargs) -> ``list``
-------------------------------------

Return the list of repositories. Keyword arguments may be passed to filter
repositories according to repository properties. Currently, accepted properties
are ``location``, ``priority`` and ``auto-sync``.

Examples
~~~~~~~~

.. code-block:: python

    >>> Repository.list(location='/var/git/meta-repo/kits/python-kit')
    [<Repository: 'python-kit'>]
    >>> Repository.list()
    [<Repository: 'net-kit'>, <Repository: 'nokit'>, <Repository: 'core-hw-kit'>,
     <Repository: 'editors-kit'>, <Repository: 'games-kit'>, <Repository: 'python-kit'>,
     <Repository: 'gnome-kit'>, <Repository: 'java-kit'>, <Repository: 'media-kit'>,
     <Repository: 'perl-kit'>, <Repository: 'xorg-kit'>, <Repository: 'kde-kit'>,
     <Repository: 'core-kit'>, <Repository: 'security-kit'>, <Repository: 'php-kit'>,
     <Repository: 'dev-kit'>, <Repository: 'desktop-kit'>, <Repository: 'science-kit'>,
     <Repository: 'text-kit'>]
    >>> Repository.list(location='/var/git/meta-repo/kits/python-kit')
    [<Repository: 'python-kit'>] 
    >>>


Repository.find(**kwargs) -> ``Repository``
-------------------------------------------

Return the only repository that matches the passed keyword arguments. If no repository
matches, return ``None``. If more than one repository match, raises ``ValueError``.

See also ``Repository.list(**kwargs)``.

Raises
~~~~~~

- ``ValueError`` if more than one repository match

Examples
~~~~~~~~

.. code-block:: python

    >>> Repository.find(location='/var/git/meta-repo/kits/python-kit')
    [<Repository: 'python-kit'>]
    >>> Repository.find()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/usr/lib/python3.4/site-packages/appi/conf/base.py", line 72, in find
        raise ValueError
    ValueError
    >>> 


Repository.list_locations() -> ``generator``
--------------------------------------------

Return all repository locations.
