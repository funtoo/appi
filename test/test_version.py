# -*- coding: utf-8 -*-
import unittest

from appi.version import Version, VersionError


class TestVersionComparisonMetaclass(type(unittest.TestCase)):

    def __new__(mcs, name, bases, attrs):
        ordered_versions = list(enumerate(Version(v) for v in attrs['ordered_versions']))
        comp_methods = ['__gt__', '__lt__', '__ge__', '__le__', '__eq__', '__ne__']
        for i1, v1 in ordered_versions:
            for i2, v2 in ordered_versions:
                for comp_method in comp_methods:
                    func_name = 'test_{}{}{}'.format(v1, comp_method, v2)

                    def test_func(self):
                        expected = getattr(i1, comp_method)(i2)
                        actual = getattr(v1, comp_method)(v2)
                        self.assertEqual(expected, actual)
                    test_func.__name__ = func_name
                    attrs[func_name] = test_func
        return super().__new__(mcs, name, bases, attrs)


class TestVersionComparison(unittest.TestCase, metaclass=TestVersionComparisonMetaclass):

    ordered_versions = [
        '0_rc0', '0', '0.0', '0.0.0', '0.0.0-r1', '0.1.0', '0.1.0.3', '0.1.3',
        '1.0', '1.0a', '1.0z_pre997', '1.0z', '1.1.9-r5', '1.1.9-r123', '2-r5',
        '2.0', '2.76_alpha1_beta2_pre3_rc4_p5', '2.76_beta1_beta2', '2.76_rc4',
        '2.76', '2.76_p0', '2.76_p1', '2.76_p75', '2.77_pre9999',
        '1999.05.05', '2015.02.17', '2016.11.20',
        '9999',
    ]


class TestInvalidVersionMetaclass(type(unittest.TestCase)):

    def __new__(mcs, name, bases, attrs):
        for version in attrs['invalid_versions']:
            func_name = 'test_invalid_version_{}'.format(version)

            def test_func(self):
                with self.assertRaises(VersionError):
                    Version(version)
            test_func.__name__ = func_name
            attrs[func_name] = test_func
        return super().__new__(mcs, name, bases, attrs)


class TestInvalidVersion(unittest.TestCase, metaclass=TestInvalidVersionMetaclass):

    invalid_versions = [
        '1-15', '2.15-12', '3_15', '3.14.bonjour', 'pi', '1-sid', 'funtoo3',
        '1.0z_gamma3', '2.76_beta', '2.76_beta-1', '3.141-rc', '123-r1_pre3',
    ]
