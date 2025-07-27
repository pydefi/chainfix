# Copyright 2021 PyDefi Development Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Some context code adapted from Python's decimal module
# Copyright (c) 2004 Python Software Foundation.

from enum import Enum
from typing import Optional


class Overflow(Enum):
    SATURATE = 1
    WRAP = 2


class _Context:

    def __init__(self,
                 wordlength: Optional[int] = None,
                 precision: Optional[int] = None,
                 overflow: Optional[Overflow] = None):
        dc = self.get_default()
        self.precision = precision if precision is not None else dc.precision
        self.wordlength = wordlength if wordlength is not None else dc.wordlength
        self.overflow = overflow if overflow is not None else dc.overflow

    def copy(self):
        """Returns a deep copy from self."""
        nc = self.__class__(self.wordlength, self.precision, self.overflow)
        return nc

    __copy__ = copy

    def get_default(self):
        raise NotImplementedError

    def __repr__(self) -> str:
        return '{}(wordlength={}, precision={}, overflow={})'.format(
            self.__class__.__name__,
            self.wordlength,
            self.precision,
            self.overflow)


class DecimalContext(_Context):
    base = 10

    def get_default(self):
        try:
            dc = DefaultDecimalContext
        except NameError:
            dc = None

        return dc


class BinaryContext(_Context):
    base = 2

    def get_default(self):
        try:
            dc = DefaultBinaryContext
        except NameError:
            dc = None

        return dc


DefaultDecimalContext = DecimalContext(
    wordlength=256,
    precision=18,
    overflow=Overflow.SATURATE
)

DefaultBinaryContext = BinaryContext(
    wordlength=32,
    precision=16,
    overflow=Overflow.SATURATE
)

# Context Functions

# The getcontext() and setcontext() function manage access to a thread-local
# current context.

import contextvars

_current_decimal_context_var = contextvars.ContextVar('chainfix_decimal')


def get_decimal_context():
    """Returns this thread's decimal context.

    If this thread does not yet have a context, returns
    a new context and sets this thread's context.
    New contexts are copies of DefaultDecimalContext.
    """
    try:
        return _current_decimal_context_var.get()
    except LookupError:
        context = DecimalContext()
        _current_decimal_context_var.set(context)
        return context


def set_decimal_context(context):
    """Set this thread's context to context."""
    if context in (DefaultDecimalContext,):
        context = context.copy()
        context.clear_flags()
    _current_decimal_context_var.set(context)


_current_binary_context_var = contextvars.ContextVar('chainfix_binary')


def get_binary_context():
    """Returns this thread's binary context.

    If this thread does not yet have a context, returns
    a new context and sets this thread's context.
    New contexts are copies of DefaultBinaryContext.
    """
    try:
        return _current_binary_context_var.get()
    except LookupError:
        context = BinaryContext()
        _current_binary_context_var.set(context)
        return context


def set_binary_context(context):
    """Set this thread's context to context."""
    if context in (DefaultBinaryContext,):
        context = context.copy()
        context.clear_flags()
    _current_binary_context_var.set(context)


del contextvars  # Don't contaminate the namespace
