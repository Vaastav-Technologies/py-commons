#!/usr/bin/env python3
# coding=utf-8

"""
Reusable interfaces for python projects related to operations.
"""
from abc import abstractmethod
from typing import Protocol


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
