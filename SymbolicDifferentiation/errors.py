#!/usr/bin/env python3


class ValueValidationError(Exception):
    def __init__(self):
        self.__message = f'Wrong value!'

    def __str__(self):
        return self.__message


class InvalidExpressionError(Exception):
    def __init__(self, expr, index):
        self.__message = f'Expression is invalid!\n' \
                         f'{expr}\n' \
                         f'{" " * index}↑\n' \
                         f'{" " * (index - 4)}[ Error ]'

    def __str__(self):
        return self.__message
