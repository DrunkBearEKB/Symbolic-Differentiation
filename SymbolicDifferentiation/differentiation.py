#!/usr/bin/env python3

from typing import List
from SymbolicDifferentiation.core import Symbol, Expression, \
    HelpFunctions, Data
from SymbolicDifferentiation.functions import Functions


class Differentiation:
    @staticmethod
    def diff(expression: Expression, symbol: Symbol, order: int = 1,
             value: float = None):
        """
        Calculates the symbolic derivative of a function of a certain order.

        :param expression:
        :type expression: Expression

        :param symbol:
        :type symbol: Symbol

        :param order:
        :type order: int

        :param value:
        :type value: float

        :return:
        :rtype: Expression
        """
        for index_1 in range(order):
            expression = expression.valid()
            expr_tree = expression.tree(symbol)
            latest_letter = sorted(list(expr_tree.keys()))[-1]
            latest_expr = expr_tree[latest_letter]
            expr_diff = Differentiation.__diff_main(latest_expr, expr_tree,
                                                    symbol)

            index_2 = 0
            while index_2 < len(expr_diff):
                if type(expr_diff[index_2]) == list:
                    expr_diff = expr_diff[:index_2] + expr_diff[index_2] + \
                                expr_diff[index_2 + 1:]
                index_2 += 1

            result = ''.join(str(j) for j in expr_diff)
            for (key, val) in expr_tree.items():
                result = result.replace(key, ''.join(str(j) for j in val))
            expression = Expression(result).simplify()

        if value is None:
            return expression
        else:
            exec(f'{symbol}={value}')
            expression = HelpFunctions.replace_functions(str(expression))
            return eval(str(expression))

    @staticmethod
    def __diff_main(expr_parsed, expr_tree, symbol):
        result = []

        temp = []
        for exp_i in expr_parsed:
            if exp_i in '+-':
                if temp:
                    result.append(temp)
                    temp = []
                result.append(exp_i)
            else:
                temp.append(exp_i)
        result.append(temp)

        for index, item in enumerate(result):
            exp_i = item
            if type(exp_i) == list:
                result[index] = Differentiation.__diff_linear_expr(exp_i,
                                                                   expr_tree,
                                                                   symbol)

        return result

    @staticmethod
    def __diff_multiplication(expr_parsed: List[str], expr_tree: dict,
                              symbol: Symbol):
        if not expr_parsed:
            return []
        result = []

        for index_1, item_1 in enumerate(expr_parsed):
            temp = []
            for index_2, item_2 in enumerate(expr_parsed):
                if index_1 == index_2:
                    if '$' in item_2:
                        temp.append(Differentiation.__diff_func(
                            expr_tree[item_2], expr_tree, symbol))
                    elif item_2 == str(symbol):
                        temp.append('1')
                    else:
                        temp = []
                        break
                else:
                    if '$' in item_2:
                        temp.append(expr_tree[item_2])
                    elif item_2 in Data.letters.upper():
                        temp.append(expr_tree[item_2])
                    else:
                        temp.append(expr_parsed[index_2])
            if temp:
                for index_2, item_2 in enumerate(temp[:-1]):
                    temp.insert(1 + 2 * index_2, '*')
                result.append(temp)

                index_2 = 0
                while index_2 != len(result[-1]):
                    if type(result[-1][index_2]) == list:
                        result[-1] = result[-1][:index_2] + \
                                     result[-1][index_2] + \
                                     result[-1][index_2 + 1:]
                    index_2 += 1

        if len(result) == 0:
            return ['0']
        while len(result) != 1:
            result[0] += ['+'] + result[1]
            result.pop(1)

        return result[0]

    @staticmethod
    def __diff_func(expr_parsed: List[str], expr_tree: dict, symbol: Symbol):
        result = Data.diff_functions[expr_parsed[0][:-1]]

        for index, item in enumerate(result):
            if item == '[arg]':
                result = result[:index] + expr_parsed[1:-1] + \
                         result[index + 1:]

        ind = HelpFunctions.find_char_in_all_list('$', result)
        while ind != -1:
            cur_func = expr_tree[result[ind]]
            result = result[:ind] + cur_func + result[ind + 1:]
            ind = HelpFunctions.find_char_in_all_list('$', result)

        if expr_parsed[1:-1] != [str(symbol)]:
            if result != ['']:
                result += ['*', '('] + \
                          Differentiation.__diff_linear_expr(
                              expr_parsed[1:-1], expr_tree, symbol) + [')']
            else:
                result = ['('] + Differentiation.__diff_linear_expr(
                    expr_parsed[1:-1], expr_tree, symbol) + [')']

        return result

    @staticmethod
    def __diff_linear_expr(expr_parsed: List[str], expr_tree: dict,
                           symbol: Symbol):
        if '+' in expr_parsed or '-' in expr_parsed:
            res = []
            temp = []
            for exp_i in expr_parsed:
                if exp_i in '+-':
                    if temp:
                        res.append(temp)
                        temp = []
                    res.append(exp_i)
                else:
                    temp.append(exp_i)
            res.append(temp)

            for index, item in enumerate(res):
                exp_i = item
                if type(exp_i) == list:
                    res[index] = \
                        Differentiation.__diff_linear_expr(exp_i,
                                                           expr_tree,
                                                           symbol)
            result = []
            for index, item in enumerate(res):
                if type(item) == list:
                    result += item
                else:
                    result.append(item)
            return result

        if len(expr_parsed) == 1:
            if str(symbol) in expr_parsed[0]:
                return '1'
            elif '$' in expr_parsed[0]:
                return Differentiation.__diff_func(expr_tree[expr_parsed[0]],
                                                   expr_tree, symbol)
            return '0'

        dividend = []
        divider = []

        operation = '*'
        for exp_i in expr_parsed:
            if exp_i not in Data.operations:
                if operation == '*':
                    dividend.append(exp_i)
                else:
                    divider.append(exp_i)
            else:
                operation = exp_i

        dividend_diff = Differentiation.__diff_multiplication(dividend,
                                                              expr_tree,
                                                              symbol)
        divider_diff = Differentiation.__diff_multiplication(divider,
                                                             expr_tree,
                                                             symbol)

        if len(divider) != 0:
            if dividend[0] not in Data.operations:
                for index, item in enumerate(dividend[:-1]):
                    dividend.insert(1 + 2 * index, '*')
            else:
                for index, item in enumerate(dividend[:-1]):
                    dividend.insert(2 * index, '*')
            if divider[0] not in Data.operations:
                for index, item in enumerate(divider[:-1]):
                    divider.insert(1 + 2 * index, '*')
            else:
                for index, item in enumerate(divider[:-1]):
                    divider.insert(2 * index, '*')
            result = ['(', '('] + dividend_diff + [')', '*', '('] + divider + \
                     [')', '-', '('] + dividend + \
                     [')', '*', '('] + divider_diff + \
                     [')', ')', '/', '('] + divider + \
                     [')', '^', '2']
        else:
            result = dividend_diff

        ind = HelpFunctions.find_char_in_all_list('$', result)
        while ind != -1:
            cur_func = expr_tree[result[ind]]
            result = result[:ind] + cur_func + result[ind + 1:]
            ind = HelpFunctions.find_char_in_all_list('$', result)

        return result
