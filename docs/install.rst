============
Install appi
============


Installation from portage tree
==============================

First check if ``dev-python/appi`` is already in your portage tree:

.. code-block:: bash

    emerge -av dev-python/appi


Installation from flora overlay
================================

If your distribution does not provide a ``dev-python/appi`` ebuild,
you can get it from the `flora overlay`_:

.. code-block:: bash

    mkdir -pv /var/overlays
    git clone https://github.com/funtoo/flora.git /var/overlays/flora
    cat > /etc/portage/repos.conf/flora <<EOF
    [flora]
    location = /var/overlays/flora
    sync-type = git
    sync-uri = git://github.com/funtoo/flora.git
    auto-sync = yes
    EOF
    emerge -av dev-python/appi::flora

.. _flora overlay: https://github.com/funtoo/flora/


Installation from pypi
======================

Not yet available.


Installation from git repository
================================

.. code-block:: bash

    pip install git+ssh://git@gitlab.com/apinsard/appi.git
