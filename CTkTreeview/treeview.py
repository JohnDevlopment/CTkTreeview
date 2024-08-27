from __future__ import annotations
from tkinter import Grid, Pack, Place, ttk
from typing import TYPE_CHECKING, cast
import re

from icecream import ic
import customtkinter as ctk

from .utils import grid

if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import Any, Literal
    from .types import Color

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
