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

    @property
    @abstractmethod
    def rev(self) -> bool:
        """
        :return: whether current operation is operating in the reverse mode.
        """
        ...


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
        ...


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
        return self._root_dir


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
    ):
        """
        Convenience method to raise ``ValueError`` when both ``root_dir`` and ``root_dir_op`` are supplied.

        Examples:

          * OK: only root-dir supplied:

            >>> RootDirOps.strictly_one_required(Path.cwd())

          * OK: only root-dir-op supplied:

            >>> RootDirOps.strictly_one_required(root_dir_op=RootDirOps.from_path(Path('tmp')))

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
        """
        if root_dir is None and root_dir_op is None:
            raise ValueError(f"Either {root_dir_str} or {root_dir_op_str} is required.")
        if root_dir and root_dir_op:
            raise ValueError(
                f"{root_dir_str} and {root_dir_op_str} are not allowed together."
            )

    @staticmethod
    def from_path(root_dir: Path = Path.cwd()) -> CWDRootDirOp:
        """
        :param root_dir: path to root-dir.
        :return: a root dir operation for the supplied path.
        """
        return CWDRootDirOp(root_dir)


# endregion
