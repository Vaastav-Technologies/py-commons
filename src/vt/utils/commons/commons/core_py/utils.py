#!/usr/bin/env python3
# coding=utf-8

"""
Reusable utilities related to core python.
"""

import sys
from collections.abc import Callable, Sequence
from types import EllipsisType
from typing import Any, Literal, TypeGuard, cast, overload

if sys.version_info >= (3, 13):
    from typing import TypeIs
else:
    from typing_extensions import TypeIs

from vt.utils.commons.commons.core_py.base import MISSING, UNSET, Missing, Unset


def is_missing(obj: object) -> TypeIs[Missing]:
    """
    Check whether ``obj`` is ``MISSING``, i.e. it was not supplied by the caller.

    Type checkers narrow ``obj`` on both branches: to ``Missing`` when this returns ``True``, and to the rest of its
    declared type (e.g. ``int`` from ``int | Missing``) when it returns ``False``. That relies on ``MISSING`` being
    the only ``Missing`` object, so never create another one.

    Examples:

      * ``True`` is expected on ``MISSING``, as it was not supplied:

        >>> is_missing(MISSING)
        True

      * ``False`` is expected on ``None``, as ``None`` is a supplied value:

        >>> is_missing(None)
        False

      * ``False`` is expected on falsy values, as they are supplied values too:

        >>> any(is_missing(_obj) for _obj in (0, '', 0.0, False, 0j, b'', [], {}, set()))
        False

      * ``False`` is expected on truthy values:

        >>> any(is_missing(_obj) for _obj in (2, 'a', 2.5, True, 1+0j, b'y', [1], {1: 'a'}, {2.5}))
        False

      * ``False`` is expected on the other sentinel, as ``UNSET`` was supplied:

        >>> is_missing(UNSET)
        False

    :param obj: object to check.
    :return: ``True`` if ``obj`` is ``MISSING``, ``False`` otherwise.
    """
    return obj is MISSING


def is_unset(obj: object) -> TypeIs[Unset]:
    """
    Check whether ``obj`` is ``UNSET``, i.e. the caller deliberately unset an already set value.

    Type checkers narrow ``obj`` on both branches: to ``Unset`` when this returns ``True``, and to the rest of its
    declared type (e.g. ``str`` from ``str | Unset``) when it returns ``False``. That relies on ``UNSET`` being the
    only ``Unset`` object, so never create another one.

    Examples:

      * ``True`` is expected on ``UNSET``, as the caller deliberately unset the value:

        >>> is_unset(UNSET)
        True

      * ``False`` is expected on ``None``, as ``None`` is a supplied value:

        >>> is_unset(None)
        False

      * ``False`` is expected on falsy values, as they are supplied values too:

        >>> any(is_unset(_obj) for _obj in (0, '', 0.0, False, 0j, b'', [], {}, set()))
        False

      * ``False`` is expected on truthy values:

        >>> any(is_unset(_obj) for _obj in (2, 'a', 2.5, True, 1+0j, b'y', [1], {1: 'a'}, {2.5}))
        False

      * ``False`` is expected on the other sentinel, as ``MISSING`` does not unset anything:

        >>> is_unset(MISSING)
        False

    :param obj: object to check.
    :return: ``True`` if ``obj`` is ``UNSET``, ``False`` otherwise.
    """
    return obj is UNSET


# Stays a TypeGuard: the type system cannot express "T without the sentinel's type", so a False result tells a type
# checker nothing it can narrow by. Use not_none_not_unset() or not_none_not_missing() to narrow both branches.
def not_none_not_sentinel[T, S](val: T | None, *, sentinel: S) -> TypeGuard[T]:
    """
    Check whether ``val`` is neither ``None`` nor the given ``sentinel``.

    Type checkers narrow ``val`` only when this returns ``True``, and only usefully when the sentinel's type is not
    part of ``val``'s declared type: for ``val: str | None`` it narrows to ``str``, but for ``val: int | None | Unset``
    ``T`` takes in ``Unset`` and the narrowed type is too wide to use. A ``False`` result narrows nothing. For
    ``UNSET`` and ``MISSING``, use ``not_none_not_unset()`` and ``not_none_not_missing()``, which narrow both
    branches.

    Examples:

      * ``True`` is expected on a value, as it is neither ``None`` nor the sentinel:

        >>> not_none_not_sentinel("x", sentinel=UNSET)
        True

      * ``True`` is expected on a falsy value, as only ``None`` and the sentinel are refused:

        >>> not_none_not_sentinel(0, sentinel=UNSET)
        True

      * ``False`` is expected on ``None``:

        >>> not_none_not_sentinel(None, sentinel=UNSET)
        False

      * ``False`` is expected on the sentinel itself:

        >>> not_none_not_sentinel(UNSET, sentinel=UNSET)
        False

    :param val: value to check.
    :param sentinel: the sentinel object that ``val`` must not be.
    :return: ``True`` if ``val`` is neither ``None`` nor ``sentinel``, ``False`` otherwise.
    """
    return val is not None and val is not sentinel


