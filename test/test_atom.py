# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
from unittest import TestCase

from appi.atom import DependAtom, QueryAtom, AtomError
from appi.version import Version


class TestAtomValidityMetaclass(type(TestCase)):

    @staticmethod
    def invalid_test_func_wrapper(atom, strict):
        def test_func(self):
            with self.assertRaises(AtomError):
                DependAtom(atom, strict)
        return test_func

    @staticmethod
    def valid_test_func_wrapper(atom, strict):
        def test_func(self):
            DependAtom(atom, strict)
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
        ('sys-kernel/vanilla-sources::sapher', False), ('~python-3.7-r9999', False),
    ]
    valid_atoms = [
        ('package', False), ('dev-lang/python', True), ('~dev-python/ipython-5.4.0', True),
        ('=x11-libs/qtile-0.10.6', True), ('=toto-3.14*', False),
        ('sys-kernel/vanilla-sources:4.8.0', True),
    ]


class TestQueryAtomStrMetaclass(type(TestCase)):

    @staticmethod
    def test_func_wrapper(a):
        def test_func(self):
            atom = QueryAtom(a, strict=False)
            self.assertEqual(str(atom), a)
        return test_func

    def __new__(mcs, name, bases, attrs):
        for a in attrs['atoms']:
            func_name = 'test_str_{}'.format(a)
            test_func = mcs.test_func_wrapper(a)
            test_func.__name__ = func_name
            attrs[func_name] = test_func
        return super().__new__(mcs, name, bases, attrs)


class TestQueryAtomStr(TestCase, metaclass=TestQueryAtomStrMetaclass):

    atoms = [
        'app-portage/chuse', 'portage', '=dev-python/appi-0.0.2', '~sys-devel/flex-2.6.2',
        'firefox::gentoo', 'sys-kernel/vanilla-sources:4.8.17',
        '=sys-kernel/vanilla-sources-4.8.17-r1:4.8.17::gentoo', '=python-3*',
        '=dev-lang/python-2*:2.7',
    ]


class TestDependAtomStrMetaclass(type(TestCase)):

    @staticmethod
    def test_func_wrapper(a):
        def test_func(self):
            atom = DependAtom(a, strict=False)
            self.assertEqual(str(atom), a)
        return test_func

    def __new__(mcs, name, bases, attrs):
        for a in attrs['atoms']:
            func_name = 'test_str_{}'.format(a)
            test_func = mcs.test_func_wrapper(a)
            test_func.__name__ = func_name
            attrs[func_name] = test_func
        return super().__new__(mcs, name, bases, attrs)


class TestDependAtomStr(TestCase, metaclass=TestDependAtomStrMetaclass):

    atoms = [
        '!app-portage/chuse', '!!portage', '!=dev-python/appi-0.0.2', '~sys-devel/flex-2.6.2',
        'firefox[system-cairo]', 'sys-kernel/vanilla-sources:4.8.17[deblob,symlink]',
        '!!=sys-kernel/vanilla-sources-4.8.17-r1:4.8.17[deblob]', '=python-3*[doc]',
        '=dev-lang/python-2*:2.7',
    ]


class TestGetVersionMetaclass(type(TestCase)):

    @staticmethod
    def test_func_wrapper(a, v):
        def test_func(self):
            atom = DependAtom(a)
            if v is None:
                self.assertIsNone(atom.get_version())
            else:
                version = Version(v)
                self.assertEqual(atom.get_version(), version)
        return test_func

    def __new__(mcs, name, bases, attrs):
        for a, v in attrs['atom_to_version']:
            func_name = 'test_get_version_{}__{}'.format(a, v)
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
        ('=virtual/perl-File-Path-2.120.100_rc-r1', '2.120.100_rc-r1'),
        ('~media-libs/speex-1.2_rc1', '1.2_rc1'),
        ('=sys-kernel/vanilla-sources-4.8.10:4.8.10', '4.8.10'),
    ]


class TestGetVersionGlobPatternMetaclass(type(TestCase)):

    @staticmethod
    def test_func_wrapper(a, expected):
        def test_func(self):
            atom = DependAtom(a, False)
            self.assertEqual(atom._get_version_glob_pattern(), expected)
        return test_func

    def __new__(mcs, name, bases, attrs):
        for atom, expected in attrs['atom_to_pattern']:
            func_name = 'test_get_version_glob_pattern_{}'.format(atom)
            test_func = mcs.test_func_wrapper(atom, expected)
            test_func.__name__ = func_name
            attrs[func_name] = test_func
        return super().__new__(mcs, name, bases, attrs)


