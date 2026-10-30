#!/usr/bin/env python3
# coding=utf-8

"""
Reusable interfaces and sentinel objects related to core python.
"""

from typing import Final


class Sentinel:
    """
    Class denoting sentinel values.
    """

    pass


class Missing(Sentinel):
    """
    A Sentinel type to represent a missing value. Can be used:

    * as default value for a parameter which has ``None`` as a valid value.

    Use the ``MISSING`` constant and never create another ``Missing``: ``is_missing()`` and ``not_none_not_missing()``
    tell type checkers that ``MISSING`` is the only ``Missing``.
    """

    pass


class Unset(Sentinel):
    """
    Sentinel type that can be used to unset a previously set value.

    Use the ``UNSET`` constant and never create another ``Unset``: ``is_unset()`` and ``not_none_not_unset()`` tell
    type checkers that ``UNSET`` is the only ``Unset``.
    """

    pass


MISSING: Final[Missing] = Missing()
"""
Sentinel to represent a missing value. Can be used:

* as default value for a parameter which has ``None`` as a valid value.

It is the only ``Missing`` object.
"""

UNSET: Final[Unset] = Unset()
"""
Sentinel that can be used to unset a previously set value.

It is the only ``Unset`` object.
"""
