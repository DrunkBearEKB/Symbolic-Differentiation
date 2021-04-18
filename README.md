# _SymbolicDifferentiation_

_Tip, it is better not to use this library, for example, a better thing in this regard is site **WolframAlpha** (https://www.wolframalpha.com/) or library **SymPy** (https://github.com/sympy/sympy)._

---

#### _Main definitions_:

**Symbol** - the class required for differentiation; an instance of this class defines the symbol for differentiation.
_Example:_

    x = Symbol('x')
    
**Expression** - the class required for differentiation; an instance of this class defines the symbolic expression for differentiation.
_Example:_

    expression = Expression('3*sin(x)+cos(x)')
   

---

#### _How to use library_:

    x = Symbol('x')
    expr = Expression('3*sin(x)+cos(x)')
    
    expr_diff = SymbolicDifferentiation.diff(expr, x))  # 3*cos(x)-sin(x)
    expr_diff = SymbolicDifferentiation.diff(expr, x, order=3))  # 3*(-1)*cos(x)+sin(x)
    
##### _You can also use other helper methods:_
    
    expr.valid()  # Expression('3*sin(x)+cos(x)') -> Expression('3*sin(x)+cos(x)')
    expr_parsed = expr.parse()  # ['3', '*', 'sin(', 'x', ')', '+', 'cos(', 'x', ')']
    
##### _Arithmetic operations on Symbols and Expressions:_

    expr_1 = Expression('sin(x)')
    expr_2 = Expression('cos(x)')
    
    expr_3 = Symbol('x') + Symbol('y'),  # Expression('x+y')
    expr_4 = Symbol('x') - Symbol('y')   # Expression('x-y')
    expr_5 = Symbol('x') * Symbol('y')   # Expression('x*y')
    expr_6 = expr_1 + expr_2  # Expression('sin(x)+cos(x)')
    expr_7 = expr_1 - expr_2  # Expression('sin(x)-cos(x)')
    expr_8 = expr_1 * expr_2  # Expression('sin(x)*cos(x)')  

---

#### _Using Console:_ 
`python main.py "expression: Expression [!]" "symbol: Symbol [!]" "Value_symbol: float [?]"` 

_[!] - necessary argument, [?] - unnecessary argument_

    python main.py sin(x) x      # -> cos(x)
    python main.py sin(x) x 1    # -> 0.5403023058681398

---

#### _Required:_
**Python 3.6 and higher version**


#### _To use this library you need to have the following installed modules:_
1. **tokenize**
2. **argparse**

---

#### _Author: Ivanenko Grigoriy, Ural State Federal University, 2020._
