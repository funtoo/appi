.. _appi.exception.AtomError:

============================
``appi.exception.AtomError``
============================

:ref:`PortageError <appi.exception.PortageError>` related to an atom.


Error codes
-----------

- ``invalid`` (default) - the atom format is invalid, no further details
- ``missing_category`` - expecting category because strict mode is enabled
- ``missing_selector`` - expecting a version selector because a version was specified
- ``missing_version`` - expecting a version because a version selector was specified
- ``unexpected_revision`` - a revision was given where it was not expected
- ``unexpected_postfix`` - a postfix was appended to the version while the version
  selector is not ``=``
- ``unexpected_slot_operator`` - a slot operator was given where it was not expected
