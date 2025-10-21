# vt-commons

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/vt-commons)
![PyPI - Types](https://img.shields.io/pypi/types/vt-commons)
![GitHub License](https://img.shields.io/github/license/Vaastav-Technologies/py-commons)
[![🔧 test](https://github.com/Vaastav-Technologies/py-commons/actions/workflows/test.yml/badge.svg)](https://github.com/Vaastav-Technologies/py-commons/actions/workflows/test.yml)
[![💡 typecheck](https://github.com/Vaastav-Technologies/py-commons/actions/workflows/typecheck.yml/badge.svg)](https://github.com/Vaastav-Technologies/py-commons/actions/workflows/typecheck.yml)
[![🛠️ lint](https://github.com/Vaastav-Technologies/py-commons/actions/workflows/lint.yml/badge.svg)](https://github.com/Vaastav-Technologies/py-commons/actions/workflows/lint.yml)
[![📊 coverage](https://codecov.io/gh/Vaastav-Technologies/py-commons/branch/main/graph/badge.svg)](https://codecov.io/gh/Vaastav-Technologies/py-commons)
[![📤 Upload Python Package](https://github.com/Vaastav-Technologies/py-commons/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Vaastav-Technologies/py-commons/actions/workflows/python-publish.yml)
![PyPI - Version](https://img.shields.io/pypi/v/vt-commons)

---

**🔥Reusable common utilities, interfaces and implementations for python projects.**

---
A fully typed library for common methods, utils, interfaces and implementations for python projects.

### Install

  ```shell
    pip install vt-commons
  ```

#### Usage examples

- Check for OS
    ```python
  from vt.utils.commons.commons.os import is_windows

  windows = is_windows()
    ```
    Check in `vt.utils.commons.commons.os` and documentation for more functions and utilities related to OS.


- Perform some operation on a root directory
    ```python
  from vt.utils.commons.commons.op import RootDirOp, CWDRootDirOp, RootDirOps
  from pathlib import Path
  from typing import override

  class MyRootDirectoryOperation(RootDirOp):
    ...

    @override
    @property
    def root_dir(self)-> Path:
        return Path('path', 'to', 'my', 'root-directory')

  certain_root_dir_operation: CWDRootDirOp = RootDirOps.from_path(Path('path', 'to', 'my', 'root-directory'))
    ```
    Check in `vt.utils.commons.commons.op` and documentation for more functions and utilities related to operations.


- Perform state operations
    ```python
  from vt.utils.commons.commons.state import DoneMarker
  from typing import override

  # Track state by marking done
  class MyStateManager(DoneMarker[int]):
    def __init__(self, *args, **kwargs):
        self.id_state = {1: False}
        ...
    
    @override
    def mark_done(self, _id: int)-> bool:
        # mark done for _id
        if self.id_state[_id] is True:
            return False
        self.id_state[_id] = True
        return True
    ```
    Check in `vt.utils.commons.commons.state` and documentation for more functions and utilities related to tracking state.


- Check if a value is `MISSING`
    ```python
  from vt.utils.commons.commons.core_py import MISSING, Missing, is_missing

  def some_operation(arg: Missing = MISSING):
    """
    ``MISSING`` can be used as a default value sentinel when ``None`` is a valid value for arg.
    """
    arg = 10 if is_missing(arg) else arg
    ...
    ```
    Check in `vt.utils.commons.commons.core_py` and documentation for more functions and utilities related to function management.


- Query and operate on iterables
    ```python
  >>> from vt.utils.commons.commons.collections import get_first_true, get_first_non_none

  >>> assert 3 == get_first_true([1, 3, 5, 7, 2, 1], 8, lambda x: x>2)
  >>> assert 10 == get_first_non_none([None, None, 10, 2, 6], 9)

    ```
    Check in `vt.utils.commons.commons.collections` and documentation for more functions and utilities related to collection management.

- String operations
    ```python
  >>> from vt.utils.commons.commons.strings import generate_random_string
  
  >>> generate_random_string()  #doctest: +ELLIPSIS
  '...'

    ```
    Check in `vt.utils.commons.commons.string` and documentation for more functions and utilities related to strings


### Contribute

Want to contribute?

Checkout [Guidelines for contributions](CONTRIBUTING.md).
