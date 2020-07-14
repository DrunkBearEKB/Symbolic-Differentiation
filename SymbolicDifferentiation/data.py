#!/usr/bin/env python3


class Data:
    e = 2.718281828459045
    pi = 3.14159
    letters = 'abcdefghijklmnopqrstuvwxyz'
    digits = '0123456789'
    operations = '+-*/^'
    brackets = '({<[]>})'
    brackets_opening = '({<['
    brackets_closing = ']>})'

    functions = ['exp', 'ln',
                 'sin', 'cos', 'tg', 'ctg', 'sec', 'csc',
                 'arcsin', 'arccos', 'arctg', 'arcctg',
                 'sh', 'ch', 'th', 'cth']

    diff_functions = {'': [''],
                      # Exponential functions
                      'exp': ['exp(', '[arg]', ')'],
                      'ln': ['1', '/', '(', '[arg]', ')'],
                      # Trigonometric functions
                      'sin': ['cos(', '[arg]', ')'],
                      'cos': ['-', 'sin(', '[arg]', ')'],
                      'tg': ['1', '/', 'cos(', '[arg]', ')', '^',
                             '2'],
                      'ctg': ['-', '1', '/', 'sin(', '[arg]', ')',
                              '^', '2'],
                      'sec': ['tg(', '[arg]', ')', '*', 'sec(',
                              '[arg]', ')'],
                      'csc': ['-', 'ctg(', '[arg]', ')', '*', 'csc(',
                              '[arg]',
                              ')'],
                      # Inverse Trigonometric functions
                      'arcsin': ['1', '/', '(', '1', '-', '(',
                                 '[arg]', ')', '^',
                                 '2', ')', '^', '2'],
                      'arccos': ['-', '1', '/', '(', '1', '-', '(',
                                 '[arg]', ')',
                                 '^', '2', ')', '^', '2'],
                      'arctg': ['1', '/', '(', '1', '+', '(', '[arg]',
                                ')', '^',
                                '2', ')'],
                      'arcctg': ['-', '1', '/', '(', '1', '+', '(',
                                 '[arg]', ')',
                                 '^', '2', ')'],
                      # Hyperbolic functions
                      'sh': ['ch(', '[arg]', ')'],
                      'ch': ['sh(', '[arg]', ')'],
                      'th': ['1', '/', 'ch(', '[arg]', ')', '^', '2'],
                      'cth': ['-', '1', '/', 'sh(', '[arg]', ')', '^',
                              '2'],
                      # Special functions
                      'gamma': ['gamma(', '[arg]', ')', '*',
                                'digamma(', '[arg]',
                                ')'],
                      'digamma': ['digamma(', '[arg]', ')'],
                      'li': ['1', '/', 'ln(', '[arg]', ')'],
                      'ei': ['exp(', '[arg]', ')', '/', '(', '[arg]',
                             ')'],
                      'erf': ['2', '*', 'exp(', '-', '[arg]', '^',
                              '2', ')', '/',
                              'pi', '^', '(', '1', '/', '2', ')']}

    operator_priorities = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    for key_func in functions:
        operator_priorities[key_func] = 4
