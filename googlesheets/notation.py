#!/usr/bin/env python

import re
import typing

A1_RANGE_EXPRESSION = re.compile(r'^[A-Z]+\d*(:[A-Z]+\d*)?$')

# use for type annotations
#
a1 = typing.TypeVar('a1')

def is_valid_syntax(expr: a1):
    parts = expr.split('!')

    if len(parts) < 2:
        return True

    return A1_RANGE_EXPRESSION.match(parts[1])
