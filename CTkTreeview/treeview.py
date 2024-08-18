from __future__ import annotations
from typing import TYPE_CHECKING


from icecream import ic
import customtkinter as ctk

from .tree_item import TreeColumn, TreeItem, TreeNode
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
        **kw
    ):
        super().__init__(master, **kw)

        self.end_number = 0
        self.tree = TreeItem()

        self.columns: dict[str, TreeColumn] = {}
        self.column_order: list[str] = []

        for cname in columns:
            tc = TreeColumn(self, cname)
            self.columns[cname] = tc
            self.column_order.append(cname)

        self._update_columns()

    def _update_columns(self):
        """
        Update columns and their buttons.
        """
        for i, cname in enumerate(self.column_order):
            self.columnconfigure(i, weight=1)
            tc = self.columns[cname]
            grid(tc.widget, column=i, row=0, sticky="ew", pady=(0, 5))

    def insert(self, parent=None, index="end", values: Any=None, update=True, **kw):
        if (nvalues := len(values)) < (ncols := len(self.columns)):
            raise ValueError(f"Provided values has a length of {nvalues}, needs {ncols}")

        # If no parent is provided, then we default to the root
        if parent is None:
            parent = self.tree
        assert isinstance(parent, TreeItem)

        FIRST_ROW = 1

        if str(index).lower() == "end":
            index = len(parent.items)
        assert isinstance(index, int)

        item = TreeItem(parent)
        row = index if isinstance(index, int) else len(parent.items)
        parent.add_item(item)
        ic(index, row)
        for i, v in enumerate(values):
            bt = ctk.CTkButton(self, text=str(v))
            grid(bt, row=row+FIRST_ROW, column=i, pady=(0, 5))
            node = TreeNode(v, bt)
            item.add_node(node)

        if update:
            self.update()

        return item

if __name__ == '__main__':
    import unittest

    class TestTree(unittest.TestCase):
        def test_thing(self):
            for i in range(3):
                with self.subTest(i=i):
                    item = TreeItem()
                    self.assertEqual(f"Item{i:03}", item.iid)

    unittest.main()
