# -*- coding: utf-8 -*-

"""
Package to parse logical tag expressions
"""

from .parser import parse, evaluate

__VERSION__ = '1.1.0'

# only expose the parse function
__all__ = ['parse', 'evaluate']
