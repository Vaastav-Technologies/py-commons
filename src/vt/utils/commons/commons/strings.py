#!/usr/bin/env python3
# coding=utf-8

"""
Reusable interfaces and methods related to strings in python.
"""

import random
import secrets
import string
from collections.abc import Sequence


def generate_random_string(
    length: int = 10, characters: Sequence[str] | None = None, secure: bool = False
) -> str:
    """
    Generates a random/secure string of a specified length using a given set of characters.

    :param length: The desired length of the random string.
    :param characters: A string containing the characters to choose from.
        Defaults to a combination of uppercase letters, lowercase letters, and digits if not provided.
    :param secure: generate cryptographically secure strings.

    :returns: The generated random string.
    """
    if characters is None:
        characters = string.ascii_letters + string.digits
    rand_provider = secrets if secure else random
    return "".join(rand_provider.choice(characters) for _ in range(length))
