from __future__ import annotations
from typing import TYPE_CHECKING
import sys as _sys

if TYPE_CHECKING:
    from typing import Any

def grid(widget, *args, **kw):
    widget.grid(*args, **kw)

def is_iterable(obj: Any) -> bool:
    try:
        iter(obj)
    except:
        return False
    return True

def error(fmt: str, *args):
    print(fmt % args, file=_sys.stderr)

def pop_kwargs(dct: dict[str, Any], valid_keys: set[str]) -> dict[str, Any]:
    """
    Create a new dict containing the keys in VALID_KEYS.

    The keys in VALID_KEYS are actually removed from DCT.
    """
    ndct: dict[str, Any] = {}
    keys = sorted(dct.keys())

    for k in keys:
        if k in valid_keys:
            if (v := dct.pop(k)) is None:
                continue
            ndct[k] = v

    return ndct

def check_kwargs_empty(dct: dict[str, Any], raise_error: bool=False) -> bool:
    """
    Return true if DCT is empty, false otherwise.

    If RAISE_ERROR is true, ValueError is raised instead of
    returning false.
    """
    keys = list(dct.keys())
    if len(dct) > 0:
        if raise_error:
            raise ValueError(
                f"{keys} are not supported keyword arguments. "
                "Check the documentation for supported arguments."
            )
        return False
    return True
