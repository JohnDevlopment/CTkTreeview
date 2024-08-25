from __future__ import annotations
from tkinter.ttk import Treeview
from typing import TYPE_CHECKING, cast

from icecream import ic
import customtkinter as ctk

class CTkTreeview(Treeview):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        # TODO:
