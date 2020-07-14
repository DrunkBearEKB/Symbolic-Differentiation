#!/usr/bin/env python3

import unittest
from SymbolicDifferentiation.core import Symbol, Expression, \
    ValueValidationError, InvalidExpressionError
from SymbolicDifferentiation.differentiation import Differentiation


class TestSymbolicDifferentiation(unittest.TestCase):
    def _check__values(self, expression_diff, expression_diff_correct):
        self.assertEqual(expression_diff_correct, str(expression_diff))

    # ==========================================================
    # TEST DIFF Main
    def test_constant(self):
        expr = Expression('1')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x),
                            '0')

    def test_symbol(self):
        expr = Expression('x')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x),
                            '1')

    # ==========================================================
    # TEST DIFF Exponential functions
    def test_exponential_functions_1(self):
        expr = Expression('exp(x)')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x),
                            'exp(x)')

    def test_exponential_functions_2(self):
        expr = Expression('ln(x)')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x),
                            '1/(x)')

    # ==========================================================
    # TEST DIFF Trigonometric functions
    def test_trigonometrical_functions_1(self):
        expr = Expression('sin(x)')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x),
                            'cos(x)')

    def test_trigonometrical_functions_2(self):
        expr = Expression('cos(x)')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x),
                            '-sin(x)')

    def test_trigonometrical_functions_3(self):
        expr = Expression('tg(x)')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x),
                            '1/cos(x)^2')

    def test_trigonometrical_functions_4(self):
        expr = Expression('ctg(x)')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x),
                            '-1/sin(x)^2')

    def test_trigonometrical_functions_5(self):
        expr = Expression('sec(x)')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x),
                            'tg(x)*sec(x)')

    def test_trigonometrical_functions_6(self):
        expr = Expression('csc(x)')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x),
                            '-ctg(x)*csc(x)')

    # ==========================================================
    # TEST DIFF Inverse Trigonometric functions
    def test_inverse_trigonometrical_functions_1(self):
        expr = Expression('arcsin(x)')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x),
                            '1/(1-(x)^2)^2')

    def test_inverse_trigonometrical_functions_2(self):
        expr = Expression('arccos(x)')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x),
                            '-1/(1-(x)^2)^2')

    def test_inverse_trigonometrical_functions_3(self):
        expr = Expression('arctg(x)')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x),
                            '1/(1+(x)^2)')

    def test_inverse_trigonometrical_functions_4(self):
        expr = Expression('arcctg(x)')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x),
                            '-1/(1+(x)^2)')

    # ==========================================================
    # TEST DIFF Hyperbolic functions
    def test_hyperbolic_functions_1(self):
        expr = Expression('sh(x)')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x),
                            'ch(x)')

    def test_hyperbolic_functions_2(self):
        expr = Expression('ch(x)')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x),
                            'sh(x)')

    def test_hyperbolic_functions_3(self):
        expr = Expression('th(x)')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x),
                            '1/ch(x)^2')

    def test_hyperbolic_functions_4(self):
        expr = Expression('cth(x)')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x),
                            '-1/sh(x)^2')

    # ==========================================================
    # TEST DIFF Complicated functions
    def test_different_functions_1(self):
        expr = Expression('sin(x)^2')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x),
                            'exp(2*ln(sin(x)))*(2*1/(sin(x))*(cos(x)))')

    def test_different_functions_2(self):
        expr = Expression('sin(2/exp(x))')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x),
                            'cos(2/exp(x))*((0*(exp(x))-'
                            '(2)*(exp(x)))/(exp(x))^2)')

    def test_different_functions_3(self):
        expr = Expression('sin(2/exp(x)+7*arcsin(x))')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x),
                            'cos(2/exp(x)+7*arcsin(x))*((0*(exp(x))-(2)*'
                            '(exp(x)))/(exp(x))^2+7*1/(1-(x)^2)^2)')

    # ==========================================================
    # TEST Calculations Errors
    def test_calculations_1(self):
        expr = Expression('sin(x)')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x, value=1),
                            '0.5403023058681398')

    def test_calculations_2(self):
        expr = Expression('cos(x)')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x, value=1),
                            '-0.8414709848078965')

    def test_calculations_3(self):
        expr = Expression('sin(x)+cos(x)')
        x = Symbol('x')
        self._check__values(Differentiation.diff(expr, x, value=1),
                            '-0.30116867893975674')

    # ==========================================================
    # TEST Errors
    def test_error_1(self):
        try:
            x = Symbol('xx')
            self.assertEqual(True, False)
        except ValueValidationError:
            self.assertEqual(True, True)

    def test_error_2(self):
        try:
            expr = Expression('sin(x))').valid()
            self.assertEqual(True, False)
        except InvalidExpressionError:
            self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
