# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
from pathlib import Path
import re
from setuptools import setup, find_packages

BASE_DIR = Path(__file__).parent

with (BASE_DIR / 'README.rst').open(encoding='utf-8') as readme:
    README = readme.read()

with (BASE_DIR / 'appi' / '__init__.py').open(encoding='utf-8') as init_file:
    pattern = '''^\s*__version__\s*=\s*["']([0-9.]+)["']\s*$'''
    VERSION = re.search(pattern, init_file.read(), re.M).group(1)

setup(
    name='appi',
    version=VERSION,
    packages=find_packages(exclude=['test']),
    include_package_data=True,
    license='GPL-2',
    description="Another Portage Python Interface",
    long_description=README,
    url='https://gihtub.com/apinsard/appi',
    author="Antoine Pinsard",
    author_email='antoine.pinsard@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: POSIX :: Linux'
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration',
    ],
)
