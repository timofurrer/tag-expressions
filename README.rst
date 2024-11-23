tag-expressions
===============

Package to evaluate logical tag expressions by using a modified version of the `Shunting Yard algorithm <https://en.wikipedia.org/wiki/Shunting-yard_algorithm>`_.
This package is a Python port of cucumbers tag expression.

It's also used by `radish <https://github.com/radish-bdd/radish>`_.

|Build Status| |PyPI package version| |PyPI python versions|


Installing
----------

.. code:: bash

    $ pip install tag-expressions

Here is a tease
---------------


.. code:: python

    >>> from tagexpressions import parse
    >>>
    >>> expression = '( a and b ) or ( c and d )'
    >>> compiled_expression = parse(expression)
    >>> print(compiled_expression)
    ( ( a and b ) or ( c and d ) )
    >>>
    >>> data = ['a', 'b', 'c', 'd']
    >>> assert compiled_expression.evaluate(data) == True
    >>>
    >>> data = ['a', 'c']
    >>> assert compiled_expression.evaluate(data) == False
    >>>
    >>>
    >>> expression = 'not a or b and not c or not d or e and f'
    >>> compiled_expression = parse(expression)
    >>> print(compiled_expression)
    ( ( ( not ( a ) or ( b and not ( c ) ) ) or not ( d ) ) or ( e and f ) )
    >>>
    >>> data = ['b', 'e', 'f']
    >>> assert compiled_expression.evaluate(data) == True
    >>>
    >>> data = ['a', 'c', 'd']
    >>> assert compiled_expression.evaluate(data) == False


Usage
-----

Available operators
~~~~~~~~~~~~~~~~~~~

* **or** - "or" conjunction of two given variables
* **and** - "and" conjunction of two given variables
* **not** - negation of a single variable

Every other token given in an *infix* is considered a variable.

Operator precedence
~~~~~~~~~~~~~~~~~~~

From high to low:

* ()
* or
* and
* not

.. |Build Status| image:: https://github.com/timofurrer/tag-expressions/actions/workflows/build.yml/badge.svg
   :target: https://github.com/timofurrer/tag-expressions/actions/workflows/build.yml
.. |PyPI package version| image:: https://badge.fury.io/py/tag-expressions.svg
   :target: https://badge.fury.io/py/tag-expressions
.. |PyPI python versions| image:: https://img.shields.io/pypi/pyversions/tag-expressions.svg
   :target: https://pypi.python.org/pypi/tag-expressions
