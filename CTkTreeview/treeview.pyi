from typing import Any, Iterable, Literal, Optional
import customtkinter as ctk

from .tree_item import TreeNode

class CTkTreeview(ctk.CTkScrollableFrame):
    def __init__(
        self,
        master: Any,
        columns: Iterable[str],
        bg_color: str | tuple[str, str] = ...,
        border_color: str | tuple[str, str]=...,
        border_width: int | str = ...,
        corner_radius: int | str = ...,
        fg_color: str | tuple[str, str] = ...,
        height: int = 200,
        label_anchor: str=...,
        label_fg_color: str | tuple[str, str]=...,
        label_font: tuple | ctk.CTkFont=...,
        label_text: str=...,
        label_text_color: str | tuple[str, str]=...,
        orientation: Literal["vertical", "horizontal"]=...,
        scrollbar_button_color: str | tuple[str, str]=...,
        scrollbar_button_hover_color: str | tuple[str, str]=...,
        scrollbar_fg_color: str | tuple[str, str]=...,
        width: int = 200
    ):
        ...

    def insert(
        self,
        parent: TreeNode=...,
        index: str | int=...,
        values: Any=None,
        **kw
    ):
        ...
