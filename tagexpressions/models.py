# -*- coding: utf-8 -*-

"""
Package to parse logical tag expressions
"""

class Literal(object):  # pylint: disable=too-few-public-methods
    """
    Represents a literal expression
    """
    def __init__(self, value):
        self.value = value

    def evaluate(self, values):
        """Evaluate the expression

        Check if the literal is in the given
        set of values.
        """
        return self.value in values

    def __str__(self):
        return self.value


class Or(object):  # pylint: disable=too-few-public-methods
    """
    Represents an "OR" expression
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, values):
        """Evaluate the "OR" expression

        Check if the left "or" right expression
        evaluate to True.
        """
        return self.left.evaluate(values) or self.right.evaluate(values)

    def __str__(self):
        return '( {0} or {1} )'.format(self.left, self.right)


class And(object):  # pylint: disable=too-few-public-methods
    """
    Represent an "AND" expression
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, values):
        """Evaluate the "AND" expression

        Check if the left "and" right expression
        evaluate to True.
        """
        return self.left.evaluate(values) and self.right.evaluate(values)

    def __str__(self):
        return '( {0} and {1} )'.format(self.left, self.right)


class Not(object):  # pylint: disable=too-few-public-methods
    """
    Represents a "NOT" expression
    """
    def __init__(self, expression):
        self.expression = expression

    def evaluate(self, values):
        """
        Evaluate the "NOT" expression

        Check if the given expression does not
        evaluate to True.
        """
        return not self.expression.evaluate(values)

    def __str__(self):
        return 'not ( {0} )'.format(self.expression)
