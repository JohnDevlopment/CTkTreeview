from __future__ import annotations
from tkinter import ttk
from typing import TYPE_CHECKING

from attrs import define, field
from icecream import ic
import customtkinter as ctk

if TYPE_CHECKING:
    from typing import Any, Optional, ClassVar

@define
class TreeColumn:
    master: Any
    column_id: str
    text: str = ""
    widget: ctk.CTkButton = field(init=False)

    HEADING_BUTTON_THEME: ClassVar[dict[str, Any]] = {
        'fg_color': ("white", "gray70"),
        'text_color': ("gray30", "black"),
        'hover_color': ("gray80", "gray50"),
        'corner_radius': 0,
        'border_width': 2,
    }

    BUTTON_THEME: ClassVar[dict[str, Any]] = {
        'fg_color': ("white", "gray70"),
        'text_color': ("gray30", "black"),
        'hover_color': ("gray80", "gray50"),
        'corner_radius': 4,
        'border_width': 2,
    }

    def __attrs_post_init__(self):
        if not self.text:
            self.text = self.column_id

        self.widget = ctk.CTkButton(self.master, text=self.text, **self.HEADING_BUTTON_THEME)

@define
class TreeItem:
    next_id: ClassVar = 0
    nodes: list[TreeNode] = field(factory=list, init=False)
    items: list[TreeNode] = field(factory=list, init=False)
    parent: Optional[TreeItem] = None
    iid: str = ""

    def __attrs_post_init__(self):
        if not self.iid:
            self.iid = f"Item{self.next_id:03}"
            TreeItem.next_id += 1

    def add_node(self, node: TreeNode):
        self.nodes.append(node)
        node.parent = self

    @property
    def is_root(self) -> bool:
        return self.parent is None

@define
class TreeNode:
    parent: TreeItem = field(init=False)
    value: Any
    button: ctk.CTkButton
