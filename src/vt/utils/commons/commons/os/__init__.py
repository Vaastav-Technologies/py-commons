#!/usr/bin/env python3
# coding=utf-8

"""
Reusable common utilities, interfaces and implementations for python projects related to operating systems.
"""

from vt.utils.commons.commons.os.windows import is_windows, not_windows
from vt.utils.commons.commons.os.linux import is_linux, not_linux
from vt.utils.commons.commons.os.mac import is_mac, not_mac
from vt.utils.commons.commons.os.posix import is_posix, not_posix
