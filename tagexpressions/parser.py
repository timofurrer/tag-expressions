# -*- coding: utf-8 -*-

"""
Package to parse logical tag expressions
"""

from collections import deque

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
    """
    Parse the given string logical tag expression.
    """
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
            create_and_push_expression(token, expressions)

    while len(ops) > 0:
        if ops[-1] == '(':
            raise TagExpressionError('Unclosed )')
        create_and_push_expression(ops.pop(), expressions)

    expression = expressions.pop()
    if len(expressions) > 0:
        raise TagExpressionError('Not empty')

    return expression


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
