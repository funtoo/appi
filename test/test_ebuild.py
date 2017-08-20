# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
from pathlib import Path
from unittest import TestCase

from appi.atom import DependAtom
from appi.ebuild import Ebuild, EbuildError
from appi.version import Version


class TestEbuildValidityMetaclass(type(TestCase)):

    @staticmethod
    def invalid_test_func_wrapper(path):
        def test_func(self):
            with self.assertRaises(EbuildError):
                Ebuild(path)
        return test_func

    @staticmethod
    def valid_test_func_wrapper(path):
        def test_func(self):
            Ebuild(path)
        return test_func

    def __new__(mcs, name, bases, attrs):
        for path in attrs['invalid_ebuilds']:
            func_name = 'test_invalid_ebuild_{}'.format(path)
            test_func = mcs.invalid_test_func_wrapper(path)
            test_func.__name__ = func_name
            attrs[func_name] = test_func
        for path in attrs['valid_ebuilds']:
            func_name = 'test_valid_ebuild_{}'.format(path)
            test_func = mcs.valid_test_func_wrapper(path)
            test_func.__name__ = func_name
            attrs[func_name] = test_func
        return super().__new__(mcs, name, bases, attrs)


class TestEbuildValidity(TestCase, metaclass=TestEbuildValidityMetaclass):

    invalid_ebuilds = [
        '/cat-name/pkg/pkg-1.9.ebuild',
        'dir/cat-name/pkg/pkg-1.9.ebuild',
        'another/dir/cat-name/pkg/pkg-1.9.ebuild',
        '/usr/portage/cat/pkg-1.9.ebuild',
        'usr/portage/cat/pkg/pkg-1.9.ebuild',
        '/usr/portage/cat/pkg/nopkg-1.9.ebuild',
        '/usr/portage/cat/pkg/nopkg-1.9.ebuild',
        'this is certainly not a valid ebuild',
        'this is certainly not a valid.ebuild',
        '/usr/portage/virtual/pkg/3.14-r1.ebuild',
        '/usr/portage/x11-wm/qtile/qtile3.14-r1.ebuild',
        '/usr/portage/dev-lang/python/python-3.4.0_pre2-r1:3.4.ebuild',
        '/usr/portage/dev-lang/python/python-3.5.0',
        '/usr/portage/dev-lang/python/python-3.5.0.sh',
        '/usr/portage/dev-lang/python/python-3.5.0..ebuild',
        '/usr/portage/dev-lang/python/python.ebuild',
        '/usr/portage/dev-lang/python/python-.ebuild',
        '/usr/portage/cat/pkg/pkg-1.9.5B_pre05_alpha12_beta5_pre10-r99.ebuild',
    ]
    valid_ebuilds = [
        '/repo/cat-name/pkg/pkg-1.9.ebuild',
        '/dir/cat-name/pkg/pkg-1.9.ebuild',
        '/another/dir/cat-name/pkg/pkg-1.9.ebuild',
        '/usr/portage/cat/pkg/pkg-1.9.ebuild',
        '/usr/portage/cat/pkg/pkg-1.9.5z_pre05_alpha12_beta5_pre10-r99.ebuild',
        '/usr/portage/cat-name/nopkg/nopkg-1.9.ebuild',
        '/usr/portage/cat/no-pkg/no-pkg-1.9.ebuild',
        '/this/is/certainly/a/valid/valid-0.ebuild',
        '/this/is/certainly/a/valid/valid-9999.ebuild',
        '/this/is/certainly/a/valid/valid-99999z.ebuild',
        '/usr/portage/virtual/pi/pi-3.14-r1.ebuild',
        '/usr/portage/x11-wm/qtile/qtile-3.14-r1.ebuild',
        '/usr/portage/dev-lang/python/python-3.4.0_pre2-r1.ebuild',
        '/usr/portage/dev-lang/python/python-3.5.0.ebuild',
        '/var/overlay/dev-lang/python/python-3.5.0.ebuild',
        '/home/me/path/to/my overlay/dev-lang/python/python-3.5.0.ebuild',
        Path('/home/me/path/to/my overlay/dev-lang/python/python-3.5.0.ebuild'),
        Path('/usr/potage/dev-lang/python/python-3.5.0.ebuild'),
    ]


class TestEbuildStr(TestCase):
    """Need to setup a temporary portage directory for these tests"""


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
        ('/repo/cat/pkg/pkg-0.12.3.ebuild', '0.12.3'),
        ('/repo/cat/pkg/pkg-3.14_pre5-r1.ebuild', '3.14_pre5-r1'),
        ('/repo/cat/pkg/pkg-5.ebuild', '5'),
        ('/repo/cat/pkg-a/pkg-a-4.4.00c_p2_pre5-r10.ebuild', '4.4.00c_p2_pre5-r10'),
    ]


class TestMatchesAtomMetaclass(type(TestCase)):

    @staticmethod
    def test_func_wrapper(e, a, assert_what):
        def test_func(self):
            ebuild = Ebuild(e)
            atom = DependAtom(a, strict=False)
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
        ('/repo/cat/pkg/pkg-0.1.0_pre0-r1.ebuild', [
            'cat/pkg', '=cat/pkg-0.1.0_pre0-r1', '~cat/pkg-0.1.0_pre0',
            'pkg', '>=pkg-0.1', '<pkg-0.1.0',
        ]),
        ('/usr/portage/dev-lang/python/python-3.5.2.ebuild', [
            'dev-lang/python', '<=dev-lang/python-4', '~dev-lang/python-3.5.2',
            '>python-3.5.0', '=python-3*',
        ]),
    ]
    unmatches = [
        ('/my/overlay/cat/pkg/pkg-1.2.3_p3-r5.ebuild', [
            'cat/package', '=category/pkg-1.2.3_p3-r5', '~cat/pkg-0.1.0_pre0',
            'pack', '<=pkg-1.2.3', '>cat/pkg-1.2.3_p3-r5',
        ]),
        ('/home/tony/Funtoo/Workspace/sapher-overlay/dev-lang/python/python-2.7.10-r1.ebuild', [
            'dev-python/python', 'dev-lang/haskell', '~dev-lang/python-3.5.2',
            '>=python-3', '=dev-lang/python-3*',
        ]),
    ]


class TestDbDirMetaclass(type(TestCase)):

    @staticmethod
    def test_func_wrapper(e, o):
        def test_func(self):
            ebuild = Ebuild(e)
            self.assertEqual(ebuild.db_dir, Path(o))
        return test_func

    def __new__(mcs, name, bases, attrs):
        for path, output in attrs['values']:
            func_name = 'test_db_dir_{}'.format(path)
            test_func = mcs.test_func_wrapper(path, output)
            test_func.__name__ = func_name
            attrs[func_name] = test_func
        return super().__new__(mcs, name, bases, attrs)


class TestDbDir(TestCase, metaclass=TestDbDirMetaclass):

    values = [
        ('/usr/portage/sys-apps/portage/portage-2.3.8.ebuild',
         '/var/db/pkg/sys-apps/portage-2.3.8'),
        ('/usr/portage/foo-bar/foobar/foobar-3.15-r11.ebuild',
         '/var/db/pkg/foo-bar/foobar-3.15-r11'),
        ('/var/overlays/toto/dev-db/postgresql/postgresql-10_beta3.ebuild',
         '/var/db/pkg/dev-db/postgresql-10_beta3'),
        ('/toto/dev-libs/clang/clang-9.ebuild',
         '/var/db/pkg/dev-libs/clang-9'),
    ]
