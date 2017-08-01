# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
import platform

__all__ = [
    'CONF_DIR', 'BIN_PATH',
]

python_version = '.'.join(platform.python_version_tuple()[:2])

CONF_DIR = '/etc/portage'
PORTAGE_DIR = '/usr/portage'
BIN_PATH = '/usr/lib/portage/python{}'.format(python_version)
GLOBAL_CONFIG_PATH = '/usr/share/portage/config'
INCREMENTAL_PORTAGE_VARS = [
    'ACCEPT_KEYWORDS', 'CONFIG_PROTECT', 'CONFIG_PROTECT_MASK', 'FEATURES',
    'IUSE_IMPLICIT', 'PRELINK_PATH', 'PRELINK_PATH_MASK',
    'PROFILE_ONLY_VARIABLES', 'USE', 'USE_EXPAND', 'USE_EXPAND_HIDDEN',
    'USE_EXPAND_IMPLICIT', 'USE_EXPAND_UNPREFIXED',
]
