#!/usr/bin/env python3
# coding=utf-8

"""
Reusable common utilities, interfaces and implementations for python projects related to Mac operating system.
"""

from vt.utils.commons.commons.os._base_utils import _is_platform

MAC_ID_STR = "Darwin"
"""
Mac OS determined by python using this string.

https://docs.python.org/3/library/platform.html#platform.system
"""


def not_mac() -> bool:
    """
    :return: ``True`` if system is not mac. ``False`` otherwise.
    """
    return not is_mac()  # pragma: no cover


def is_mac() -> bool:
    """
    :return: ``True`` if system is mac. ``False`` otherwise.
    """
    return _is_platform(MAC_ID_STR)  # pragma: no cover
