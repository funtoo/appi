============
Install appi
============


Installation from portage tree
==============================

First check if ``dev-python/appi`` is already in you portage tree:

.. code-block:: bash

    emerge -av dev-python/appi


Installation from sapher overlay
================================

If your distribution does not provide a ``dev-python/appi`` ebuild,
you can get it from the `sapher overlay`_:

.. code-block:: bash

    mkdir -pv /var/overlays
    git clone https://github.com/apinsard/sapher-overlay.git /var/overlays/sapher
    cat > /etc/portage/repos.conf/sapher <<EOF
    [sapher]
    location = /var/overlays/sapher
    sync-type = git
    sync-uri = git://github.com/apinsard/sapher-overlay.git
    auto-sync = yes
    EOF
    emerge -av dev-python/appi::sapher

.. _sapher overlay: https://github.com/apinsard/sapher-overlay/


Installation from pypi
======================

Not yet available.


Installation from git repository
================================

.. code-block:: bash

    pip install git+ssh://git@github.com/apinsard/appi.git
