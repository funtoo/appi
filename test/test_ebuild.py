# -*- coding: utf-8 -*-
import unittest

from appi.ebuild import Ebuild, EbuildError
from appi.version import Version


class TestInvalidEbuildMetaclass(type(unittest.TestCase)):

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


class TestInvalidEbuild(unittest.TestCase, metaclass=TestInvalidEbuildMetaclass):

    invalid_ebuilds = [
        'ebuild', 'path/to/ebuild', '/path/to/ebuild', 'path/to/toto.ebuild',
        '/path/to/path.ebuild', 'cat-name/pkg-name/pkg-name.ebuild',
        '/cat-name/pkg-name/pkg-name.ebuild', 'category/package/pkg-0.1.2.ebuild',
        '/cat/pkg/package-0.1.2-r1.ebuild', 'cat/pkg/pkg-0.1.2', '/cat/pkg/pkg-0.1.2.eb',
        'cat/pkg/0.1.2.ebuild', '/cat-egory/pack-age/0-r1.ebuild', 'cat/pkg/pkg-r1.ebuild',
        'cat/pkg/pkg-0.1.2..ebuild',
    ]


class TestGetVersionMetaclass(type(unittest.TestCase)):

    @staticmethod
    def test_func_wrapper(e, v):
        def test_func(self):
            ebuild = Ebuild(e)
            version = Version(v)
            self.assertEqual(ebuild.get_version(), version)
        return test_func

    def __new__(mcs, name, bases, attrs):
        for e, v in attrs['ebuild_to_version'].items():
            func_name = 'test_get_version_{}'.format(v)
            test_func = mcs.test_func_wrapper(e, v)
            test_func.__name__ = func_name
            attrs[func_name] = test_func
        return super().__new__(mcs, name, bases, attrs)


class TestGetVersion(unittest.TestCase, metaclass=TestGetVersionMetaclass):

    ebuild_to_version = {
        'cat/pkg/pkg-0.12.3.ebuild': '0.12.3',
        'cat/pkg/pkg-3.14_pre5-r1.ebuild': '3.14_pre5-r1',
        'cat/pkg/pkg-5.ebuild': '5',
        'cat/pkg-a/pkg-a-4.4.00c_p2_pre5-r10.ebuild': '4.4.00c_p2_pre5-r10',
    }
