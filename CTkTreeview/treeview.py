from __future__ import annotations
from typing import TYPE_CHECKING, cast

from icecream import ic
import customtkinter as ctk

from .tree_item import TreeColumn, TreeItem, TreeNode
from .types import Color
from .utils import grid

if TYPE_CHECKING:
    from typing import Any, Iterable

# from tkinter import ttk
# ttk.Treeview

class CTkTreeview(ctk.CTkScrollableFrame):
    def __init__(
        self,
        master,
        columns: Iterable[str],
        button_color="default",
        highlight_color="default",
        hover=True,
        hover_color="default",
        text_color="default",
        **kw
    ):
        super().__init__(master, **kw)

        # Button fg color
        self.button_fg_color = (
            "transparent" if button_color == "default"
            else button_color
        )
        self.button_fg_color = cast(Color, self.button_fg_color)

        # Button text color
        self.text_color = (
            ctk.ThemeManager.theme["CTkLabel"]["text_color"]
            if text_color == "default"
            else text_color
        )

        # Button selection color
        self.select_color: Color = (
            ctk.ThemeManager.theme['CTkButton']['fg_color']
            if highlight_color == "default"
            else highlight_color
        )
        self.select_color = cast(Color, self.select_color)

        # Button selection color: based on 'button_fg_color'
        self.hover_color: Color = (
            ctk.ThemeManager.theme['CTkButton']['hover_color']
            if hover_color == "default"
            else hover_color
        )
        self.hover_color = cast(Color, self.hover_color)

        self.end_number = 0
        self.tree = TreeItem()
        self.selected_item: TreeItem | None = None

        self.columns: dict[str, TreeColumn] = {}
        self.column_order: list[str] = []

        for cname in columns:
            tc = TreeColumn(self, cname)
            self.columns[cname] = tc
            self.column_order.append(cname)

        self.hover = hover

        self._update_columns()

    def _update_columns(self):
        """
        Update columns and their buttons.
        """
        for i, cname in enumerate(self.column_order):
            self.columnconfigure(i, weight=1)
            tc = self.columns[cname]
            grid(tc.widget, column=i, row=0, sticky="ew", pady=(0, 5))

    def select(self, item):
        # Locate item
        item = self.tree.find(item)
        if item is None:
            return

        # Reset all buttons to their default bg
        for subitem in self.tree:
            for node in subitem.nodes:
                node.button.configure(fg_color=self.button_fg_color, hover=self.hover)

        self.selected_item = item

        buttons = [node.button for node in item.nodes]

        for button in buttons:
            button.configure(fg_color=self.select_color, hover=False)

        # TODO: Add multiple selection

        def _hover():
            for button in buttons:
                button.configure(hover=self.hover)
        self.after(100, _hover)

        self.event_generate("<<TreeviewSelect>>")

    def insert(self, parent=None, index="end", values: Any=None, update=True, **kw):
        if (nvalues := len(values)) < (ncols := len(self.columns)):
            raise ValueError(f"Provided values has a length of {nvalues}, needs {ncols}")

        # If no parent is provided, then we default to the root
        if parent is None:
            parent = self.tree
        else:
            old_parent = parent
            parent = self.tree.find(parent)
            if parent is None:
                raise ValueError(f"Invalid item {old_parent!r}")
        assert isinstance(parent, TreeItem)

        FIRST_ROW = 1

        # INDEX can be "end" or an integer
        if str(index).lower() == "end":
            index = -1
        elif not isinstance(index, int):
            raise TypeError(f"Invalid index {index!r}, must be 'end' or an integer")

        index = cast(int, index)

        # Create tree item and add to parent
        item = TreeItem()
        parent.add_item(item)
        # TODO: If INDEX is >= 0, insert into the item (not append)

        row = len(parent.items) if index < 0 else index

        ic(index, row)
        for i, v in enumerate(values):
            # TODO: When the user clicks one of these buttons, "select" the item
            bt = ctk.CTkButton(
                self,
                text=str(v),
                fg_color=self.button_fg_color,
                hover_color=self.hover_color,
                text_color=self.text_color
            )
            grid(bt, row=row+FIRST_ROW, column=i, pady=(0, 5))
            node = TreeNode(v, bt)
            item.add_node(node)

        if update:
            self.update()

        return item.iid

if __name__ == '__main__':
    import unittest

    class TestTree(unittest.TestCase):
        def test_thing(self):
            for i in range(3):
                with self.subTest(i=i):
                    item = TreeItem()
                    self.assertEqual(f"Item{i:03}", item.iid)

    unittest.main()
