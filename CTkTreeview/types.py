"""
Type aliases for use with other modules.
"""
from __future__ import annotations
from _tkinter import Tcl_Obj
from tkinter import Image
from tkinter.font import Font
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from typing import TypeAlias

#: For ``anchor=`` arguments in methods. The following values
#: are valid:
#: * nw (northwest)
#: * n (north)
#: * ne (northeast)
#: * w (west)
#: * center
#: * e (east)
#: * sw (southwest)
#: * s (south)
#: * se (southeast)
Anchor: TypeAlias = Literal['nw', 'n', 'ne', 'w', 'center', 'e', 'sw', 's', 'se']

#: Color description. The tuple version describes the colors
#: for light mode and dark mode; in the case of a single
#: string, both light and dark mode.
Color: TypeAlias = str | tuple[str, str]

#: For ``font=`` arguments in methods.
FontDescription: TypeAlias = (str | Font | list[Any] | tuple[str] | tuple[str, int] |
    tuple[str, int, str] | tuple[str, int, list[str] | tuple[str, ...]] | Tcl_Obj)

#: For ``image=`` arguments in methods.
ImageSpec: TypeAlias = Image | str

#: Screen units (i.e., )
ScreenUnits: TypeAlias = str | float

Padding: TypeAlias = (
    ScreenUnits
    | tuple[ScreenUnits]
    | tuple[ScreenUnits, ScreenUnits]
    | tuple[ScreenUnits, ScreenUnits, ScreenUnits]
    | tuple[ScreenUnits, ScreenUnits, ScreenUnits, ScreenUnits]
)
