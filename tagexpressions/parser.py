# -*- coding: utf-8 -*-

"""
Package to parse logical tag expressions
"""

from collections import deque
from uuid import uuid4
from re import compile as compile_regex
from .models import Literal, Or, And, Not

#: Holds the possible token associativities
ASSOC_LEFT = 0
ASSOC_RIGHT = 1

TOKEN_ASSOCS = {'or': ASSOC_LEFT, 'and': ASSOC_LEFT, 'not': ASSOC_RIGHT}

#: Holds the token precedences
TOKEN_PRECS = {'(': -2, ')': -1, 'or': 0, 'and': 1, 'not': 2}


class TagExpressionError(Exception):
    """Raised for tag expression specific errors"""
    pass


def parse(infix):
    """Parse the given infix string to an expression which can be evaluated.

    Known operators are:
        * or
        * and
        * not

    With the following precedences (from high to low):
        * not
        * and
        * or
        * )
        * (


    :param str infix: the input string expression

    :returns: an expression which can be evaluated with some input values
    """
    # this regex should match most variations of sometag(somevar,someOtherVar). i refer to them as a complex literal because
    # they will not change the evaluation. a should act the same as a(x)
    literal_re = compile_regex(r'(?:\w|\d)+\((?:\w|\d|,)+\)')
    # To support tags with variables, replace all tags containing variables with a unique identifier
    complex_literals = {str(uuid4()): complex_literal for complex_literal in literal_re.findall(infix)}
    # now for each complex literal, replace it with the unique_id into the infix
    for unique_id, complex_literal in complex_literals.items():
        infix = infix.replace(complex_literal, unique_id)
    
    tokens = infix.replace('(', ' ( ').replace(')', ' ) ').strip().split()

    #: Holds the parsed operations
    ops = deque()
    #: Holds the parsed expressions
    expressions = deque()

    for token in tokens:
        if token in TOKEN_ASSOCS:
            while len(ops) > 0 and ops[-1] in TOKEN_ASSOCS and (
                (TOKEN_ASSOCS[token] == ASSOC_LEFT and TOKEN_PRECS[token] <= TOKEN_PRECS[ops[-1]]) or \
                  (TOKEN_ASSOCS[token] == ASSOC_RIGHT and TOKEN_PRECS[token] < TOKEN_PRECS[ops[-1]])):
                create_and_push_expression(ops.pop(), expressions)

            ops.append(token)
        elif token == '(':
            ops.append(token)
        elif token == ')':
            while len(ops) > 0 and ops[-1] != '(':
                create_and_push_expression(ops.pop(), expressions)

            if len(ops) == 0:
                raise TagExpressionError('Unclosed (')

            if ops[-1] == '(':
                ops.pop()
        else:
            # if we replaced the token earlier, then revert that replacement now. 
            create_and_push_expression(token if token not in complex_literals else complex_literals[token], expressions)

    while len(ops) > 0:
        if ops[-1] == '(':
            raise TagExpressionError('Unclosed )')
        create_and_push_expression(ops.pop(), expressions)

    expression = expressions.pop()
    if len(expressions) > 0:
        raise TagExpressionError('Not empty')

    return expression


def evaluate(infix, values):
    """Parse the given infix string and evaluate with the given values.

    :param str infix: the input string expression
    :param list values: a list of values with variables to match
                        against the infix expression.

    :returns: if the given values match the infix expression
    :rtype: bool
    """
    expression = parse(infix)
    return expression.evaluate(values)


def create_and_push_expression(token, expressions):
    """Creates an expression from the given token and adds it
    to the stack of the given expression.

    In the case of "and" and "or" expressions the last expression
    is poped from the expression stack to link it to the new
    created one.
    """
    if token == 'and':
        right_expr = expressions.pop()
        expressions.append(And(expressions.pop(), right_expr))
    elif token == 'or':
        right_expr = expressions.pop()
        expressions.append(Or(expressions.pop(), right_expr))
    elif token == 'not':
        expressions.append(Not(expressions.pop()))
    else:
        expressions.append(Literal(token))
