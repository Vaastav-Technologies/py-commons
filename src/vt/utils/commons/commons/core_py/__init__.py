#!/usr/bin/env python3
# coding=utf-8

"""
Reusable interfaces related to core python.
"""

# region Base interfaces
from vt.utils.commons.commons.core_py.base import MISSING as MISSING
from vt.utils.commons.commons.core_py.base import Missing as Missing
from vt.utils.commons.commons.core_py.base import UNSET as UNSET
from vt.utils.commons.commons.core_py.base import Unset as Unset
# endregion

# region utility functions
from vt.utils.commons.commons.core_py.utils import (
    has_atleast_one_arg as has_atleast_one_arg,
)
from vt.utils.commons.commons.core_py.utils import (
    ensure_atleast_one_arg as ensure_atleast_one_arg,
)
from vt.utils.commons.commons.core_py.utils import (
    not_none_not_unset as not_none_not_unset,
)
from vt.utils.commons.commons.core_py.utils import is_unset as is_unset
from vt.utils.commons.commons.core_py.utils import alt_if_unset as alt_if_unset
from vt.utils.commons.commons.core_py.utils import alt_if_missing as alt_if_missing
from vt.utils.commons.commons.core_py.utils import is_missing as is_missing
from vt.utils.commons.commons.core_py.utils import alt_if_ellipses as alt_if_ellipses
from vt.utils.commons.commons.core_py.utils import is_ellipses as is_ellipses
from vt.utils.commons.commons.core_py.utils import fallback_on_none as fallback_on_none
from vt.utils.commons.commons.core_py.utils import (
    fallback_on_none_strict as fallback_on_none_strict,
)
from vt.utils.commons.commons.core_py.utils import (
    not_none_not_missing as not_none_not_missing,
)
from vt.utils.commons.commons.core_py.utils import (
    not_none_not_sentinel as not_none_not_sentinel,
)
from vt.utils.commons.commons.core_py.utils import strictly_int as strictly_int
# endregion
