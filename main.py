#!/usr/bin/env python3

import argparse
from SymbolicDifferentiation.core import Symbol, Expression
from SymbolicDifferentiation.differentiation import Differentiation

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('expression', type=str, help='Expression')
    parser.add_argument('symbol', type=str, help='Symbol')
    parser.add_argument('value', type=str, help='float', nargs='?')
    args = parser.parse_args()

    result = Differentiation.diff(Expression(args.expression),
                                  Symbol(args.symbol), value=args.value)
    print(result)
