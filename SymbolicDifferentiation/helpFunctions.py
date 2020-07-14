#!/usr/bin/env python3

from SymbolicDifferentiation.data import Data


class HelpFunctions:
    @staticmethod
    def find_char_in_all_list(symbol_str: str, list_: list):
        for index, item in enumerate(list_):
            if symbol_str in item:
                return index

        return -1

    @staticmethod
    def rfind_char_in_all_list(symbol_str: str, list_: list):
        for index, item in reversed(list(enumerate(list_))):
            if symbol_str in list_[index]:
                return index

        return -1

    @staticmethod
    def replace_functions(expr: str):
        for func_name in Data.functions:
            expr = expr.replace(func_name, f'Functions.{func_name}')
        return expr
