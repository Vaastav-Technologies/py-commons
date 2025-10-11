#!/usr/bin/env python3
# coding=utf-8

"""
Reusable common utilities, interfaces and implementations for python projects related to POSIX operating system
families.
"""

from vt.utils.commons.commons.os._base_utils import _is_os_name

POSIX_ID_STR = "posix"
"""
POSIX OS families are determined by python using this string.

https://docs.python.org/3/library/os.html#os.name
"""


def not_posix() -> bool:
    """
    :return: ``True`` if system is not POSIX. ``False`` otherwise.
    """
    return not is_posix()  # pragma: no cover


def is_posix() -> bool:
    """
    :return: ``True`` if system is POSIX. ``False`` otherwise.
    """
    return _is_os_name(POSIX_ID_STR)  # pragma: no cover
