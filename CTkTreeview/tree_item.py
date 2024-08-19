from __future__ import annotations
from collections.abc import Iterator
from tkinter import ttk
from typing import TYPE_CHECKING
import queue

from attrs import define, field
from icecream import ic
import customtkinter as ctk

if TYPE_CHECKING:
    from typing import Any, Optional, ClassVar, TypeAlias

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
    items: list[TreeItem] = field(factory=list, init=False)
    parent: Optional[TreeItem] = field(init=False, default=None)
    iid: str = ""

    def __iter__(self):
        return TreeItemIterator(self)

    def __attrs_post_init__(self):
        if not self.iid:
            self.iid = f"Item{self.next_id:03}"
            TreeItem.next_id += 1

    def add_node(self, node: TreeNode):
        self.nodes.append(node)
        node.parent = self

    def add_item(self, item: TreeItem):
        self.items.append(item)
        item.parent = self

    def find(self, iid: str) -> TreeItem | None:
        res = None
        for item in self.items:
            if item.iid == iid:
                res = item
            elif item.items:
                res = item.find(iid)

            if res is not None:
                break

        return res

    @property
    def is_root(self) -> bool:
        return self.parent is None

class TreeItemIterator(Iterator[TreeItem]):
    StackType: TypeAlias = queue.SimpleQueue[TreeItem]

    def __init__(self, item: TreeItem):
        self.item = item
        self.x = 0
        self.stack = self._make_stack()

    def _make_stack_recurse(self, stack: StackType, item: TreeItem):
        for item in item.items:
            stack.put_nowait(item)
            if len(item.items) > 0:
                self._make_stack_recurse(stack, item)

    def _make_stack(self):
        stack = self.StackType()
        self._make_stack_recurse(stack, self.item)
        return stack

    def __next__(self) -> TreeItem:
        try:
            return self.stack.get_nowait()
        except queue.Empty:
            raise StopIteration

@define
class TreeNode:
    parent: TreeItem = field(init=False)
    value: Any
    button: ctk.CTkButton
