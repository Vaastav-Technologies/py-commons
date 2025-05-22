#!/usr/bin/env python3
# coding=utf-8

"""
Reusable utilities related to core python.
"""
from collections.abc import Callable
from typing import Any, cast
from vt.utils.commons.commons.core_py.base import MISSING, Missing, UNSET, Unset


def is_missing[T](obj: T) -> bool:
    """
    Determine whether an ``obj`` is ``MISSING``, i.e. not supplied by the caller.

    Examples:

    * ``obj`` is ``MISSING``, i.e. not supplied by the caller:

    >>> obj_to_test = MISSING
    >>> is_missing(obj_to_test)
    True

    * ``obj`` is supplied but ``None``, i.e. it is supplied by the caller and hence, not missing:

    >>> is_missing(None)
    False

    * ``obj`` is truthy primitive and supplied but non ``None``, i.e. it is supplied by the caller and
      hence, not missing:

    >>> is_missing(2) or is_missing('a') or is_missing(2.5) or is_missing(True) or is_missing(1+0j) or is_missing(b'y')
    False

    * ``obj`` is falsy primitive and supplied but non ``None``, i.e. it is supplied by the caller and
      hence, not missing:

    >>> is_missing(0) or is_missing('') or is_missing(0.0) or is_missing(False) or is_missing(0j) or is_missing(b'')
    False

    * ``obj`` is truthy non-primitive and supplied but non ``None``, i.e. it is supplied by the caller and
      hence, not missing:

    >>> is_missing([1, 2, 3]) or is_missing({1: 'a', 2: 'b'}) or is_missing({2.5, 2.0})
    False

    * ``obj`` is falsy non-primitive and supplied but non ``None``, i.e. it is supplied by the caller and
      hence, not missing:

    >>> is_missing([]) or is_missing({}) or is_missing(set())
    False

    :param obj: object to be tested whether it was supplied by caller or not.
    :return: ``True`` if the ``obj`` is missing and not supplied by caller, ``False`` otherwise.
    """
    return obj is MISSING


def is_unset[T](obj: T) -> bool:
    """
    Determine whether an ``obj`` is ``UNSET``, i.e. deliberately unset an already set value by the caller.

    Examples:

    * ``obj`` is ``UNSET``, i.e. deliberately unset by the caller:

    >>> obj_to_test = UNSET
    >>> is_unset(obj_to_test)
    True

    * ``obj`` is supplied but ``None``, i.e. it is supplied by the caller and hence, not unset:

    >>> is_unset(None)
    False

    * ``obj`` is truthy primitive and supplied but non ``None``, i.e. it is supplied by the caller and
      hence, not unset:

    >>> is_unset(2) or is_unset('a') or is_unset(2.5) or is_unset(True) or is_unset(1+0j) or is_unset(b'y')
    False

    * ``obj`` is falsy primitive and supplied but non ``None``, i.e. it is supplied by the caller and
      hence, not unset:

    >>> is_unset(0) or is_unset('') or is_unset(0.0) or is_unset(False) or is_unset(0j) or is_unset(b'')
    False

    * ``obj`` is truthy non-primitive and supplied but non ``None``, i.e. it is supplied by the caller and
      hence, not unset:

    >>> is_unset([1, 2, 3]) or is_unset({1: 'a', 2: 'b'}) or is_unset({2.5, 2.0})
    False

    * ``obj`` is falsy non-primitive and supplied but non ``None``, i.e. it is supplied by the caller and
      hence, not unset:

    >>> is_unset([]) or is_unset({}) or is_unset(set())
    False

    :param obj: object to be tested whether it was supplied by caller or not.
    :return: ``True`` if the ``obj`` is deliberatley unset by the caller, ``False`` otherwise.
    """
    return obj is UNSET


def _alt_if_predicate_true[T, U](obj: Any | U, alt: T, predicate: Callable[[Any | U], bool]) -> T:
    """
    Get an alternate object ``alt`` if the queried object ``obj`` is ``MISSING``, i.e. it is not supplied by the caller.

    Note::

        Returned value is always of the type of alt object.

    :param obj: object to be tested whether it was fulfills the ``predicate`` or not.
    :param predicate: A predicate that ``obj`` needs to fulfill to be returned from this method.
    :param alt: alternate object to be returned if ``obj`` does not fulfill the ``predicate``.
    :return: ``obj`` if it fulfills the ``predicate`` else ``alt``.
    """
    if predicate(obj):
        return alt
    if type(obj) != type(alt):
        raise TypeError(f"Unexpected type: `obj` and `alt` must be of the same type. type(obj): {type(obj)}, "
                        f"type(alt): {type(alt)}")
    return alt if is_missing(obj) else cast(T, obj)


