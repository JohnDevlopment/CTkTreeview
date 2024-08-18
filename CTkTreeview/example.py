from __future__ import annotations
from tkinter import ttk

from attrs import define, field
from icecream import ic
import customtkinter as ctk

from .treeview import CTkTreeview
from .utils import grid

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional

def main():
    app = ctk.CTk()
    app.title("CTkTreeview Example")
    frame = ctk.CTkFrame(app, width=500)
    frame.pack(fill="both", expand=True)

    tree = CTkTreeview(frame, ["First", "Last", "Age"], width=400, height=500)
    tree.insert(values=("John", "Smith", 30))
    tree.insert(values=("Jane", "Doe", 27))
    grid(tree, sticky="snew")

    def _toggle_mode_function():
        mode = "light"

        def toggle_mode():
            nonlocal mode
            mode = "dark" if mode == "light" else "light"
            ctk.set_appearance_mode(mode)

        return toggle_mode

    grid(
         ctk.CTkButton(frame, text="Toggle Appearence Mode", command=_toggle_mode_function())
    )

    app.mainloop()

# def main():
#     app = ctk.CTk()
#     tree =ttk.Treeview(
#         app,
#         columns=["First", "Last", "Age"]
#     )
#     tree.column("#0", width=50)
#     tree.heading("First", text="First")
#     tree.heading("Last", text="Last")
#     tree.heading("Age", text="Age")
#     tree.grid(row=0, column=0)

#     def tree_insert(parent: str, values: list[Any] | tuple[Any, ...]):
#         return tree.insert(parent, "end", values=values)

#     item = tree_insert("", ("John", "Russell", "30"))
#     tree_insert(
#         tree_insert(item, ("Bob", "Joe", "26")),
#         ("Joe", "Bob", "25")
#     )

#     app.mainloop()
