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
    """

    pass


class Unset(Sentinel):
    """
    Sentinel type that can be used to unset a previously set value.
    """

    pass


MISSING: Final[Missing] = Missing()
"""
Sentinel to represent a missing value. Can be used:

* as default value for a parameter which has ``None`` as a valid value.
"""

UNSET: Final[Unset] = Unset()
"""
Sentinel that can be used to unset a previously set value.
"""
