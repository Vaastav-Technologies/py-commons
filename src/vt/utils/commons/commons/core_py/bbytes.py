# coding=utf-8

"""
bbytes - bits and bytes

All the basic bytes related operations.
"""

from typing import IO


def read_exact(stream: IO[bytes], size: int) -> bytes:
    """
    Read exact sized bytes from the ``stream``.

    ``.read(n)`` reads at-most ``n`` bytes from the stream, which is:
    - faster.
    - unreliable as left out bytes can corrupt next read.

    This function can help read exact ``size`` bytes from the ``stream``.

    :param stream: readable stream to read bytes from.
    :param size: number of bytes to read from the readable stream.
    :return: ``size`` number of bytes from the readable ``stream``.
    """
    chunks: list[bytes] = []
    while size > 0:
        chunk = stream.read(size)
        if not chunk:
            raise EOFError
        chunks.append(chunk)
        size -= len(chunk)
    return b"".join(chunks)
