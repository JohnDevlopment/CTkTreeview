from __future__ import annotations
from contextlib import AbstractContextManager
from tkinter import Grid, Pack, Place, ttk
from typing import TYPE_CHECKING, cast, overload
import re

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
        # Treeview options
        columns: str | Iterable[str | int],
        displaycolumns: str | int | Iterable[str] | Iterable[int]=("#all",),
        fg_color: Color | None=None,
        height: int=25,
        selectmode: Literal['browse', 'extended', 'none']="extended",
        show: Literal['tree', 'headings', 'tree headings', ''] | Iterable[str]=("tree", "headings"),

        # Frame options
        bg_color: Color="transparent",
        border_color: Color | None=None,
        border_width: int | str | None=None,
        corner_radius: int | str | None=None,
        width: int=200,
        **kw
    ):
        # Frame options
        self.frame = ctk.CTkFrame(master)

        # Treeview
        super().__init__(self.frame, height=height,
                         columns=cast("Any", columns), **kw)
        grid(self, row=0, column=0, sticky="nsew")

        # Scrollbar
        self.scrollbar = ctk.CTkScrollbar(
            self.frame,
            orientation="vertical",
            command=self.yview
        )
        grid(self.scrollbar, row=0, column=1, sticky='ns')

        # Pass init keywords into configure()
        self.configure(
            True,
            # Tree
            displaycolumns=displaycolumns,
            fg_color=fg_color,
            height=height,
            selectmode=selectmode,
            show=show,
            yscrollcommand=self.scrollbar.set,

            # Frame
            bg_color=bg_color,
            border_color=border_color,
            border_width=border_width,
            corner_radius=corner_radius,
            width=width,
            **kw
        )

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

    def configure(self, require_redraw=False, **kw):
        # Frame options
        INT_PROP_PATTERN = re.compile(r'border_width|corner_radius|height|width')
        frame_options = {}

        for k in ['background_corner_colors', 'bg_color', 'border_color',
                  'border_width', 'fg_color', 'corner_radius', 'height', 'width']:
            if k in kw:
                # These options are not added if they are None
                if (v := kw.pop(k)) is not None:
                    frame_options[k] = v
        for k in ['overwrite_preferred_drawing_method']:
            if k in kw:
                v = kw.pop(k)
                if INT_PROP_PATTERN.match(k) and v is None:
                    continue

                frame_options[k] = v

        # Our options
        options = {}

        if 'displaycolumns' in kw:
            self.displaycolumns = cast(bool, kw.pop('displaycolumns'))
            options['displaycolumns'] = self.displaycolumns

        if 'fg_color' in kw:
            self.fg_color = cast(Color, kw.pop('fg_color'))
            options['fg_color'] = self.fg_color

        if 'height' in kw:
            self.height = cast(int, kw.pop('height'))
            options['height'] = self.height

        if 'selectmode' in kw:
            self.selectmode = cast("Literal['browse', 'extended', 'none']",
                kw.pop('selectmode'))
            options['selectmode'] = self.selectmode

        if 'show' in kw:
            self.show = cast("Literal['tree', 'headings', 'tree headings', ''] | Iterable[str]",
                kw.pop('show'))
            options['show'] = self.show

        if 'yscrollcommand' in kw:
            self.yscrollcommand = cast("Callable[[float, float], None]", kw.pop('yscrollcommand'))
            options['yscrollcommand'] = self.yscrollcommand

        kw.update(options)

        self.frame.configure(require_redraw, **frame_options)
        super().configure(**kw)

    def headings(self):
        return _HeadingsContextManager(self)
