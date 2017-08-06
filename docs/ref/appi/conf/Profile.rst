.. _appi.conf.Profile:

=====================
``appi.conf.Profile``
=====================

A `portage profile`_.

Currently, this only allows to retrieve the system ``make.conf``. By "system",
it is meant: after parsing ``/usr/share/portage/config/make.globals``, profiles
``make.defaults`` and ``/etc/portage/make.conf``.

Accross future versions, features will be implemented to retrieve all information
contained in profiles, separately or all profiles aggregated.

.. _portage profile: https://wiki.gentoo.org/wiki/Profile_(Portage)


Profile.list() -> ``list``
--------------------------

Return the list of all enabled profiles, sorted in the order they will be parsed
in the chain.

Examples
~~~~~~~~

.. code-block:: python

    >>> Profile.list()
    [<Profile: '/usr/portage/profiles/base'>,
     <Profile: '/var/git/meta-repo/kits/core-kit/profiles/arch/base'>,
     <Profile: '/var/git/meta-repo/kits/core-kit/profiles/funtoo/1.0/linux-gnu'>,
     <Profile: '/var/git/meta-repo/kits/core-kit/profiles/funtoo/1.0/linux-gnu/arch/x86-64bit'>,
     <Profile: '/var/git/meta-repo/kits/core-kit/profiles/funtoo/1.0/linux-gnu/build/current'>,
     <Profile: '/var/git/meta-repo/kits/core-kit/profiles/funtoo/1.0/linux-gnu/arch/x86-64bit/subarch/generic_64'>,
     <Profile: '/var/git/meta-repo/kits/core-kit/profiles/funtoo/1.0/linux-gnu/flavor/minimal'>,
     <Profile: '/var/git/meta-repo/kits/core-kit/profiles/funtoo/1.0/linux-gnu/flavor/core'>,
     <Profile: '/var/git/meta-repo/kits/core-kit/profiles/funtoo/1.0/linux-gnu/mix-ins/console-extras'>,
     <Profile: '/var/git/meta-repo/kits/core-kit/profiles/funtoo/1.0/linux-gnu/mix-ins/X'>,
     <Profile: '/var/git/meta-repo/kits/core-kit/profiles/funtoo/1.0/linux-gnu/mix-ins/no-systemd'>]
    >>>


Profile.get_system_make_conf() -> ``dict``
------------------------------------------

Return a dictionnary of system ``make.conf`` variables.

Examples
~~~~~~~~

.. code-block:: python

    >>> a = Profile.get_system_make_conf()
    >>> a['ARCH']
    'amd64'
    >>> a['KERNEL']
    'linux'
    >>> a['EMERGE_DEFAULT_OPTS']
    '-j --load-average=5 --keep-going --autounmask=n'
    >>> a['PORTAGE_TMPDIR']
    '/var/tmp'
    >>>


Profile(path)
-------------

Create a profile object from an absolute path. ``path`` must be a path to the
directory describing the profile.
