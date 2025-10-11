#!/usr/bin/env python3
# coding=utf-8

"""
Reusable common utilities for python projects related to collections.
"""

from collections.abc import Sequence, Callable, Iterator


def get_first_true[T](
    ids: Sequence[T],
    default_val: T,
    predicate: Callable[[T], bool],
    iter_provider: Callable[[Sequence[T]], Iterator[T]] = iter,
) -> T:
    """
    Get the first id which returns ``True`` from the supplied ``predicate`` else get the ``default_val``.

    Examples:

    * First id is returned if all ``ids`` are inferred as ``True``::

        >>> get_first_true([1, 2, 3], -1, lambda x: True)
        1

    * Default id is returned if no ``ids`` are inferred as ``True``::

        >>> get_first_true([1, 2, 3], -1, lambda x: False)
        -1

    Error scenarios:

    * supplied predicate is not a callable::

        >>> get_first_true([1, 2, 3], -1,
        ...                     object()) # noqa: to avoid typecheck warnings, expects (x)->bool Callable
        Traceback (most recent call last):
        TypeError: predicate must be a (x) -> bool Callable. Supplied <class 'object'>.

    * suppplied predicate is a non-conforming callable::

        >>> get_first_true([1, 2, 3], -1,
        ...                     lambda x, y: True) # noqa: to avoid typecheck warnings, expects (x)->bool Callable.
        Traceback (most recent call last):
        TypeError: <lambda>() missing 1 required positional argument: 'y'

    :param ids: sequence of id(s) from which the first ever ``predicate`` determined truthy id is to be found.
    :param default_val: value returned if no id is found as truthy from the ``ids`` list according to the supplied
        ``predicate``.
    :param predicate: predicate to determine whether an id is inferred as satisfying and hence returning ``True`` for
        that id.
    :param iter_provider: iterator provider for the ``ids`` sequence.
    :return: the first id from the list of ``ids`` which returns ``True`` by the ``predicate`` or ``default_val`` if
        the ``predicate`` returns ``True`` for no id(s).
    """
    if not callable(predicate):
        raise TypeError(
            f"predicate must be a (x) -> bool Callable. Supplied {type(predicate)}."
        )

    for _id in iter_provider(ids):
        if predicate(_id):
            return _id
    return default_val


def get_last_true[T](
    ids: Sequence[T], default_val: T, predicate: Callable[[T], bool]
) -> T:
    """
    Get the last id which returns ``True`` from the supplied ``predicate`` else get the ``default_val``.

    Examples:

    * Last id is returned if all ``ids`` are inferred as ``True``::

        >>> get_last_true([1, 2, 3], -1, lambda x: True)
        3

    * Default id is returned if no ``ids`` are inferred as ``True``::

        >>> get_last_true([1, 2, 3], -1, lambda x: False)
        -1

    Error scenarios:

    * supplied predicate is not a callable::

        >>> get_last_true([1, 2, 3], -1,
        ...                     object()) # noqa: to avoid typecheck warnings, expects (x)->bool Callable
        Traceback (most recent call last):
        TypeError: predicate must be a (x) -> bool Callable. Supplied <class 'object'>.

    * suppplied predicate is a non-conforming callable::

        >>> get_last_true([1, 2, 3], -1,
        ...                     lambda x, y: True) # noqa: to avoid typecheck warnings, expects (x)->bool Callable.
        Traceback (most recent call last):
        TypeError: <lambda>() missing 1 required positional argument: 'y'

    :param ids: sequence of id(s) from which the last ``predicate`` determined truthy id is to be found.
    :param default_val: value returned if no id is found as truthy from the ``ids`` list according to the supplied
        ``predicate``.
    :param predicate: predicate to determine whether an id is inferred as satisfying and hence returning ``True`` for
        that id.
    :return: the last id from the list of ``ids`` which returns ``True`` by the ``predicate`` or ``default_val`` if
        the ``predicate`` returns ``True`` for no id(s).
    """
    return get_first_true(ids, default_val, predicate, reversed)


def get_first_non_none[T](
    lst: list[T | None],
    default: T | None = None,
    iter_provider: Callable[[Sequence[T | None]], Iterator[T | None]] = iter,
) -> T | None:
    """
    Get first non-``None`` item from the list ``lst`` else ``default``.

    Examples:

      * Return the default if all values are ``None``:

        >>> get_first_non_none([None, None, None], 5)
        5

      * default can be ``None``:

        >>> get_first_non_none([None, None], None)

      * first non-``None`` is returned:

        >>> get_first_non_none([None, None, 2, None, 5], 9)
        2

      * default is returned when empty-list is supplied:

        >>> get_first_non_none([], "some str")
        'some str'

        >>> get_first_non_none([], None) # None returned as default is None

        >>> get_first_non_none([]) # None returned as default is None

    :param lst: list of values.
    :param default: value to return if list consists of all ``None``s.
    :param iter_provider: iterator provider for the ``ids`` sequence.
    :return: first non ``None`` value or ``default`` if all ``None`` are encountered.
    """
    return get_first_true(lst, default, lambda x: x is not None, iter_provider)


def get_last_non_none[T](lst: list[T | None], default: T | None = None) -> T | None:
    """
    Get last non-``None`` item from the list ``lst`` else ``default``.

    Examples:

      * Return the default if all values are ``None``:

        >>> get_last_non_none([None, None, None], 5)
        5

      * default can be ``None``:

        >>> get_last_non_none([None, None], None)

      * last non-``None`` is returned:

        >>> get_last_non_none([None, None, 2, None, 5], 9)
        5

      * default is returned when empty-list is supplied:

        >>> get_last_non_none([], "some str")
        'some str'

        >>> get_last_non_none([], None) # None returned as default is None

        >>> get_last_non_none([]) # None returned as default is None

    :param lst: list of values.
    :param default: value to return if list consists of all ``None``s.
    :return: first non ``None`` value or ``default`` if all ``None`` are encountered.
    """
    return get_first_non_none(lst, default, reversed)
