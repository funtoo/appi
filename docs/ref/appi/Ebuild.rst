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


String representation
---------------------

get_version()
-------------

matches_atom(atom)
------------------
