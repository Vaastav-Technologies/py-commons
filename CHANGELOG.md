# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Date format: YYYY-MM-DD

## [0.0.2.dev0] - 2026-10-30

### Added

- Introduced initial Changelog, with the history of earlier releases.
- `typing_extensions>=4.10` dependency, on Python 3.12 only, for `TypeIs`.

### Changed

- Type checkers now narrow both branches of an `if`/`else` on `is_missing()`, `is_unset()`, `is_ellipses()`,
  `not_none_not_unset()` and `not_none_not_missing()`. For `val: int | Missing`, the `else` branch of
  `if is_missing(val):` is now `int` instead of `int | Missing`.
  - They return `TypeIs` (PEP 742) instead of `TypeGuard` (`bool` for `is_ellipses()`).
- `strictly_int()` and `not_none_not_sentinel()` still return `TypeGuard`, and their docs explain why their `else`
  branch cannot narrow: bools are ints, yet `strictly_int(True)` is `False`.
- Documented that `MISSING` and `UNSET` must stay the only `Missing` and `Unset` objects: never instantiate the
  classes, or the narrowing above becomes wrong.

## [0.0.1.dev11] - 2026-05-25

### Added

- `read_exact(stream, size)` in `core_py`: reads exactly `size` bytes from a binary stream, as a single `.read()`
  may return fewer. Raises `EOFError` if the stream ends first.

## [0.0.1.dev10] - 2026-02-03

### Added

- `match_regexp()` in `strings`: returns the strings from a list that match any of the given compiled regexps.
  A custom match function can replace the default `re.Pattern.match()` check.

## [0.0.1.dev9] - 2025-10-21

### Added

- `lenient` parameter for `last_char_remove()`. `lenient=False` raises `IndexError` on an empty string, which is
  otherwise returned unchanged.

## [0.0.1.dev8] - 2025-10-21

### Added

- `last_char_remove(s, c="\n")` in `strings`: removes the last character of `s` if it is `c`.

## [0.0.1.dev7] - 2025-10-21

### Added

- `ReversibleOp.true()` and `ReversibleOp.false()`: operations whose `rev` is always `True` or always `False`.
- `DoneMarker.true()`, `DoneMarker.false()`, `DoneEnquirer.true()` and `DoneEnquirer.false()`: markers and
  enquirers that always answer `True` or always answer `False`.

## [0.0.1.dev6] - 2025-10-11

Replaces the yanked 0.0.1.dev5, with the same changes.

## [0.0.1.dev5] - 2025-10-11 [YANKED]

### Changed

- `RootDirOps.strictly_one_required()` returns the root directory: `root_dir` if given, else
  `root_dir_op.root_dir`. It used to only validate its arguments.

## [0.0.1.dev4] - 2025-09-22

### Added

- `generate_random_string()` in `strings`: a random string of a given length from a set of characters, letters and
  digits by default. `secure=True` makes it cryptographically secure.

## [0.0.1.dev3] - 2025-09-11

### Added

- `get_first_non_none()` in `collections` and `get_last_non_none()` in `collections.utils`: the first or last
  non-`None` item of a list, or a default.

## [0.0.1.dev2] - 2025-07-01

No user-facing changes.

## [0.0.1.dev1] - 2025-07-01

### Changed

- README: install instructions and usage examples, and badges for the supported Python versions, typing and the
  licence.

## [0.0.1] - 2025-06-30 [YANKED]

First release on PyPI. A typed package (`py.typed`) for Python 3.12+.

### Added

- `core_py`: the `MISSING` and `UNSET` sentinels (`Missing`, `Unset`), with `is_missing()`, `is_unset()`,
  `alt_if_missing()`, `alt_if_unset()`, `not_none_not_missing()`, `not_none_not_unset()` and
  `not_none_not_sentinel()`.
- `core_py`: `is_ellipses()`, `alt_if_ellipses()`, `fallback_on_none()`, `fallback_on_none_strict()`,
  `strictly_int()`, `ensure_atleast_one_arg()` and `has_atleast_one_arg()`.
- `collections`: `get_first_true()` and `get_last_true()`.
- `op`: the `ReversibleOp` and `RootDirOp` interfaces, `CWDRootDirOp`, and the `RootDirOps` factory.
- `state`: the `DoneMarker`, `DoneEnquirer`, `DoneVisitor` and `DelegatingDoneVisitor` interfaces.
- `os`: `is_windows()`, `is_linux()`, `is_mac()`, `is_posix()` and their `not_*()` counterparts.
