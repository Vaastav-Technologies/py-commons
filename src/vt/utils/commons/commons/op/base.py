#!/usr/bin/env python3
# coding=utf-8

"""
Reusable interfaces for python projects related to operations.
"""

from __future__ import annotations
from abc import abstractmethod
from pathlib import Path
from typing import Protocol, override, final


class ReversibleOp(Protocol):
    """
    Operation that can be reversed or act in the reversed mode.
    """

    # __always_true = AlwaysTrue()
    # __always_false = AlwaysFalse()

    @property
    @abstractmethod
    def rev(self) -> bool:
        """
        :return: whether current operation is operating in the reverse mode.
        """
        ...  # pragma: no cover

    @staticmethod
    def true() -> AlwaysTrue:
        """
        >>> assert ReversibleOp.true().rev

        :return:
        """
        # TODO: try to return singleton __always_true
        # return ReversibleOp.__always_true
        return AlwaysTrue()

    @staticmethod
    def false() -> AlwaysFalse:
        """
        >>> assert not ReversibleOp.false().rev

        :return:
        """
        # TODO: try to return singleton __always_false
        # return ReversibleOp.__always_false
        return AlwaysFalse()


class AlwaysTrue(ReversibleOp):
    @override
    @property
    def rev(self) -> bool:
        return True


class AlwaysFalse(ReversibleOp):
    @override
    @property
    def rev(self) -> bool:
        return False


# region Root dir related operations
class RootDirOp(Protocol):
    """
    Perform operations on the ``root_dir``.
    """

    @property
    @abstractmethod
    def root_dir(self) -> Path:
        """
        :return: Path to the ``root_dir`` root directory for this operation.
        """
        ...  # pragma: no cover


class CWDRootDirOp(RootDirOp):
    def __init__(self, root_dir=Path.cwd()):
        """
        Perform operations on the root_dir.

        :param root_dir: the path to the root directory.
        """
        self._root_dir = root_dir

    @override
    @property
    def root_dir(self) -> Path:
        return self._root_dir  # pragma: no cover


@final
class RootDirOps:
    """
    A factory-like class for ``RootDirOp``.
    """

    @staticmethod
    def strictly_one_required(
        root_dir: Path | None = None,
        root_dir_op: RootDirOp | None = None,
        *,
        root_dir_str: str = "root_dir",
        root_dir_op_str: str = "root_dir_op",
    ) -> Path:
        """
        Convenience method to raise ``ValueError`` when both ``root_dir`` and ``root_dir_op`` are supplied.

        Examples:

          * OK: only root-dir supplied:

            >>> assert Path.cwd() == RootDirOps.strictly_one_required(Path.cwd())

          * OK: only root-dir-op supplied:

            >>> assert Path('tmp') == RootDirOps.strictly_one_required(root_dir_op=RootDirOps.from_path(Path('tmp')))

          * At least one of ``root_dir`` or ``root_dir_op`` must be provided:

            >>> RootDirOps.strictly_one_required(None, None)
            Traceback (most recent call last):
            ValueError: Either root_dir or root_dir_op is required.

          * Both ``root_dir`` or ``root_dir_op`` cannot be provided:

            >>> RootDirOps.strictly_one_required(root_dir=Path.cwd(), root_dir_op=RootDirOps.from_path(Path('tmp')))
            Traceback (most recent call last):
            ValueError: root_dir and root_dir_op are not allowed together.

        :param root_dir: path to the root directory.
        :param root_dir_op: object that has path to the root directory.
        :param root_dir_str: variable name string for overriding the default ``root_op`` variable name in error
            messages.
        :param root_dir_op_str: variable name string for overriding the default ``root_dir_op`` variable name in error
            messages.
        :raises ValueError: when both ``root_dir`` and ``root_dir_op`` are supplied.
        :return: root dir path.
        """
        if root_dir and root_dir_op:
            raise ValueError(
                f"{root_dir_str} and {root_dir_op_str} are not allowed together."
            )
        if root_dir:
            return root_dir
        if root_dir_op:
            return root_dir_op.root_dir
        raise ValueError(f"Either {root_dir_str} or {root_dir_op_str} is required.")

    @staticmethod
    def from_path(root_dir: Path = Path.cwd()) -> CWDRootDirOp:
        """
        :param root_dir: path to root-dir.
        :return: a root dir operation for the supplied path.
        """
        return CWDRootDirOp(root_dir)


# endregion
