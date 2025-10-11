#!/usr/bin/env python3
# coding=utf-8

"""
Reusable common utilities, interfaces and implementations for python projects related to Linux operating system.
"""

from vt.utils.commons.commons.os._base_utils import _is_platform

LINUX_ID_STR = "Linux"
"""
Linux OS determined by python using this string.

https://docs.python.org/3/library/platform.html#platform.system
"""


def not_linux() -> bool:
    """
    :return: ``True`` if system is not linux. ``False`` otherwise.
    """
    return not is_linux()  # pragma: no cover


def is_linux() -> bool:
    """
    :return: ``True`` if system is linux. ``False`` otherwise.
    """
    return _is_platform(LINUX_ID_STR)  # pragma: no cover