def alt_if_missing[T](obj: Any | Missing, alt: T) -> T:
    """
    Get an alternate object ``alt`` if the queried object ``obj`` is ``MISSING``, i.e. it is not supplied by the caller.

    Note::

        Returned value is always of the type of alt object.

    Examples:

    * Main object ``obj`` is returned if it is not ``MISSING``, i.e. it was supplied by the caller. Also, the returned
      object ``obj`` is of the type of alternative ``alt`` object, test for falsy ``obj`` objects:

    >>> assert alt_if_missing(None, None) is None
    >>> assert alt_if_missing(0, 2) == 0
    >>> assert alt_if_missing(0.0, 1.3) == 0.0
    >>> assert alt_if_missing('', 'z') == ''
    >>> assert alt_if_missing([], [1, 2, 3]) == []
    >>> assert alt_if_missing({}, {'a': 1, 'b': 2}) == {}
    >>> assert alt_if_missing(set(), {1, 2, 3}) == set()
    >>> assert alt_if_missing(0j, 1+2j) == 0j

    * Main object ``obj`` is returned if it is not ``MISSING``, i.e. it was supplied by the caller. Also, the returned
      object ``obj`` is of the type of alternative ``alt`` object, test for truthy ``obj`` objects:

    >>> assert alt_if_missing('a', 'null') == 'a'
    >>> assert alt_if_missing(-1, 2) == -1
    >>> assert alt_if_missing(0.9, 1.3) == 0.9
    >>> assert alt_if_missing('jo', 'z') == 'jo'
    >>> assert alt_if_missing([9, 8, 7], [1, 2, 3]) == [9, 8, 7]
    >>> assert alt_if_missing({'z': 10, 'y': 9, 'x': 8}, {'a': 1, 'b': 2}) == {'z': 10, 'y': 9, 'x': 8}
    >>> assert alt_if_missing({0, 9, 8}, {1, 2, 3}) == {0, 9, 8}
    >>> assert alt_if_missing(1+0j, 1+2j) == 1+0j

    * Alternate object ``alt`` is returned when main object ``obj`` is ``MISSING``, i.e. it was not supplied by
      the caller. Also, the returned object ``alt`` is of the type of alternative ``alt`` object:

    >>> assert alt_if_missing(MISSING, None) is None
    >>> assert alt_if_missing(MISSING, 0) == 0
    >>> assert alt_if_missing(MISSING, 0.0) == 0,0
    >>> assert alt_if_missing(MISSING, '') == ''
    >>> assert alt_if_missing(MISSING, []) == []
    >>> assert alt_if_missing(MISSING, {}) == {}
    >>> assert alt_if_missing(MISSING, set()) == set()
    >>> assert alt_if_missing(MISSING, 0j) == 0j

    * Errs if main object ``obj`` is not ``MISSING`` and hence, is supplied by the caller, but its type is different
      from the type of the alternative ``alt`` object:

    >>> alt_if_missing('a', 2)
    Traceback (most recent call last):
    TypeError: Unexpected type: `obj` and `alt` must be of the same type. type(obj): <class 'str'>, type(alt): <class 'int'>

    >>> alt_if_missing([], (2, 3, 4))
    Traceback (most recent call last):
    TypeError: Unexpected type: `obj` and `alt` must be of the same type. type(obj): <class 'list'>, type(alt): <class 'tuple'>

    :param obj: object to be tested whether it was supplied by caller or not.
    :param alt: alternate object to be returned if ``obj`` was not supplied by the caller.
    :return: ``obj`` if it was supplied by the caller else ``alt``.
    """
    return _alt_if_predicate_true(obj, alt, is_missing)


