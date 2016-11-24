# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
from unittest import TestCase

from appi.atom import Atom
from appi.ebuild import Ebuild, EbuildError
from appi.version import Version


class TestInvalidEbuildMetaclass(type(TestCase)):

    @staticmethod
    def test_func_wrapper(ebuild):
        def test_func(self):
            with self.assertRaises(EbuildError):
                Ebuild(ebuild)
        return test_func

    def __new__(mcs, name, bases, attrs):
        for ebuild in attrs['invalid_ebuilds']:
            func_name = 'test_invalid_ebuild_{}'.format(ebuild)
            test_func = mcs.test_func_wrapper(ebuild)
            test_func.__name__ = func_name
            attrs[func_name] = test_func
        return super().__new__(mcs, name, bases, attrs)


class TestInvalidEbuild(TestCase, metaclass=TestInvalidEbuildMetaclass):

    invalid_ebuilds = [
        'ebuild', 'path/to/ebuild', '/path/to/ebuild', 'path/to/toto.ebuild',
        '/path/to/path.ebuild', 'cat-name/pkg-name/pkg-name.ebuild',
        '/cat-name/pkg-name/pkg-name.ebuild', 'category/package/pkg-0.1.2.ebuild',
        '/cat/pkg/package-0.1.2-r1.ebuild', 'cat/pkg/pkg-0.1.2', '/cat/pkg/pkg-0.1.2.eb',
        'cat/pkg/0.1.2.ebuild', '/cat-egory/pack-age/0-r1.ebuild', 'cat/pkg/pkg-r1.ebuild',
        'cat/pkg/pkg-0.1.2..ebuild',
    ]


class TestGetVersionMetaclass(type(TestCase)):

    @staticmethod
    def test_func_wrapper(e, v):
        def test_func(self):
            ebuild = Ebuild(e)
            version = Version(v)
            self.assertEqual(ebuild.get_version(), version)
        return test_func

    def __new__(mcs, name, bases, attrs):
        for e, v in attrs['ebuild_to_version']:
            func_name = 'test_get_version_{}'.format(v)
            test_func = mcs.test_func_wrapper(e, v)
            test_func.__name__ = func_name
            attrs[func_name] = test_func
        return super().__new__(mcs, name, bases, attrs)


class TestGetVersion(TestCase, metaclass=TestGetVersionMetaclass):

    ebuild_to_version = [
        ('cat/pkg/pkg-0.12.3.ebuild', '0.12.3'),
        ('cat/pkg/pkg-3.14_pre5-r1.ebuild', '3.14_pre5-r1'),
        ('cat/pkg/pkg-5.ebuild', '5'),
        ('cat/pkg-a/pkg-a-4.4.00c_p2_pre5-r10.ebuild', '4.4.00c_p2_pre5-r10'),
    ]


class TestMatchesAtomMetaclass(type(TestCase)):

    @staticmethod
    def test_func_wrapper(e, a, assert_what):
        def test_func(self):
            ebuild = Ebuild(e)
            atom = Atom(a, strict=False)
            getattr(self, 'assert' + assert_what)(ebuild.matches_atom(atom))
        return test_func

    def __new__(mcs, name, bases, attrs):
        for e, atoms in attrs['matches']:
            for a in atoms:
                func_name = 'test_match_atom_{}_{}'.format(e, a)
                test_func = mcs.test_func_wrapper(e, a, 'True')
                test_func.__name__ = func_name
                attrs[func_name] = test_func
        for e, atoms in attrs['unmatches']:
            for a in atoms:
                func_name = 'test_unmatch_atom_{}_{}'.format(e, a)
                test_func = mcs.test_func_wrapper(e, a, 'False')
                test_func.__name__ = func_name
                attrs[func_name] = test_func
        return super().__new__(mcs, name, bases, attrs)


class TestMatchesAtom(TestCase, metaclass=TestMatchesAtomMetaclass):

    matches = [
        ('cat/pkg/pkg-0.1.0_pre0-r1.ebuild', [
            'cat/pkg', '=cat/pkg-0.1.0_pre0-r1', '~cat/pkg-0.1.0_pre0',
            'pkg', '>=pkg-0.1', '<pkg-0.1.0',
        ]),
        ('dev-lang/python/python-3.5.2.ebuild', [
            'dev-lang/python', '<=dev-lang/python-4', '~dev-lang/python-3.5.2',
            '>python-3.5.0', '=python-3*',
        ]),
    ]
    unmatches = [
        ('cat/pkg/pkg-1.2.3_p3-r5.ebuild', [
            'cat/package', '=category/pkg-1.2.3_p3-r5', '~cat/pkg-0.1.0_pre0',
            'pack', '<=pkg-1.2.3', '>cat/pkg-1.2.3_p3-r5',
        ]),
        ('dev-lang/python/python-2.7.10-r1.ebuild', [
            'dev-python/python', 'dev-lang/haskell', '~dev-lang/python-3.5.2',
            '>=python-3', '=dev-lang/python-3*',
        ]),
    ]
