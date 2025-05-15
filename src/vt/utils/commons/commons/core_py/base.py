#!/usr/bin/env python3
# coding=utf-8

"""
Reusable interfaces and sentinel objects related to core python.
"""

from vt.utils.commons.commons.core_py._base import _MISSING

MISSING = _MISSING()
"""
Sentinel to represent a missing value. Can be used:

* as default value for a parameter which has ``None`` as a valid value.
"""

MISSING_TYPE = _MISSING
"""
Sentinel value type useful for type hinting.
"""
