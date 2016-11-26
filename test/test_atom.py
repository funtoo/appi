# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
from unittest import TestCase

from appi.atom import Atom, AtomError
from appi.version import Version


class TestAtomValidityMetaclass(type(TestCase)):

    @staticmethod
    def invalid_test_func_wrapper(atom, strict):
        def test_func(self):
            with self.assertRaises(AtomError):
                Atom(atom, strict)
        return test_func

    @staticmethod
    def valid_test_func_wrapper(atom, strict):
        def test_func(self):
            Atom(atom, strict)
        return test_func

    def __new__(mcs, name, bases, attrs):
        for atom, strict in attrs['invalid_atoms']:
            func_name = 'test_invalid_atom_{}'.format(atom)
            test_func = mcs.invalid_test_func_wrapper(atom, strict)
            test_func.__name__ = func_name
            attrs[func_name] = test_func
        for atom, strict in attrs['valid_atoms']:
            func_name = 'test_valid_atom_{}'.format(atom)
            test_func = mcs.valid_test_func_wrapper(atom, strict)
            test_func.__name__ = func_name
            attrs[func_name] = test_func
        return super().__new__(mcs, name, bases, attrs)


class TestAtomValidity(TestCase, metaclass=TestAtomValidityMetaclass):

    invalid_atoms = [
        ('package', True), ('=dev-lang/python', False), ('~dev-python/ipython', False),
        ('x11-libs/qtile-0.10.6', False), ('toto-3.14*', False), ('<toto-3.14*', False),
    ]
    valid_atoms = [
        ('package', False), ('dev-lang/python', True), ('~dev-python/ipython-5.4.0', True),
        ('=x11-libs/qtile-0.10.6', True), ('=toto-3.14*', False),
    ]


class TestGetVersionMetaclass(type(TestCase)):

    @staticmethod
    def test_func_wrapper(a, v):
        def test_func(self):
            atom = Atom(a)
            if v is None:
                self.assertIsNone(atom.get_version())
            else:
                version = Version(v)
                self.assertEqual(atom.get_version(), version)
        return test_func

    def __new__(mcs, name, bases, attrs):
        for a, v in attrs['atom_to_version']:
            func_name = 'test_get_version_{}'.format(v)
            test_func = mcs.test_func_wrapper(a, v)
            test_func.__name__ = func_name
            attrs[func_name] = test_func
        return super().__new__(mcs, name, bases, attrs)


class TestGetVersion(TestCase, metaclass=TestGetVersionMetaclass):

    atom_to_version = [
        ('=cat/pkg-0.12.3', '0.12.3'),
        ('<=cat/pkg-3.14_pre5-r1', '3.14_pre5-r1'),
        ('>cat/pkg-5', '5'),
        ('>=cat/pkg-a-4.4.00c_p2_pre5-r10', '4.4.00c_p2_pre5-r10'),
        ('<cat/pkg-a-4.4.00c_p2_pre5-r10', '4.4.00c_p2_pre5-r10'),
        ('cat/some-pkg', None),
        ('dev-lang/python:3.4', None),
        ('=dev-lang/python-3*', '3'),
        ('=x11-libs/gtk+-2.4m_beta3*', '2.4m_beta3'),
        ('~media-libs/speex-1.2_rc1', '1.2_rc1'),
        ('=sys-kernel/vanilla-sources-4.8.10:4.8.10', '4.8.10'),
    ]


class TestGetVersionGlobPattern(TestCase):
    pass


class TestGetGlobPattern(TestCase):
    pass


class TestListMatchingEbuilds(TestCase):
    """Need to setup a temporary portage directory for these tests"""


class TestMatchesExistingEbuild(TestCase):
    """Need to setup a temporary portage directory for these tests"""


class TestQueryAtomValidity(TestCase):
    pass


class TestGetRepository(TestCase):
    pass
