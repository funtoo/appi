# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
import platform

__all__ = [
    'ROOT', 'BIN_PATH', 'CONF_DIR', 'GLOBAL_CONFIG_PATH', 'PACKAGE_DB_PATH',
    'INCREMENTAL_PORTAGE_VARS',
]

ROOT = '/'

python_version = '.'.join(platform.python_version_tuple()[:2])
BIN_PATH = ROOT + 'usr/lib/portage/python{}'.format(python_version)
# TODO find a better way to fill this out.
# Cf. GitLab#12

CONF_DIR = ROOT + 'etc/portage'
GLOBAL_CONFIG_PATH = ROOT + 'usr/share/portage/config'
PACKAGE_DB_PATH = ROOT + 'var/db/pkg'

INCREMENTAL_PORTAGE_VARS = [
    'ACCEPT_KEYWORDS', 'CONFIG_PROTECT', 'CONFIG_PROTECT_MASK', 'FEATURES',
    'IUSE_IMPLICIT', 'PRELINK_PATH', 'PRELINK_PATH_MASK',
    'PROFILE_ONLY_VARIABLES', 'USE', 'USE_EXPAND', 'USE_EXPAND_HIDDEN',
    'USE_EXPAND_IMPLICIT', 'USE_EXPAND_UNPREFIXED',
]
