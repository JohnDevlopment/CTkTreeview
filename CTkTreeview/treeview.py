from __future__ import annotations
from contextlib import AbstractContextManager
from tkinter import Grid, Pack, Place, ttk
from typing import TYPE_CHECKING, cast, overload
import re
from typing_extensions import reveal_type

from icecream import ic
import customtkinter as ctk

from .utils import grid

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from typing import Any, Literal
    from typing_extensions import Self
    from .types import Anchor, Color, ImageSpec

class _HeadingsContextManager(AbstractContextManager):
    def __init__(self, obj: CTkTreeview) -> None:
        self.obj = obj

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    def anchor(self, column: str | int, anchor: Anchor) -> None:
        """
        Set the anchor argument of column.
        """
        self.obj.heading(column, anchor=anchor)

    def command(self, column: str | int, command: Callable[[], None]) -> None:
        self.obj.heading(column, command=command)

    def image(self, column: str | int, image: ImageSpec) -> None:
        self.obj.heading(column, image=image)

    def text(self, column: str | int, text: str) -> None:
        self.obj.heading(column, text=text)

class _ColumnContextManager(AbstractContextManager):
    def __init__(self, obj: CTkTreeview) -> None:
        self.obj = obj

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    @overload
    def anchor(self, column: int | str, anchor: Anchor) -> None:
        ...

    @overload
    def anchor(self, column: int | str) -> Anchor:
        ...

    def anchor(self, column: int | str, anchor=None):
        if anchor is not None:
            self.obj.column(column, anchor=anchor)
            return

        return cast("Anchor", self.obj.column(column, 'anchor'))

    def id(self, column: int | str) -> str:
        return self.obj.column(column, 'id')

    @overload
    def minwidth(self, column: int | str) -> int:
        ...

    @overload
    def minwidth(self, column: int | str, minwidth: int) -> None:
        ...

    def minwidth(self, column: int | str, minwidth=None):
        if minwidth is not None:
            self.obj.column(column, minwidth=minwidth)
            return

        return self.obj.column(column, 'minwidth')

    @overload
    def width(self, column: int | str) -> int:
        ...

    @overload
    def width(self, column: int | str, width: int) -> None:
        ...

    def width(self, column: int | str, width=None):
        if width is not None:
            self.obj.column(column, width=width)
            return

        return self.obj.column(column, 'width')

    @overload
    def stretch(self, column: int | str, stretch: bool) -> None:
        ...

    @overload
    def stretch(self, column: int | str) -> bool:
        ...

    def stretch(self, column: int | str, stretch=None):
        if stretch is not None:
            self.obj.column(column, stretch=stretch)
            return
        return self.obj.column(column, 'stretch')

class CTkTreeview(ttk.Treeview):
    def __init__(
        self,
        master: Any,
        *,
        columns: str | Iterable[str | int],
        corner_radius: int | None=None,
        displaycolumns: str | int | Iterable[str] | Iterable[int]=("#all",),
        fg_color: Color | None=None,
        height: int=25,
        # TODO: Name?
        selectmode: Literal['browse', 'extended', 'none']="extended",
        show: Literal['tree', 'headings', 'tree headings', ''] | Iterable[str]=("tree", "headings"),
        width: int=200,
        **kw
    ):
        self.frame = ctk.CTkFrame(master, width=width+20)

        # Treeview
        super().__init__(self.frame, height=height,
                         columns=cast("Any", columns), selectmode=selectmode, **kw)
        grid(self, row=0, column=0, sticky="nsew")

        self.selectmode = selectmode

        # Scrollbar
        self.scrollbar = ctk.CTkScrollbar(
            self.frame,
            orientation="vertical",
            command=self.yview
        )
        grid(self.scrollbar, row=0, column=1, sticky='ns')

        self.configure(yscrollcommand=self.scrollbar.set)

        # Override the grid, pack, and place methods to point to the parent frame
        treeview_methods = vars(ttk.Treeview)
        pack_methods = vars(Grid).keys() | vars(Pack).keys() | vars(Place).keys()
        pack_methods = pack_methods.difference(treeview_methods)
        for m in pack_methods:
            if m[0] != "_" and m != "config" and m != "configure":
                setattr(self, m, getattr(self.frame, m))

        # TODO: Bind double-click method

    def columns(self):
        return _ColumnContextManager(self)

    def headings(self):
        return _HeadingsContextManager(self)
