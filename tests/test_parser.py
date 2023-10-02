# -*- coding: utf-8 -*-

"""
Package to parse logical tag expressions
"""

import pytest

from tagexpressions import parse, evaluate


@pytest.mark.parametrize('infix, expected', [
    ('a and b', '( a and b )'),
    ('a or b', '( a or b )'),
    ('not a', 'not ( a )'),
    ('( a and b ) or ( c and d )', '( ( a and b ) or ( c and d ) )'),
    ('not a or b and not c or not d or e and f', '( ( ( not ( a ) or ( b and not ( c ) ) ) or not ( d ) ) or ( e and f ) )')
])
def test_parser(infix, expected):
    """Test the tag expression parser"""
    assert str(parse(infix)) == expected


@pytest.mark.parametrize('infix, values, expected', [
    ('a and b', ['a', 'b'], True),
    ('a and b', ['b', 'a'], True),
    ('a and b', ['a'], False),
    ('a or b', ['a', 'b'], True),
    ('a or b', ['b', 'a'], True),
    ('a or b', ['a'], True),
    ('a or b', ['b'], True),
    ('a or b', ['c'], False),
    ('not a', ['b'], True),
    ('not a', ['a'], False),
    ('not a', [], True),
    ('not a(x)', [], True),
    ('not a(x)', ['a(x)'], False),
    ('a(x) or b', ['a(x)'], True),
    ('a(x) or b', ['b'], True),
    ('a(x) or b', [''], False),
    ('a(x,y) or b', [''], False),
    ('sometag(someValue,y) or b', [''], False),
    ('sometag(someValue,y) or b(x)', ['b(x)'], True),
    ('a or (sometag(someValue,y) and not b(x))', ['b(x)', 'sometag(someValue, y)'], False),
    ('c(y) and (author(inquisitev) or (sometag(someValue,y) and not b(x)))', ['c(y)', 'sometag(someValue,y)'], True),
    ('c(y) and (author(inquisitev) or (sometag(someValue,y) and not b(x)))', ['c(y)', 'author(inquisitev)'], True),
    ('c(y) and not (author(inquisitev) or (sometag(someValue,y) and not b(x)))', ['c(y)', "b(x)"], True)
])
def test_basic_evaluation(infix, values, expected):
    """Test basic tag expression evaluation"""
    assert parse(infix).evaluate(values) == expected


@pytest.mark.parametrize('infix, values, expected', [
    ('( a and b ) or ( c and d )', ['a', 'b', 'c', 'd'], True),
    ('( a and b ) or ( c and d )', ['c', 'd'], True),
    ('( a and b ) or ( c and d )', ['a', 'b'], True),
    ('( a and b ) or ( c and d )', ['a', 'c'], False),
    ('not a or b and not c or not d or e and f', ['b', 'e', 'f'], True),
    ('not a or b and not c or not d or e and f', ['a', 'b', 'e', 'f'], True),
    ('not a or b and not c or not d or e and f', ['a', 'b', 'c'], True),
    ('not a or b and not c or not d or e and f', ['a', 'c', 'd'], False),
])
def test_complex_evaluation(infix, values, expected):
    """Test complex tag expression evaluation"""
    assert parse(infix).evaluate(values) == expected


@pytest.mark.parametrize('infix, values, expected', [
    ('a and b', ['a', 'b'], True),
    ('a and b', ['a'], False),
    ('a or b', ['a', 'b'], True),
    ('a or b', ['a'], True),
    ('not a', ['b'], True),
    ('sometag(someValue,y) or b', ['b'], True),
    ('sometag(someValue,y) or b', ['sometag(someValue,y)'], True)
])
def test_direct_evaluation(infix, values, expected):
    """Test direct evaluation of an infix against some values"""
    assert evaluate(infix, values) == expected