class TestGetVersionGlobPattern(TestCase, metaclass=TestGetVersionGlobPatternMetaclass):

    atom_to_pattern = [
        ('foo/bar', '*'),
        ('baz', '*'),
        ('<=foo-bar/baz-1.1', '*'),
        ('<baz-1.2', '*'),
        ('>foo-bar/baz-1.3', '*'),
        ('>=baz-1.4', '*'),
        ('=foo-bar/baz-1.5', '1.5'),
        ('~baz-1.6', '1.6*'),
        ('=foo-bar/baz-1.7*', '1.7*'),
    ]


class TestGetGlobPatternMetaclass(type(TestCase)):

    @staticmethod
    def test_func_wrapper(a, expected):
        def test_func(self):
            atom = DependAtom(a, False)
            self.assertEqual(atom._get_glob_pattern(), expected)
        return test_func

    def __new__(mcs, name, bases, attrs):
        for atom, expected in attrs['atom_to_pattern']:
            func_name = 'test_get_glob_pattern_{}'.format(atom)
            test_func = mcs.test_func_wrapper(atom, expected)
            test_func.__name__ = func_name
            attrs[func_name] = test_func
        return super().__new__(mcs, name, bases, attrs)


class TestGetGlobPattern(TestCase, metaclass=TestGetGlobPatternMetaclass):

    atom_to_pattern = [
        ('foo/bar', 'foo/bar/bar-*.ebuild'),
        ('baz', '*/baz/baz-*.ebuild'),
        ('<=foo-bar/baz-1.1', 'foo-bar/baz/baz-*.ebuild'),
        ('<baz-1.2', '*/baz/baz-*.ebuild'),
        ('>foo-bar/baz-1.3', 'foo-bar/baz/baz-*.ebuild'),
        ('>=baz-1.4', '*/baz/baz-*.ebuild'),
        ('=foo-bar/baz-1.5', 'foo-bar/baz/baz-1.5.ebuild'),
        ('~baz-1.6', '*/baz/baz-1.6*.ebuild'),
        ('=foo-bar/baz-1.7*', 'foo-bar/baz/baz-1.7*.ebuild'),
    ]


class TestListMatchingEbuilds(TestCase):
    """Need to setup a temporary portage directory for these tests"""


class TestMatchesExistingEbuild(TestCase):
    """Need to setup a temporary portage directory for these tests"""


class TestListPossibleUseflags(TestCase):
    """Need to setup a temporary portage directory for these tests"""


class TestIsInstalled(TestCase):
    """Need to setup a temporary portage directory for these tests"""


class TestQueryAtomValidityMetaclass(type(TestCase)):

    @staticmethod
    def invalid_test_func_wrapper(atom, strict):
        def test_func(self):
            with self.assertRaises(AtomError):
                QueryAtom(atom, strict)
        return test_func

    @staticmethod
    def valid_test_func_wrapper(atom, strict):
        def test_func(self):
            QueryAtom(atom, strict)
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


class TestQueryAtomValidity(TestCase, metaclass=TestQueryAtomValidityMetaclass):

    invalid_atoms = [
        ('package', True), ('=dev-lang/python', False), ('~dev-python/ipython', False),
        ('x11-libs/qtile-0.10.6', False), ('toto-3.14*', False), ('<toto-3.14*', False),
        ('sys-kernel/gentoo-sources:4.8.0*', False),
    ]
    valid_atoms = [
        ('package', False), ('dev-lang/python', True), ('~dev-python/ipython-5.4.0', True),
        ('=x11-libs/qtile-0.10.6', True), ('=toto-3.14*', False),
        ('=x11-libs/qtile-0.10.6::sapher', True), ('=toto-3.14*:3.14::gentoo', False),
        ('=virtual/toto-0_beta_alpha-r0', True), ('sys-kernel/gentoo-sources:4.8.0=', True),
    ]


class TestGetRepository(TestCase):
    """Need to setup a temporary portage configuration directory for these tests"""
