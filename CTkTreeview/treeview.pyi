from collections.abc import Callable, Iterable
from contextlib import AbstractContextManager
from tkinter import _ImageSpec, Event
from tkinter.ttk import _TreeviewItemDict
from typing import Any, Literal, overload

from typing_extensions import Self
import customtkinter as ctk

from .types import Anchor, Color, ImageSpec

class Headings(AbstractContextManager):
    def __init__(self, obj: CTkTreeview) -> None:
        ...

    def __enter__(self) -> Self:
        ...

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        ...

    def anchor(self, column: str | int, anchor: Anchor) -> None:
        ...

    @overload
    def command(self, column: str | int, command: str | Callable[[], None]) -> None:
        ...

    @overload
    def command(self, column: str | int) -> str | Callable[[], None]:
        ...

    @overload
    def image(self, column: str | int, image: ImageSpec) -> None:
        ...

    @overload
    def image(self, column: str | int) -> ImageSpec:
        ...

    @overload
    def text(self, column: str | int, text: str) -> None:
        ...

    @overload
    def text(self, column: str | int) -> str:
        ...

class Columns(AbstractContextManager):
    """
    A context manager that sets options for the headings.
    """
    def __init__(self, obj: CTkTreeview) -> None:
        ...

    def __enter__(self) -> Self:
        ...

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        ...

    @overload
    def anchor(self, column: int | str, anchor: Anchor) -> None:
        ...

    @overload
    def anchor(self, column: int | str) -> Anchor:
        ...

    def id(self, column: int | str) -> str:
        ...

    @overload
    def minwidth(self, column: int | str) -> int:
        ...

    @overload
    def minwidth(self, column: int | str, minwidth: int) -> None:
        ...

    @overload
    def width(self, column: int | str) -> int:
        ...

    @overload
    def width(self, column: int | str, width: int) -> None:
        ...

    @overload
    def stretch(self, column: int | str, stretch: bool) -> None:
        ...

    @overload
    def stretch(self, column: int | str) -> bool:
        ...

class CTkTreeview(ctk.CTkFrame):
    """
    A customized treeview widget.

    For the time being, no customizations are done on this
    widget---such changes will be done at a later update.
    """
    _valid_frame_options = ...
    def __init__(
        self,
        master: Any,
        *,
        columns: str | Iterable[str | int],
        displaycolumns: str | int | Iterable[str] | Iterable[int]=...,
        height: int=...,
        selectmode: Literal['browse', 'extended', 'none']=...,
        show: Literal['tree', 'headings', 'tree headings', ''] | Iterable[str]=...,
        bg_color: Color=...,
        border_color: Color | None=...,
        border_width: int | str | None=...,
        corner_radius: int | str | None=...,
        fg_color: Color | None=...,
        width: int=...,
        **kw
    ) -> None:
        ...

    def columns(self) -> Columns:
        ...

    def configure(self, require_redraw=..., **kw) -> None:
        ...

    def headings(self)-> Headings:
        ...

    ## Treeview wrapper methods

    def bbox(
        self,
        item: str | int,
        column: str | int | None=...
    ) -> tuple[int, int, int, int] | Literal['']:
        ...

    def identify_column(self, x: int) -> str:
        ...

    def identify_region(self, x: int, y: int) -> Literal['cell', 'heading', 'nothing', 'separator', 'tree']:
        ...

    @overload
    def item(self, item: str | int, option: Literal["text"]) -> str: ...
    @overload
    def item(self, item: str | int, option: Literal["image"]) -> tuple[str] | Literal[""]: ...
    @overload
    def item(self, item: str | int, option: Literal["values"]) -> tuple[Any, ...] | Literal[""]: ...
    @overload
    def item(self, item: str | int, option: Literal["open"]) -> bool: ...  # actually 0 or 1
    @overload
    def item(self, item: str | int, option: Literal["tags"]) -> tuple[str, ...] | Literal[""]: ...
    @overload
    def item(self, item: str | int, option: str) -> Any: ...
    @overload
    def item(self, item: str | int, option: None = None) -> _TreeviewItemDict: ...
    @overload
    def item(
        self,
        item: str | int,
        option: None = None,
        *,
        text: str = ...,
        image: _ImageSpec = ...,
        values: list[Any] | tuple[Any, ...] | Literal[""] = ...,
        open: bool = ...,
        tags: str | list[str] | tuple[str, ...] = ...,
    ) -> None: ...

    def item(self, item, option=..., **kw) -> None:
        ...

    ## Hooks

    def on_double_clicked(self, event: Event[Self]) -> None:
        ...

    def on_entry_focus_out(self, _event: Event[ctk.CTkEntry], **kw) -> None:
        ...

    def on_entry_enter_pressed(self, _event: Event, **kw) -> None:
        ...