def alt_if_unset[T](obj: Any | Unset, alt: T) -> T:
    """
    Get an alternate object ``alt`` if the queried object ``obj`` is ``UNSET``, i.e. it is deliberately unset by
    the caller.

    Note::

        Returned value is always of the type of alt object.

    Examples:

    * Main object ``obj`` is returned if it is not ``UNSET``, i.e. it was not deliberately unset by the caller. Also,
      the returned object ``obj`` is of the type of alternative ``alt`` object, test for falsy ``obj`` objects:

    >>> assert alt_if_unset(None, None) is None
    >>> assert alt_if_unset(0, 2) == 0
    >>> assert alt_if_unset(0.0, 1.3) == 0.0
    >>> assert alt_if_unset('', 'z') == ''
    >>> assert alt_if_unset([], [1, 2, 3]) == []
    >>> assert alt_if_unset({}, {'a': 1, 'b': 2}) == {}
    >>> assert alt_if_unset(set(), {1, 2, 3}) == set()
    >>> assert alt_if_unset(0j, 1+2j) == 0j

    * Main object ``obj`` is returned if it is not ``UNSET``, i.e. it was not deliberately unset by the caller. Also,
      the returned object ``obj`` is of the type of alternative ``alt`` object, test for truthy ``obj`` objects:

    >>> assert alt_if_unset('a', 'null') == 'a'
    >>> assert alt_if_unset(-1, 2) == -1
    >>> assert alt_if_unset(0.9, 1.3) == 0.9
    >>> assert alt_if_unset('jo', 'z') == 'jo'
    >>> assert alt_if_unset([9, 8, 7], [1, 2, 3]) == [9, 8, 7]
    >>> assert alt_if_unset({'z': 10, 'y': 9, 'x': 8}, {'a': 1, 'b': 2}) == {'z': 10, 'y': 9, 'x': 8}
    >>> assert alt_if_unset({0, 9, 8}, {1, 2, 3}) == {0, 9, 8}
    >>> assert alt_if_unset(1+0j, 1+2j) == 1+0j

    * Alternate object ``alt`` is returned when main object ``obj`` is ``UNSET``, i.e. it was deliberately unset by
      the caller. Also, the returned object ``alt`` is of the type of alternative ``alt`` object:

    >>> assert alt_if_unset(UNSET, None) is None
    >>> assert alt_if_unset(UNSET, 0) == 0
    >>> assert alt_if_unset(UNSET, 0.0) == 0,0
    >>> assert alt_if_unset(UNSET, '') == ''
    >>> assert alt_if_unset(UNSET, []) == []
    >>> assert alt_if_unset(UNSET, {}) == {}
    >>> assert alt_if_unset(UNSET, set()) == set()
    >>> assert alt_if_unset(UNSET, 0j) == 0j

    * Errs if main object ``obj`` is not ``UNSET`` and hence, is supplied by the caller, but its type is different
      from the type of the alternative ``alt`` object:

    >>> alt_if_unset('a', 2)
    Traceback (most recent call last):
    TypeError: Unexpected type: `obj` and `alt` must be of the same type. type(obj): <class 'str'>, type(alt): <class 'int'>

    >>> alt_if_unset([], (2, 3, 4))
    Traceback (most recent call last):
    TypeError: Unexpected type: `obj` and `alt` must be of the same type. type(obj): <class 'list'>, type(alt): <class 'tuple'>

    :param obj: object to be tested whether it was deliberately unset by the caller or not.
    :param alt: alternate object to be returned if ``obj`` was not supplied by the caller.
    :return: ``alt`` if ``obj`` was deliberately unset by the caller, else ``obj``.
    """
    return _alt_if_predicate_true(obj, alt, is_unset)


def is_ellipses(obj: Any) -> bool:
    """
    :param obj: object to be tested whether it was supplied by caller or not.
    :return: ``True`` if the ``obj`` is missing and not supplied by caller, ``False`` otherwise.
    """
    return obj is ...


