from __future__ import annotations
from tkinter import ttk

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
    frame.pack(fill="both")

    tree = CTkTreeview(frame, columns=["First", "Last", "Age"])
    grid(tree, column=0, row=0)
    app.after(100, lambda: print(app.geometry()))

    app.mainloop()

if __name__ == '__main__':
    main()
