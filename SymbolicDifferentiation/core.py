#!/usr/bin/env python3

from io import BytesIO
from tokenize import tokenize

from SymbolicDifferentiation.errors import ValueValidationError, \
    InvalidExpressionError
from SymbolicDifferentiation.simplify import Simplify
from SymbolicDifferentiation.helpFunctions import HelpFunctions
from SymbolicDifferentiation.data import Data


class Symbol:
    def __init__(self, letter: str):
        if type(letter) == str and len(letter) == 1:
            self.__symbol_str = letter
        else:
            raise ValueValidationError()

    def contains_in_expression(self, expr_parsed,
                               left: int, right: int):
        if left > right or left < 0 or right > len(expr_parsed) - 1:
            raise ValueValidationError()

        for index in range(left, right + 1):
            if '$' in expr_parsed[index] or \
                    (self.__symbol_str in expr_parsed[index] and
                     expr_parsed[index][:-1] not in Data.functions):
                if index != 0 and expr_parsed[index - 1] in Data.letters:
                    continue
                if index != len(expr_parsed) - 1 and \
                        expr_parsed[index + 1] in Data.letters:
                    continue
                return True

        return False

    def __add__(self, other):
        return Expression(f'({self.__symbol_str})+({other})')

    def __sub__(self, other):
        return Expression(f'({self.__symbol_str})-({other})')

    def __mul__(self, other):
        return Expression(f'({self.__symbol_str})*({other})')

    def __str__(self):
        return self.__symbol_str


