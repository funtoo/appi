# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
from .atom import DependAtom, QueryAtom
from .ebuild import Ebuild
from .version import Version

__all__ = [
    'DependAtom', 'Ebuild', 'QueryAtom', 'Version',
]

__author__ = "Antoine Pinsard"
__copyright__ = "Copyright (C) 2018 Antoine Pinsard"
__credits__ = ["Antoine Pinsard"]
__license__ = "GPL-2"
__version__ = "0.2.0"
__maintainer__ = "Antoine Pinsard"
__email__ = "antoine.pinsard@gmail.com"
__status__ = "Development"
