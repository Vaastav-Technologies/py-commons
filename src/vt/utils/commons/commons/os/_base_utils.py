#!/usr/bin/env python3
# coding=utf-8

"""
Internal reusable common utilities, interfaces and implementations for python projects related to operating systems.
"""

import os
import platform


def _is_platform(platform_name: str) -> bool:
    return platform.system() == platform_name  # pragma: no cover


def _is_os_name(os_name: str) -> bool:
    return os.name == os_name  # pragma: no cover