def not_none_not_unset[T](val: T | None | Unset) -> TypeIs[T]:
    """
    Check whether ``val`` is neither ``None`` nor ``UNSET``.

    Type checkers narrow ``val`` on both branches: e.g. for ``val: int | None | Unset``, to ``int`` when this returns
    ``True`` and to ``None | Unset`` when it returns ``False``.

    Examples:

      * ``True`` is expected on a value:

        >>> not_none_not_unset("a")
        True

      * ``True`` is expected on falsy values, as only ``None`` and ``UNSET`` are refused:

        >>> all(not_none_not_unset(_val) for _val in (0, '', False, [], {}, set()))
        True

      * ``False`` is expected on ``None``:

        >>> not_none_not_unset(None)
        False

      * ``False`` is expected on ``UNSET``:

        >>> not_none_not_unset(UNSET)
        False

    :param val: value to check.
    :return: ``True`` if ``val`` is neither ``None`` nor ``UNSET``, ``False`` otherwise.
    """
    return val is not None and val is not UNSET


def not_none_not_missing[T](val: T | None | Missing) -> TypeIs[T]:
    """
    Check whether ``val`` is neither ``None`` nor ``MISSING``.

    Type checkers narrow ``val`` on both branches: e.g. for ``val: str | None | Missing``, to ``str`` when this
    returns ``True`` and to ``None | Missing`` when it returns ``False``.

    Examples:

      * ``True`` is expected on a value:

        >>> not_none_not_missing("b")
        True

      * ``True`` is expected on falsy values, as only ``None`` and ``MISSING`` are refused:

        >>> all(not_none_not_missing(_val) for _val in (0, '', False, [], {}, set()))
        True

      * ``False`` is expected on ``None``:

        >>> not_none_not_missing(None)
        False

      * ``False`` is expected on ``MISSING``:

        >>> not_none_not_missing(MISSING)
        False

    :param val: value to check.
    :return: ``True`` if ``val`` is neither ``None`` nor ``MISSING``, ``False`` otherwise.
    """
    return val is not None and val is not MISSING


def _alt_if_predicate_true[T, U](
    obj: Any | U, alt: T, predicate: Callable[[Any | U], bool]
) -> T:
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
    if type(obj) is not type(alt):
        raise TypeError(
            f"Unexpected type: `obj` and `alt` must be of the same type. type(obj): {type(obj)}, "
            f"type(alt): {type(alt)}"
        )
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


