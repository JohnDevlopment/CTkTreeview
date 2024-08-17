from __future__ import annotations
from typing import TYPE_CHECKING

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
