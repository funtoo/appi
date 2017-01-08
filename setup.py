# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='appi',
    version='0.0.0',
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
