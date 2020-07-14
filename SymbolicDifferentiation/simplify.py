#!/usr/bin/env python3

from SymbolicDifferentiation.data import Data
import SymbolicDifferentiation.core
import re


class Simplify:
    @staticmethod
    def simplify(expr: str):
        SymbolicDifferentiation.core.Expression(expr)
        if type(expr) != str:
            expr = str(expr)

        expr = Simplify.__simplify_main(expr)
        expr = Simplify.__simplify_brackets(expr)
        expr = Simplify.__simplify_numbers(expr)

        return SymbolicDifferentiation.core.Expression(expr)

    @staticmethod
    def __simplify_main(expr: str):
        dict_for_replacement = {' ': '',
                                '**': '^', '+-': '-', '--': '+', '*+': '*',
                                '*-': '*(-1)*', '(-1)*(-1)': '1', '*1*': '*',
                                '+0+': '', '-0+': '', '+0-': '', '-0-': '',
                                '(0+': '(', '(0-': '(', '+0)': ')', '-0)': ')',
                                '(1*': '(', '*1)': ')'}
        for (key, value) in dict_for_replacement.items():
            expr = expr.replace(key, value)
        if expr[0] == '+':
            expr = expr[1:]

        return expr

    @staticmethod
    def __simplify_brackets(expr: str):
        brackets = []
        unclosed_brackets = []
        counter = 0
        counter_max = 0

        for index, item in enumerate(expr):
            if item == '(':
                unclosed_brackets.append((index, counter_max))
                brackets.append([expr[index], index, counter_max])
                counter += 1
                counter_max += 1
            elif item == ')':
                brackets.append([item, index, unclosed_brackets[-1][1]])
                unclosed_brackets.pop(-1)
                counter -= 1

        pairs_left = []
        for index, item in enumerate(brackets[:-1]):
            if item[0] == '(' and brackets[index + 1][0] == '(' and \
                    brackets[index + 1][1] - item[1] == 1:
                pairs_left.append([(item[2], brackets[index + 1][2]),
                                   (item[1], brackets[index + 1][1])])

        pairs_right = []
        for index, item in reversed(list(enumerate(brackets))):
            if item[0] == ')' and brackets[index - 1][0] == ')' and \
                    item[1] - brackets[index - 1][1] == 1:
                pairs_right.append([(item[2], brackets[index - 1][2]),
                                    (item[1], brackets[index - 1][1])])

        pairs = []
        for index_1, item_1 in enumerate(pairs_left):
            for index_2, item_2 in enumerate(pairs_right):
                if item_1[0] == item_2[0]:
                    pairs.append(item_1[1][0])
                    pairs.append(item_2[1][1])

        pairs = list(set(pairs))
        for index, item in enumerate(pairs):
            expr = expr[:item] + '@' + expr[item + 1:]
        expr = expr.replace('@', '')

        return expr

    @staticmethod
    def __simplify_numbers(expr: str):
        numbers = re.findall(r'\d*\.\d+|\d+', expr)
        dict_replace = {}
        counter = 0
        while len(numbers) != 0:
            if numbers[0] == 0:
                numbers.pop(0)
                continue

            index = expr.index(numbers[0])
            if index != 0 and \
                    expr[index - 1] in Data.brackets_opening and \
                    index != len(expr) - 1 and \
                    expr[
                        index + len(numbers[0])] in Data.brackets_closing:
                expr = expr[:index - 1] + \
                       Data.letters[counter].upper() + \
                       expr[index + len(numbers[0]) + 1:]
                dict_replace[Data.letters[counter].upper()] = numbers[0]
                counter += 1
            numbers.pop(0)
        for (key, value) in dict_replace.items():
            expr = expr.replace(key, value)

        return expr
