#!/usr/bin/env python3
# coding=utf-8

"""
Type narrowing of the ``core_py`` type guards, checked by mypy through ``pytest-mypy-testing``.

Each ``@pytest.mark.mypy_testing`` function is one pytest test. The plugin runs mypy on this file and compares mypy's
messages with the ``# R:`` (revealed type) and ``# E:`` (error) comments: a missing, extra or different message
fails the test. Nothing here runs at runtime.

mypy checks against the Python running pytest, so the CI test matrix covers both ``TypeIs`` imports: ``typing`` on
3.13+ and ``typing_extensions`` on 3.12.
"""

from types import EllipsisType
from typing import reveal_type

import pytest

from vt.utils.commons.commons.core_py import (
    MISSING,
    UNSET,
    Missing,
    Unset,
    is_ellipses,
    is_missing,
    is_unset,
    not_none_not_missing,
    not_none_not_sentinel,
    not_none_not_unset,
    strictly_int,
)


@pytest.mark.mypy_testing
def mypy_test_is_missing_narrows_both_branches(val: int | Missing) -> None:
    """``is_missing()`` narrows to ``Missing`` when ``True`` and drops it when ``False``."""
    if is_missing(val):
        reveal_type(val)  # R: vt.utils.commons.commons.core_py.base.Missing
    else:
        reveal_type(val)  # R: int


@pytest.mark.mypy_testing
def mypy_test_is_unset_narrows_both_branches(val: str | Unset) -> None:
    """``is_unset()`` narrows to ``Unset`` when ``True`` and drops it when ``False``."""
    if is_unset(val):
        reveal_type(val)  # R: vt.utils.commons.commons.core_py.base.Unset
    else:
        reveal_type(val)  # R: str


@pytest.mark.mypy_testing
def mypy_test_is_ellipses_narrows_both_branches(val: int | EllipsisType) -> None:
    """``is_ellipses()`` narrows to ``EllipsisType`` when ``True`` and drops it when ``False``."""
    if is_ellipses(val):
        reveal_type(val)  # R: types.EllipsisType
    else:
        reveal_type(val)  # R: int


@pytest.mark.mypy_testing
def mypy_test_not_none_not_unset_narrows_both_branches(val: int | None | Unset) -> None:
    """``not_none_not_unset()`` narrows to the value type when ``True`` and to ``None | Unset`` when ``False``."""
    if not_none_not_unset(val):
        reveal_type(val)  # R: int
    else:
        reveal_type(val)  # R: None | vt.utils.commons.commons.core_py.base.Unset


@pytest.mark.mypy_testing
def mypy_test_not_none_not_missing_narrows_both_branches(
    val: str | None | Missing,
) -> None:
    """``not_none_not_missing()`` narrows to the value type when ``True`` and to ``None | Missing`` when ``False``."""
    if not_none_not_missing(val):
        reveal_type(val)  # R: str
    else:
        reveal_type(val)  # R: None | vt.utils.commons.commons.core_py.base.Missing


@pytest.mark.mypy_testing
def mypy_test_strictly_int_narrows_only_the_true_branch(val: int | str) -> None:
    """
    ``strictly_int()`` narrows to ``int`` when ``True`` and keeps ``int | str`` when ``False``.

    Bools are ints yet make it return ``False``, so the ``False`` branch must keep ``int``. If ``strictly_int()``
    ever returns ``TypeIs[int]``, the ``else`` type becomes ``str`` and the ``.upper()`` error disappears, failing
    this test.
    """
    if strictly_int(val):
        reveal_type(val)  # R: int
    else:
        reveal_type(val)  # R: int | str
        val.upper()  # E: [union-attr]


@pytest.mark.mypy_testing
def mypy_test_not_none_not_sentinel_narrows_only_the_true_branch(
    val: str | None,
) -> None:
    """``not_none_not_sentinel()`` narrows when ``True`` (sentinel not in the declared type) and not when ``False``."""
    if not_none_not_sentinel(val, sentinel=UNSET):
        reveal_type(val)  # R: str
    else:
        reveal_type(val)  # R: str | None


@pytest.mark.mypy_testing
def mypy_test_is_comparison_narrows_only_the_true_branch(val: int | Missing) -> None:
    """
    A plain ``is MISSING`` check narrows only to ``Missing``, as ``Missing`` is an ordinary class: use
    ``is_missing()`` to narrow both branches.

    This pins the known limit of the current sentinels, so a change to them (or to mypy) shows up here.
    """
    if val is MISSING:
        reveal_type(val)  # R: vt.utils.commons.commons.core_py.base.Missing
    else:
        reveal_type(val)  # R: int | vt.utils.commons.commons.core_py.base.Missing
