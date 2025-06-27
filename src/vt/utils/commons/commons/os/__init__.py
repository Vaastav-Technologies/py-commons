#!/usr/bin/env python3
# coding=utf-8

"""
Reusable common utilities, interfaces and implementations for python projects related to operating systems.
"""

from vt.utils.commons.commons.os.windows import is_windows as is_windows
from vt.utils.commons.commons.os.windows import not_windows as not_windows

from vt.utils.commons.commons.os.linux import is_linux as is_linux
from vt.utils.commons.commons.os.linux import not_linux as not_linux

from vt.utils.commons.commons.os.mac import is_mac as is_mac
from vt.utils.commons.commons.os.mac import not_mac as not_mac

from vt.utils.commons.commons.os.posix import is_posix as is_posix
from vt.utils.commons.commons.os.posix import not_posix as not_posix
