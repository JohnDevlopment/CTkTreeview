from __future__ import annotations

import customtkinter as ctk

from .treeview import CTkTreeview
from .utils import grid


def main():
    app = ctk.CTk()
    app.title("CTkTreeview Example")
    frame = ctk.CTkFrame(app, width=500)
    frame.pack(fill="both")

    tree = CTkTreeview(frame, columns=["File", "Date"])
    grid(tree, column=0, row=0)
    app.after(100, lambda: print(app.geometry()))

    with tree.headings() as th:
        th.text("File", "File")
        th.text("Date", "Date Added")

    app.mainloop()


if __name__ == "__main__":
    main()
