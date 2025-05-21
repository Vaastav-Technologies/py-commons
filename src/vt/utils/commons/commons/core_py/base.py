#!/usr/bin/env python3
# coding=utf-8

"""
Reusable interfaces and sentinel objects related to core python.
"""
from typing import TypeAlias, Final

from vt.utils.commons.commons.core_py._base import _MISSING

MISSING_TYPE: TypeAlias = _MISSING
"""
Sentinel value type useful for type hinting.
"""

UNSET_TYPE: TypeAlias = MISSING_TYPE
"""
Sentinel value type to denote un-setting variable.
"""

MISSING: Final[MISSING_TYPE] = MISSING_TYPE()
"""
Sentinel to represent a missing value. Can be used:

* as default value for a parameter which has ``None`` as a valid value.
"""

UNSET: Final[UNSET_TYPE] = MISSING
"""
Sentinel that can be used to unset a previously set value.
"""