def alt_if_ellipses[T](obj, alt: T) -> T:
    """
    Get an alternate object ``alt`` if the queried object ``obj`` is ``...``, i.e. it is not supplied by the caller or
    is deliberatey kept ``...`` by the caller.

    Note::

        Returned value is always of the type of alt object.

    Examples:

    * Main object ``obj`` is returned if it is not ``...``, i.e. it was supplied by the caller. Also, the returned
      object ``obj`` is of the type of alternative ``alt`` object, test for falsy ``obj`` objects:

    >>> assert alt_if_ellipses(None, None) is None
    >>> assert alt_if_ellipses(0, 2) == 0
    >>> assert alt_if_ellipses(0.0, 1.3) == 0.0
    >>> assert alt_if_ellipses('', 'z') == ''
    >>> assert alt_if_ellipses([], [1, 2, 3]) == []
    >>> assert alt_if_ellipses({}, {'a': 1, 'b': 2}) == {}
    >>> assert alt_if_ellipses(set(), {1, 2, 3}) == set()
    >>> assert alt_if_ellipses(0j, 1+2j) == 0j

    * Main object ``obj`` is returned if it is not ``...``, i.e. it was supplied by the caller. Also, the returned
      object ``obj`` is of the type of alternative ``alt`` object, test for truthy ``obj`` objects:

    >>> assert alt_if_ellipses('a', 'null') == 'a'
    >>> assert alt_if_ellipses(-1, 2) == -1
    >>> assert alt_if_ellipses(0.9, 1.3) == 0.9
    >>> assert alt_if_ellipses('jo', 'z') == 'jo'
    >>> assert alt_if_ellipses([9, 8, 7], [1, 2, 3]) == [9, 8, 7]
    >>> assert alt_if_ellipses({'z': 10, 'y': 9, 'x': 8}, {'a': 1, 'b': 2}) == {'z': 10, 'y': 9, 'x': 8}
    >>> assert alt_if_ellipses({0, 9, 8}, {1, 2, 3}) == {0, 9, 8}
    >>> assert alt_if_ellipses(1+0j, 1+2j) == 1+0j

    * Alternate object ``alt`` is returned when main object ``obj`` is ``...``, i.e. it was not supplied by
      the caller or is deliberately kept ``...`` by the caller. Also, the returned object ``alt`` is of the type of
      alternative ``alt`` object:

    >>> assert alt_if_ellipses(..., None) is None
    >>> assert alt_if_ellipses(..., 0) == 0
    >>> assert alt_if_ellipses(..., 0.0) == 0,0
    >>> assert alt_if_ellipses(..., '') == ''
    >>> assert alt_if_ellipses(..., []) == []
    >>> assert alt_if_ellipses(..., {}) == {}
    >>> assert alt_if_ellipses(..., set()) == set()
    >>> assert alt_if_ellipses(..., 0j) == 0j

    * Errs if main object ``obj`` is not ``...`` and hence, is supplied by the caller, but its type is different
      from the type of the alternative ``alt`` object:

    >>> alt_if_ellipses('a', 2)
    Traceback (most recent call last):
    TypeError: Unexpected type: `obj` and `alt` must be of the same type. type(obj): <class 'str'>, type(alt): <class 'int'>

    >>> alt_if_ellipses([], (2, 3, 4))
    Traceback (most recent call last):
    TypeError: Unexpected type: `obj` and `alt` must be of the same type. type(obj): <class 'list'>, type(alt): <class 'tuple'>

    :param obj: object to be tested whether it was supplied as ellipses by caller or not.
    :param alt: alternate object to be returned if ``obj`` is supplied as ellipses by the caller.
    :return: ``obj`` if it was supplied as ellipses by the caller, else ``alt``.
    """
    return _alt_if_predicate_true(obj, alt, is_ellipses)


def fallback_on_none[T](value:T | None, default_val: T | None) -> T | None:
    """
    Get ``value`` if it is non-``None`` else get ``default_val``.

    Examples:

    >>> fallback_on_none('a', 'b')
    'a'

    >>> fallback_on_none(None, 'b')
    'b'

    >>> fallback_on_none(None, True)
    True

    >>> fallback_on_none(True, False)
    True

    * on Falsy values:

    >>> fallback_on_none([], [1, 2])
    []

    >>> fallback_on_none({}, {1: 2, 2: 3})
    {}

    >>> fallback_on_none(set(), {1, 2, 3})
    set()

    >>> fallback_on_none((),
    ...                 (1, 2, 3)) # noqa: some tuple warning
    ()

    >>> fallback_on_none(False, True)
    False

    :param value: The main value to return if it is not ``None``.
    :param default_val: returned if ``value`` is ``None``.
    :return: ``default_val`` if ``value`` is ``None`` else ``value``.
    """
    return default_val if value is None else value


def fallback_on_none_strict[T](value: T | None, default_val: T) -> T:
    """
    Same as ``fallback_on_non_strict()`` but has an assertion guarantee that ``default_val`` is non-``None``.

    Examples:

    >>> fallback_on_none_strict('a', 'b')
    'a'

    >>> fallback_on_none_strict('a',
    ...                         None) # noqa: just for example
    Traceback (most recent call last):
    AssertionError: default_val must not be None.

    :param value: The main value to return if it is not ``None``.
    :param default_val: returned if ``value`` is ``None``.
    :return: ``default_val`` if ``value`` is ``None`` else ``value``.
    """
    assert default_val is not None, "default_val must not be None."
    return cast(T, fallback_on_none(value, default_val))