class Expression:
    def __init__(self, expr: str):
        if type(expr) == str:
            self.__expr = expr
            self.__expr_valid = ''
            self.__expr_parsed = []
            self.__expr_tree = {}
        else:
            raise ValueValidationError()

    def __check_validity_brackets(self):
        stack = []
        for index, item in enumerate(self.__expr):
            symbol = item
            if symbol in Data.brackets:
                stack.append((symbol, index))
                while len(stack) >= 2:
                    if stack[-2][0] == '(' and stack[-1][0] == ')' or \
                            stack[-2][0] == '[' and stack[-1][0] == ']' or \
                            stack[-2][0] == '{' and stack[-1][0] == '}' or \
                            stack[-2][0] == '<' and stack[-1][0] == '>':
                        stack.pop(-1)
                        stack.pop(-1)
                    else:
                        break
        return stack[-1][1] if len(stack) != 0 else None

    def __check_validity_operations(self):
        for index, item in enumerate(self.__expr):
            symbol = item
            if symbol in Data.operations:
                if index != 0 and \
                        self.__expr[index - 1] in Data.operations:
                    return index
                if index != len(self.__expr) - 1 and \
                        self.__expr[index + 1] in Data.operations:
                    return index
        return None

    def __check_validity_functions(self):
        for index, item in enumerate(self.__expr):
            if self[index] in Data.brackets:
                if index != 0 and self[index - 1] in Data.letters:
                    j = index - 1
                    func = ''
                    while self[j] in Data.letters:
                        func += self[j]
                        j -= 1
                    func = func[::-1]
                    if len(func) != 1 and func not in Data.functions:
                        return index
        return None

    def __check_validity(self):
        val_brackets = self.__check_validity_brackets()
        if val_brackets is not None:
            raise InvalidExpressionError(self.__expr, val_brackets)
        val_operations = self.__check_validity_operations()
        if val_operations is not None:
            raise InvalidExpressionError(self.__expr, val_operations)
        val_functions = self.__check_validity_functions()
        if val_functions is not None:
            raise InvalidExpressionError(self.__expr, val_functions)

    def valid(self):
        self.__check_validity()

        result = self.__expr
        dict_for_replacement = {' ': '', '**': '^', '+-': '-',
                                '--': '+', '*+': '*', '*-': '*(-1)*',
                                '(-1)*(-1)': '1', '*1*': '*'}
        for key in dict_for_replacement.keys():
            result = result.replace(key, dict_for_replacement[key])

        i = 0
        while i != len(result) - 1:
            if result[i] in Data.brackets_opening:
                if i != 0 and result[i - 1] in Data.letters:
                    j = i - 1
                    func = ''
                    while result[j] in Data.letters:
                        func += result[j]
                        j -= 1
                    func = func[::-1]
                    if len(func) == 1:
                        result = result[:i] + '*' + result[i:]
                        i += 1
            elif result[i] in Data.digits:
                if i + 1 != len(result) - 1 and \
                        result[i + 1] in Data.letters:
                    result = result[:i + 1] + '*' + result[i + 1:]
                    i += 1

            i += 1

        i = 0
        while i != len(result) - 1:
            if result[i] == '^':
                part_left = result[i - 1]
                left = i - 1
                if result[i - 1] in Data.brackets_closing:
                    stack = [result[i - 1]]
                    j = 2
                    while len(stack) != 0:
                        if result[i - j] in Data.brackets:
                            stack.append(result[i - j])
                            while len(stack) >= 2 and \
                                    stack[-1] == Data.brackets[
                                3 - Data.brackets[4:]
                                        .find(stack[-2])]:
                                stack.pop(-1)
                                stack.pop(-1)
                        part_left += result[i - j]
                        left = i - j
                        j += 1

                    if left != 0:
                        j = 1
                        func = ''
                        while left - j != -1 and \
                                result[left - j] in Data.letters:
                            func += result[left - j]
                            j += 1
                        left -= j - 1
                        if func[::-1] in Data.functions:
                            part_left += func

                part_left = part_left[::-1]

                part_right = result[i + 1]
                right = i + 1
                if result[i + 1] in Data.brackets_opening:
                    stack = [result[i + 1]]
                    j = 2
                    while len(stack) != 0:
                        if result[i + j] in Data.brackets:
                            stack.append(result[i + j])
                            while len(stack) >= 2 and stack[-2] == \
                                    Data.brackets[
                                        3 - Data.brackets[4:].find(
                                            stack[-1])]:
                                stack.pop(-1)
                                stack.pop(-1)
                        part_right += result[i + j]
                        right = i + j
                        j += 1

                result = result[:i] + '#' + result[i + 1:]
                new_part = f'exp({part_right}*ln({part_left}))' \
                    if part_left != 'e' else f'exp({part_right})'

                result = result[:left] + new_part + result[right + 1:]
            i += 1

        result = result.replace(' ', '')
        result = result.replace('#', '^')

        self.__expr_valid = Expression(result)

        return Expression(result)

    def parse(self):
        """
        Parse symbolic expression to main parts

        :rtype: List[str]
        """
        if self.__expr_parsed:
            return self.__expr_parsed

        self.valid()
        result = \
            [str(j.string) for j in
             tokenize(BytesIO(str(self.__expr_valid)
                              .encode('utf-8')).readline)][1:]
        index = 0
        while '(' in result and index < len(result):
            if result[index] in Data.functions:
                result[index] += '('
                result[index + 1] += '#'
                index += 1
            elif result[index] == '(#':
                result = result[:index] + result[index + 1:]
            else:
                index += 1

        while '' in result:
            result.remove('')
        while '(#' in result:
            result.remove('(#')
        self.__expr_parsed = result

        return result

    def tree(self, symbol: Symbol):
        """

        :rtype: dict[str] = str
        """
        if self.__expr_tree != {}:
            return self.__expr_tree
        if not self.__expr_parsed:
            self.parse()

        result = {}
        ind = 0
        expr_parsed = self.parse()
        symbols_for_replacement = ' '.join(
            str(letter) for letter in Data.letters.upper()).split()
        index_left = \
            HelpFunctions.rfind_char_in_all_list('(', expr_parsed)

        while index_left != -1 and len(expr_parsed) != 0:
            index_right = index_left
            index_right += HelpFunctions. \
                find_char_in_all_list(')', expr_parsed[index_left:])

            bonus_expr_contains_symbol = \
                '$' if symbol.contains_in_expression(expr_parsed,
                                                     left=index_left,
                                                     right=index_right) else ''
            result[symbols_for_replacement[ind] +
                   bonus_expr_contains_symbol] = \
                expr_parsed[index_left:index_right + 1]

            expr_parsed = \
                expr_parsed[:index_left] + \
                [symbols_for_replacement[ind] +
                 bonus_expr_contains_symbol] + \
                expr_parsed[index_right + 1:]

            ind += 1
            index_left = HelpFunctions. \
                rfind_char_in_all_list('(', expr_parsed)

        if symbol.contains_in_expression(expr_parsed, left=0,
                                         right=len(expr_parsed) - 1):
            bonus_expr_contains_symbol = '$'
        else:
            bonus_expr_contains_symbol = ''
        result[symbols_for_replacement[ind] +
               bonus_expr_contains_symbol] = expr_parsed
        self.__expr_tree = result

        return result

    def simplify(self):
        return Simplify.simplify(self.__expr)

    def __add__(self, other):
        return Expression(f'({self.__expr})+({other})')

    def __iadd__(self, other):
        self.__expr = f'({self.__expr})+({other})'

    def __sub__(self, other):
        return Expression(f'({self.__expr})-({other})')

    def __isub__(self, other):
        self.__expr = f'({self.__expr})-({other})'

    def __mul__(self, other):
        return Expression(f'({self.__expr})*({other})')

    def __imul__(self, other):
        self.__expr = f'({self.__expr})*({other})'

    def __getitem__(self, index):
        return self.__expr[index]

    def __len__(self):
        return len(self.__expr)

    def __str__(self):
        return self.__expr
