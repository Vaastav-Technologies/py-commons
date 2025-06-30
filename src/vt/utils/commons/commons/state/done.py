#!/usr/bin/env python3
# coding=utf-8

"""
Reusable common utilities, interfaces and implementations for python projects related to states and state variables
marking and enquiring ``done`` state.
"""

from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol, override

from vt.utils.commons.commons.collections import get_first_true, get_last_true


class DoneMarker[T](Protocol):
    """
    Interface to facilitate marking as operation as ``done``.
    """

    @abstractmethod
    def mark_done(self, _id: T) -> bool:
        """
        Mark an ``_id`` as ``done`` in the system. Returns ``True`` when ``_id`` is marked ``done`` to represent a
        logical truthy and done state.

        :param _id: any id.
        :return: ``True`` if marking is done, ``False`` if marking is not to be done for a dry-run or if ``_id``
            is already marked done.
        :raise Exception: on underlying system error.
        """
        ...


class DoneEnquirer[T](Protocol):
    """
    Interface to facilitate checkin whether an operation is marked as ``done``.
    """

    @abstractmethod
    def is_done(self, _id: T) -> bool:
        """
        Check whether the supplied ``_id`` is marked ``done`` in the system. Returns ``True`` when ``_id`` is marked
        ``done`` to represent a logical truthy and done state.

        :param _id: any id.
        :return: ``True`` if marking is done, ``False`` if marking is not done.
        :raise Exception: on underlying system error.
        """
        ...

    def get_first_done(self, ids: Sequence[T], default_val: T) -> T:
        """
        Get the first id which is marked as ``done`` else get the ``default_val``.

        Examples:

          * Doctest setup:
            >>> from typing import Any
            >>> class AlwaysDone(DoneEnquirer[Any]):
            ...     def __init__(self, marking: bool):
            ...         self.marking = marking
            ...
            ...     def is_done(self, _id: Any) -> bool:
            ...         return self.marking

        * First id is returned if all are marked done::

            >>> AlwaysDone(True).get_first_done([1, 2, 3], -1)
            1

        * Default id is returned if none are marked done::

            >>> AlwaysDone(False).get_first_done([1, 2, 3], -1)
            -1

        :param ids: sequence of id(s) from which the first ever ``done`` id is to be found.
        :param default_val: value returned if no id is marked as ``done`` from the ``ids`` list.
        :return: the first id from the list of ``ids`` which is marked ``done`` by the ``done_enquirer`` or
            ``default_val`` if no id was identified as ``done``.
        """
        return get_first_true(ids, default_val, self.is_done)

    def get_last_done(self, ids: Sequence[T], default_val: T) -> T:
        """
        Get the last id which is marked as ``done`` else get the ``default_val``.

        Examples:

          * Doctest setup:

            >>> from typing import Any
            >>> class AlwaysDone(DoneEnquirer[Any]):
            ...     def __init__(self, marking: bool):
            ...         self.marking = marking
            ...
            ...     def is_done(self, _id: Any) -> bool:
            ...         return self.marking

        * Last id is returned if all are marked done::

            >>> AlwaysDone(True).get_last_done([1, 2, 3], -1)
            3

        * Default id is returned if none are marked done::

            >>> AlwaysDone(False).get_last_done([1, 2, 3], -1)
            -1

        :param ids: sequence of id(s) from which the last ``done`` id is to be found.
        :param default_val: value returned if no id is marked as ``done`` from the ``ids`` list.
        :return: the last id from the list of ``ids`` which is marked ``done`` by the ``done_enquirer`` or
            ``default_val`` if no id was identified as ``done``.
        """
        return get_last_true(ids, default_val, self.is_done)


class DoneVisitor[T](DoneMarker[T], DoneEnquirer[T], Protocol):
    """
    Interface for:

    * Marking the operation as done. Supplied by ``DoneMarker``.
    * Checking whether an operation is marked as done. Supplied by ``DoneEnquirer``.
    """

    pass


class DelegatingDoneVisitor[T](DoneVisitor[T], Protocol):
    """
    A ``DoneVisitor`` that stores references to the supplied ``DoneMarker`` and ``DoneEnquirer``.

    Created to facilitate composition over inheritance and hence each of its components, i.e.:

    * ``done_marker``
    * ``done_enquirer``

    Can be initialised at runtime.
    """

    @property
    @abstractmethod
    def done_marker(self) -> DoneMarker[T]:
        """
        :return: stored ``DoneMarker``.
        """
        ...

    @property
    @abstractmethod
    def done_enquirer(self) -> DoneEnquirer[T]:
        """
        :return: stored ``DoneEnquirer``.
        """
        ...

    @override
    def mark_done(self, _id: T) -> bool:
        return self.done_marker.mark_done(_id)

    @override
    def is_done(self, _id: T) -> bool:
        return self.done_enquirer.is_done(_id)
