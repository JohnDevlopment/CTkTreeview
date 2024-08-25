from typing import Any, Iterable, Literal, Optional
from tkinter.ttk import Treeview

import customtkinter as ctk

from .tree_item import TreeNode
from .types import Color

class CTkTreeview(ctk.CTkScrollableFrame):
    def __init__(
        self,
        master: Any,
        columns: Iterable[str],
        *,
        bg_color: Color = ...,
        border_color: Color=...,
        border_width: int | str = ...,
        corner_radius: int | str = ...,
        fg_color: Color = ...,
        height: int = 200,
        highlight_color: Color=...,
        label_anchor: str=...,
        label_fg_color: Color=...,
        label_font: tuple | ctk.CTkFont=...,
        label_text: str=...,
        label_text_color: Color=...,
        orientation: Literal["vertical", "horizontal"]=...,
        scrollbar_button_color: Color=...,
        scrollbar_button_hover_color: Color=...,
        scrollbar_fg_color: Color=...,
        text_color: Color=...,
        width: int = 200
    ):
        ...
