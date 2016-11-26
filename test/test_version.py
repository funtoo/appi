# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
from unittest import TestCase

from appi.version import Version, VersionError


class TestVersionValidityMetaclass(type(TestCase)):
    pass


class TestVersionValidity(TestCase, metaclass=TestVersionValidityMetaclass):
    pass


class TestVersionComparisonMetaclass(type(TestCase)):

    @staticmethod
    def test_func_wrapper(v1, v2, i1, i2, comp_method):
        def test_func(self):
            expected = getattr(i1, comp_method)(i2)
            actual = getattr(v1, comp_method)(v2)
            self.assertIs(expected, actual)
        return test_func

    def __new__(mcs, name, bases, attrs):
        ordered_versions = list(enumerate(Version(v) for v in attrs['ordered_versions']))
        comp_methods = ['__gt__', '__lt__', '__ge__', '__le__', '__eq__', '__ne__']
        for i1, v1 in ordered_versions:
            for i2, v2 in ordered_versions:
                for comp_method in comp_methods:
                    func_name = 'test_{}{}{}'.format(v1, comp_method, v2)
                    test_func = mcs.test_func_wrapper(v1, v2, i1, i2, comp_method)
                    test_func.__name__ = func_name
                    attrs[func_name] = test_func
        return super().__new__(mcs, name, bases, attrs)


class TestVersionComparison(TestCase, metaclass=TestVersionComparisonMetaclass):

    ordered_versions = [
        '0_rc0', '0', '0.0', '0.0.0', '0.0.0-r1', '0.1.0', '0.1.0.3', '0.1.3',
        '1.0', '1.0a', '1.0z_pre997', '1.0z', '1.1.9-r5', '1.1.9-r123', '2-r5',
        '2.0', '2.76_alpha1_beta2_pre3_rc4_p5', '2.76_beta1_beta2', '2.76_rc4',
        '2.76', '2.76_p0', '2.76_p1', '2.76_p75', '2.77_pre9999',
        '1999.01', '1999.05.05', '1999.1', '1999.5.5' '2015.02.17', '2016.11.20',
        '9999',
    ]

    def test_different_but_equal_versions_major(self):
        self.assertEqual(Version('5.0'), Version('05.0'))

    def test_different_but_equal_versions_minor(self):
        self.assertEqual(Version('5.0'), Version('5.00'))

    def test_different_but_equal_versions_patch(self):
        self.assertEqual(Version('5.0_p005'), Version('5.00_p5'))


class TestInvalidVersionMetaclass(type(TestCase)):

    @staticmethod
    def test_func_wrapper(version):
        def test_func(self):
            with self.assertRaises(VersionError):
                Version(version)
        return test_func

    def __new__(mcs, name, bases, attrs):
        for version in attrs['invalid_versions']:
            func_name = 'test_invalid_version_{}'.format(version)
            test_func = mcs.test_func_wrapper(version)
            test_func.__name__ = func_name
            attrs[func_name] = test_func
        return super().__new__(mcs, name, bases, attrs)


class TestInvalidVersion(TestCase, metaclass=TestInvalidVersionMetaclass):

    invalid_versions = [
        '1-15', '2.15-12', '3_15', '3.14.bonjour', 'pi', '1-sid', 'funtoo3',
        '1.0z_gamma3', '2.76_beta', '2.76_beta-1', '3.141-rc', '123-r1_pre3',
    ]


class TestGetVersionTuple(TestCase):
    pass


class TestGetBaseTuple(TestCase):
    pass


class TestGetLetterTuple(TestCase):
    pass


class TestGetSuffixTuple(TestCase):
    pass


class TestGetRevisionTuple(TestCase):
    pass


class TestStartswithMetaclass(type(TestCase)):

    @staticmethod
    def test_func_wrapper(v1, v2, expect):
        def test_func(self):
            result = Version(v1).startswith(Version(v2))
            if expect:
                self.assertTrue(result)
            else:
                self.assertFalse(result)
        return test_func

    def __new__(mcs, name, bases, attrs):
        for v1, v2 in attrs['expect_true']:
            func_name = 'test_{}_startswith_{}_is_true'.format(v1, v2)
            test_func = mcs.test_func_wrapper(v1, v2, True)
            test_func.__name__ = func_name
            attrs[func_name] = test_func
        for v1, v2 in attrs['expect_false']:
            func_name = 'test_{}_startswith_{}_is_false'.format(v1, v2)
            test_func = mcs.test_func_wrapper(v1, v2, False)
            test_func.__name__ = func_name
            attrs[func_name] = test_func
        return super().__new__(mcs, name, bases, attrs)


class TestStartswith(TestCase, metaclass=TestStartswithMetaclass):

    expect_true = [
        ('12.34.5-r2', '12'),
        ('12.34.5-r2', '12.34'),
        ('12.34.5-r2', '12.34.5'),
        ('12.34.5-r2', '12.34.5-r2'),
        ('1.2.3d_beta5_p6_rc7', '1.2.3'),
        ('1.2.3d_beta5_p6_rc7', '1.2.3d'),
        ('1.2.3d_beta5_p6_rc7', '1.2.3d_beta5'),
        ('1.2.3d_beta5_p6_rc7', '1.2.3d_beta5_p6'),
        ('1.2.3d_beta5_p6_rc7', '1.2.3d_beta5_p6_rc7'),
    ]
    expect_false = [
        ('12.34.5-r2', '12.34.5-r23'),
        ('12.34.5-r2', '12.3'),
        ('12.34.5-r2', '12.34.5-r6'),
        ('12.34.5-r2', '34.5-r2'),
        ('1.2.3d_beta5_p6_rc7', '1.2.3_beta5'),
        ('1.2.3d_beta5_p6_rc7', '1.2.3_beta5_p6_rc7'),
        ('1.2.3d_beta5_p6_rc7', '1.2.3d_p6_beta5_rc7'),
        ('1.2.3d_beta5_p6_rc7', '1.2.3d_p6_beta5'),
        ('1.2.3d_beta5_p6_rc7', '1.2.3d_rc7'),
    ]

    def test_invalid_version_number(self):
        version = Version('3.14.1')
        with self.assertRaises(VersionError):
            version.startswith('3.14.')

    def test_valid_version_number(self):
        version = Version('3.14.1')
        version.startswith('3.14')


class TestGetUpstreamVersion(TestCase):
    pass
