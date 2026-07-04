from __future__ import annotations

from _tkinter import Tcl_Obj
from tkinter import Image, Misc
from tkinter.font import Font
from typing import TYPE_CHECKING, Any, Literal, TypedDict, type_check_only

if TYPE_CHECKING:
    from typing import TypeAlias

Anchor: TypeAlias = Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"]

Color: TypeAlias = str | tuple[str, str]

FontDescription: TypeAlias = (
    str
    | Font
    | list[Any]
    | tuple[str]
    | tuple[str, int]
    | tuple[str, int, str]
    | tuple[str, int, list[str] | tuple[str, ...]]
    | Tcl_Obj
)

ImageSpec: TypeAlias = Image | str

ScreenUnits: TypeAlias = str | float

Padding: TypeAlias = (
    ScreenUnits
    | tuple[ScreenUnits]
    | tuple[ScreenUnits, ScreenUnits]
    | tuple[ScreenUnits, ScreenUnits, ScreenUnits]
    | tuple[ScreenUnits, ScreenUnits, ScreenUnits, ScreenUnits]
)