def is_ellipses(obj: object) -> TypeIs[EllipsisType]:
    """
    Check whether ``obj`` is the ``...`` (``Ellipsis``) object.

    Type checkers narrow ``obj`` on both branches: to ``EllipsisType`` when this returns ``True``, and to the rest of
    its declared type (e.g. ``int`` from ``int | EllipsisType``) when it returns ``False``.

    Examples:

      * ``True`` is expected on ``...``:

        >>> is_ellipses(...)
        True

      * ``False`` is expected on any other value:

        >>> is_ellipses(1)
        False

      * ``False`` is expected on ``None``, as it is not ``...``:

        >>> is_ellipses(None)
        False

    :param obj: object to check.
    :return: ``True`` if ``obj`` is ``...``, ``False`` otherwise.
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


def fallback_on_none[T](value: T | None, default_val: T | None) -> T | None:
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


# Stays a TypeGuard, never TypeIs: bools are ints, yet this returns False for them. TypeIs[int] would make type
# checkers drop int (and so bool) from the False branch, where True and False actually land.
def strictly_int(value: object) -> TypeGuard[int]:
    """
    Check whether ``value`` is an ``int`` but not a ``bool``.

    ``bool`` is a subclass of ``int``, so ``isinstance(True, int)`` is ``True``. This check refuses bools, for
    arguments that take integers but must not take booleans.

    Type checkers narrow ``value`` to ``int`` only when this returns ``True``. A ``False`` result keeps the declared
    type (e.g. ``int | str`` stays ``int | str``), because a ``bool``, which is an ``int``, may be there.

    Examples:

      * ``True`` is expected on ints, including zero and negatives:

        >>> all(strictly_int(_value) for _value in (5, -10, 0))
        True

      * ``False`` is expected on bools, although they are ints:

        >>> strictly_int(True) or strictly_int(False)
        False

      * ``False`` is expected on values that only look like ints:

        >>> strictly_int(5.0) or strictly_int("5")
        False

      * ``False`` is expected on ``None`` and other objects:

        >>> any(strictly_int(_value) for _value in (None, [1, 2, 3], object()))
        False

    :param value: value to check.
    :return: ``True`` if ``value`` is an ``int`` but not a ``bool``, ``False`` otherwise.
    """
    return isinstance(value, int) and not isinstance(value, bool)


# region positional args related utility methods

# region ensure_atleast_one_arg() and overloads


@overload
def ensure_atleast_one_arg[T](
    first: T | None, *rest: T, falsy: bool = False, enforce_type: None = None
) -> Sequence[T]: ...


@overload
def ensure_atleast_one_arg[T](
    first: object | None,
    *rest: object,
    falsy: bool = False,
    enforce_type: Literal[False] = False,
) -> Sequence[object]: ...


# TODO: check if a Union of types can be enforced in enforce_type. Like, Union[str, Path] or direct `str | Path`
#   or maybe check if an enforce_types list can be added.
@overload
def ensure_atleast_one_arg[T](
    first: T | None, *rest: T, falsy: bool = False, enforce_type: type[T]
) -> Sequence[T]: ...


def ensure_atleast_one_arg[T](
    first: T | object | None,
    *rest: T | object,
    falsy: bool = False,
    enforce_type: type | Literal[False] | None = None,
) -> Sequence[T] | Sequence[object]:
    """
    Ensures that at least one argument is provided (truthy or non-None),
    with optional type enforcement or inference.


    ``enforce_type`` behavior:

      * if not provided, defaults to ``None``. This defaults the method to type check all the arguments to have the same
        type as the first valid argument. Invalidating this condition raises a ``TypeError``.

      * if ``False`` then, no type-enforcement is performed.

      * if a type is provided, like ``str``, ``int`` etc. then all the arguments are enforce to have this same type.
        Invalidating this condition raises a ``TypeError``.

    :param first: First argument (can be None).
    :param rest: Additional arguments.
    :param falsy: Whether to treat falsy values as invalid.
    :param enforce_type: A specific type to enforce across all arguments.

    :returns: A tuple of valid arguments.

    :raises ValueError: If no valid argument is provided.
    :raises TypeError: If enforce_type is given but a mismatch is found.


    Examples::

    >>> ensure_atleast_one_arg("foo", None)
    ('foo',)

    >>> ensure_atleast_one_arg("foo", "bar", enforce_type=str)
    ('foo', 'bar')

    >>> ensure_atleast_one_arg(1, "a", enforce_type=int) # type: ignore[arg-type] # expected int, provided str.
    Traceback (most recent call last):
    TypeError: Expected all arguments to be of type int.

    >>> ensure_atleast_one_arg(1, "a")
    Traceback (most recent call last):
    TypeError: Expected all arguments to be of type int.

    >>> ensure_atleast_one_arg(1, "a", enforce_type=False)
    (1, 'a')

    >>> ensure_atleast_one_arg(None, [], {}, falsy=True)
    Traceback (most recent call last):
    ValueError: At least one argument is required.

    >>> ensure_atleast_one_arg(None, 0, "", enforce_type=False, falsy=True)
    Traceback (most recent call last):
    ValueError: At least one argument is required.

    >>> ensure_atleast_one_arg(None, "hi", 2.3, enforce_type=False)
    ('hi', 2.3)

    >>> ensure_atleast_one_arg(None, "hi", 2.3)
    Traceback (most recent call last):
    TypeError: Expected all arguments to be of type str.

    >>> ensure_atleast_one_arg(None, 123, enforce_type=int)
    (123,)

    >>> ensure_atleast_one_arg(None, 123, enforce_type=str)
    Traceback (most recent call last):
    TypeError: Expected all arguments to be of type str.

    >>> ensure_atleast_one_arg("hi", None, 3.0, falsy=True)
    Traceback (most recent call last):
    TypeError: Expected all arguments to be of type str.

    >>> ensure_atleast_one_arg(None, 'null', 3.0, None, set(), enforce_type=False)
    ('null', 3.0, set())
    """
    values = _filter_args(first, *rest, falsy=falsy)

    if not values:
        raise ValueError("At least one argument is required.")

    if enforce_type is not False:
        expected_type = enforce_type or type(values[0])
        for v in values:
            if not isinstance(v, expected_type):
                raise TypeError(
                    f"Expected all arguments to be of type {expected_type.__name__}."
                )

    return values


# endregion


# region has_atleast_one_arg() and overloads
@overload
def has_atleast_one_arg[T](
    first: T | None, *rest: T, falsy: bool = False, enforce_type: None = None
) -> bool:
    """
    A ``has_atleast_one_arg()`` overload.

    ``first`` and ``rest`` all args must be of the same type when ``enforce_type`` is not provided or is ``None``.
    """
    ...  # pragma: no cover


@overload
def has_atleast_one_arg(
    first: object | None,
    *rest: object,
    falsy: bool = False,
    enforce_type: Literal[False] = False,
) -> bool:
    """
    A ``has_atleast_one_arg()`` overload.

    ``first`` and ``rest`` all args can be of any type when ``enforce_type=False``.
    """
    ...  # pragma: no cover


@overload
def has_atleast_one_arg[T](
    first: T | None, *rest: T, falsy: bool = False, enforce_type: type[T]
) -> bool:
    """
    A ``has_atleast_one_arg()`` overload.

    ``first`` and ``rest`` all args must be of the type provided as ``enforce_type``.

    For example, ``first`` and ``rest`` all args must be ``int`` when ``enforce_type=int``.
    """
    ...  # pragma: no cover


def has_atleast_one_arg(
    first: object | None,
    *rest: object,
    falsy: bool = False,
    enforce_type: type | Literal[False] | None = None,
) -> bool:
    """
    Returns True if there is at least one valid (non-None or truthy) argument,
    optionally enforcing all values are of the same type.

    :param first: First argument (can be None).
    :param rest: Additional arguments.
    :param falsy: Whether to treat falsy values as invalid.
    :param enforce_type: Type to enforce across all arguments.
    :returns: True if valid arguments are found and type checks pass.

    >>> has_atleast_one_arg(None, [])
    True

    >>> has_atleast_one_arg(None, [], falsy=True)
    False

    >>> has_atleast_one_arg("a", "b", enforce_type=str)
    True

    >>> has_atleast_one_arg("a", 1, enforce_type=str) # type: ignore[arg-type] # expected str, provided int.
    False

    >>> has_atleast_one_arg("foo")
    True

    >>> has_atleast_one_arg(None, "bar")
    True

    >>> has_atleast_one_arg(None, None)
    False

    >>> has_atleast_one_arg("", [], 0)
    False

    >>> has_atleast_one_arg("", [], 0, enforce_type=False)
    True

    >>> has_atleast_one_arg("", [], 0, falsy=True)
    False

    >>> has_atleast_one_arg(1, 2, 3, enforce_type=int)
    True

    >>> has_atleast_one_arg(1, "2", enforce_type=int) # type: ignore[arg-type] # expected int, provided str.
    False

    >>> has_atleast_one_arg(1, "2", enforce_type=False)
    True

    >>> has_atleast_one_arg(None, 2.0, enforce_type=int)
    False

    >>> has_atleast_one_arg(None, 2.0, enforce_type=float)
    True

    >>> has_atleast_one_arg(None, "", 0, False, enforce_type=False, falsy=True)
    False

    >>> has_atleast_one_arg("abc", 123)
    False

    >>> has_atleast_one_arg("abc", 123, enforce_type=False)
    True

    >>> has_atleast_one_arg("abc", 123, enforce_type=str) # type: ignore[arg-type] # expected str, provided int.
    False

    >>> has_atleast_one_arg(None, None, None, falsy=True)
    False

    >>> has_atleast_one_arg("a", None, falsy=True)
    True

    >>> has_atleast_one_arg("a", None, enforce_type=str) # type: ignore[arg-type] # expected str, provided None.
    True

    >>> has_atleast_one_arg(None, [1, 2, 3], enforce_type=list)
    True

    >>> has_atleast_one_arg(None, [1, 2, 3], enforce_type=dict)
    False
    """
    return bool(
        _collect_valid_args(first, *rest, falsy=falsy, enforce_type=enforce_type)
    )


# endregion


# region Internal utility functions to handle positional variadic args.
def _filter_args(first, *rest, falsy):
    """
    Examples:

    >>> _filter_args('a', 'b', '', falsy=True)
    ('a', 'b')

    >>> _filter_args('a', 'b', '', falsy=False)
    ('a', 'b', '')

    >>> _filter_args('a', 'b', None, falsy=True)
    ('a', 'b')

    >>> _filter_args('a', 'b', None, falsy=False)
    ('a', 'b')
    """
    args = (first, *rest)
    if falsy:
        return tuple(arg for arg in args if arg)
    else:
        return tuple(arg for arg in args if arg is not None)


def _collect_valid_args(first, *rest, falsy, enforce_type):
    values = _filter_args(first, *rest, falsy=falsy)
    if enforce_type is False:
        return values

    if values:
        expected_type = enforce_type or type(values[0])
        if all(isinstance(v, expected_type) for v in values):
            return values
    return ()


# endregion

# endregion
