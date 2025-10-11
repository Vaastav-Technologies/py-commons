#!/usr/bin/env python3
# coding=utf-8

"""
Reusable common utilities, interfaces and implementations for python projects related to Windows operating system.
"""

from vt.utils.commons.commons.os._base_utils import _is_platform

WINDOWS_ID_STR = "Windows"
"""
Windows OS determined by python using this string.

https://docs.python.org/3/library/platform.html#platform.system
"""


def not_windows() -> bool:
    """
    :return: ``True`` if system is not windows. ``False`` otherwise.
    """
    return not is_windows()  # pragma: no cover


def is_windows() -> bool:
    """
    :return: ``True`` if system is windows. ``False`` otherwise.
    """
    return _is_platform(WINDOWS_ID_STR)  # pragma: no cover
