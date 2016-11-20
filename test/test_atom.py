# -*- coding: utf-8 -*-
import unittest

from appi.atom import Atom, AtomError


class TestAtomValidityMetaclass(type(unittest.TestCase)):

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


class TestInvalidAtom(unittest.TestCase, metaclass=TestAtomValidityMetaclass):

    invalid_atoms = [
        ('package', True), ('=dev-lang/python', False), ('~dev-python/ipython', False),
        ('x11-libs/qtile-0.10.6', False), ('toto-3.14*', False), ('<toto-3.14*', False),
    ]
    valid_atoms = [
        ('package', False), ('dev-lang/python', True), ('~dev-python/ipython-5.4.0', True),
        ('=x11-libs/qtile-0.10.6', True), ('=toto-3.14*', False),
    ]
