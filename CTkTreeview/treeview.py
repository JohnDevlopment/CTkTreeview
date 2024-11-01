from __future__ import annotations
from contextlib import AbstractContextManager
from tkinter import Event, Grid, Pack, Place, ttk
from typing import TYPE_CHECKING, cast, overload
import functools
import re

import customtkinter as ctk

from .utils import check_kwargs_empty, grid, pop_kwargs

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from typing import Any, Literal
    from typing_extensions import Self
    from .types import Anchor, Color, ImageSpec

class Headings(AbstractContextManager):
    """
    A context manager that sets options for the headings.
    """

    def __init__(self, obj: CTkTreeview):
        self.obj = obj

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    def anchor(self, column: str | int, anchor: Anchor) -> None:
        """
        Set the anchor of a heading.

        :param column: The name or index of a column
        :type column: str or int

        :param str anchor: One of 'nw', 'n' 'ne', 'e', 'se', 's',
                           'sw', 'w'

        :returns: ``None`` if `anchor` is set, otherwise the current
                  anchor of `column`'s heading
        :rtype: str or None
        """
        self.obj.heading(column, anchor=anchor)

    @overload
    def command(self, column: str | int, command: str | Callable[[], None]) -> None:
        ...

    @overload
    def command(self, column: str | int) -> str | Callable[[], None]:
        ...

    def command(self, column: str | int, command: str | Callable[[], None] | None=None):
        """
        Query or set the command of a heading.

        :param column: The name or index of the column
        :type column: str or int

        :param command: The command to be called when the heading is
                        clicked on
        :type command: Callable or None

        :returns: ``None`` if `command` is provided, otherwise the
                  currently set command
        :rtype: None or str or Callable
        """
        if command is not None:
            self.obj.heading(column, command=command)
        else:
            return self.obj.heading(column, 'heading')

    @overload
    def image(self, column: str | int, image: ImageSpec) -> None:
        ...

    @overload
    def image(self, column: str | int) -> tuple[str] | str:
        ...

    def image(self, column: str | int, image: ImageSpec | None=None):
        """
        Query or set a heading's image.

        :param column: String name or index of a column
        :type column: str or int

        :param ImageSpec image: A string name of an image or a
                                ``tkinter.Image``

        :returns: ``None`` if `image` is provided, otherwise the
                  currently set image
        :rtype: tuple[str] or str or None
        """
        if image is not None:
            self.obj.heading(column, image=image)
        else:
            return self.obj.heading(column, 'image')

    @overload
    def text(self, column: str | int, text: str) -> None:
        ...

    @overload
    def text(self, column: str | int) -> str:
        ...

    def text(self, column: str | int, text: str | None=None):
        """
        Query or set the textual label of a heading.

        :param column: String name or index of a column
        :type column: str or int

        :param str text: Textual label of the heading

        :returns: ``None`` if `text` is provided, otherwise the
                  current textual label
        :rtype: str or None
        """
        if text is not None:
            self.obj.heading(column, text=text)
        else:
            return self.obj.heading(column, 'text')

class Columns(AbstractContextManager):
    """
    A context manager that sets options for the headings.
    """

    def __init__(self, obj: CTkTreeview):
        self.obj = obj

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    @overload
    def anchor(self, column: int | str, anchor: Anchor) -> None:
        ...

    @overload
    def anchor(self, column: int | str) -> Anchor:
        ...

    def anchor(self, column: int | str, anchor=None):
        """
        Query or set the anchor of a column.

        :param column: String name or index of a column
        :type column: str or int

        :param str anchor: One of 'nw', 'n' 'ne', 'e', 'se', 's',
                           'sw', or 'w'

        :returns: ``None`` if `anchor` is provided, otherwise one of
                  'nw', 'n' 'ne', 'e', 'se', 's', 'sw', or 'w'
        :rtype: str or None
        """
        if anchor is not None:
            self.obj.column(column, anchor=anchor)
            return

        return cast("Anchor", self.obj.column(column, 'anchor'))

    def id(self, column: int | str) -> str:
        """
        Query the ID of a column.

        :param column: String name or index of a column
        :type column: str or int

        :returns: The ID of `column`
        :rtype: str
        """
        return self.obj.column(column, 'id')

    @overload
    def minwidth(self, column: int | str) -> int:
        ...

    @overload
    def minwidth(self, column: int | str, minwidth: int) -> None:
        ...

    def minwidth(self, column: int | str, minwidth=None):
        """
        Query or set the minimum width of a column.

        :param column: String name or index of a column
        :type column: str or int

        :param int width: The minimum width that `column` should be

        :returns: ``None`` if `column` is provided, otherwise the
                  currently set minimum width of the column
        :rtype: int or None
        """
        if minwidth is not None:
            self.obj.column(column, minwidth=minwidth)
            return

        return self.obj.column(column, 'minwidth')

    @overload
    def width(self, column: int | str) -> int:
        ...

    @overload
    def width(self, column: int | str, width: int) -> None:
        ...

    def width(self, column: int | str, width=None):
        """
        Query or set the width of a column.

        :param column: String name or index of a column
        :type column: str or int

        :param int width: The width of `column`

        :returns: ``None`` if `column` is provided, otherwise the
                  currently set width of the column
        :rtype: int or None
        """
        if width is not None:
            self.obj.column(column, width=width)
            return

        return self.obj.column(column, 'width')

    @overload
    def stretch(self, column: int | str, stretch: bool) -> None:
        ...

    @overload
    def stretch(self, column: int | str) -> bool:
        ...

    def stretch(self, column: int | str, stretch=None):
        """
        Query or set the stretch flag of a column.

        :param column: String name or index of a column
        :type column: str or int

        :param bool stretch: Whether or not the column should
                             stretch when the widget resizes or when
                             the user drags a column separator

        :returns: ``None`` if `stretch` is provided, otherwise
                  ``True`` or ``False`` depending on the current
                  stretch of `column`
        :rtype: bool or None
        """
        if stretch is not None:
            self.obj.column(column, stretch=stretch)
            return

        return self.obj.column(column, 'stretch')

class CTkTreeview(ttk.Treeview):
    def __init__(
        self,
        master: Any,
        *,
        # Treeview options
        columns: str | Iterable[str | int],
        displaycolumns: str | int | Iterable[str] | Iterable[int]=("#all",),
        height: int=25,
        selectmode: Literal['browse', 'extended', 'none']="extended",
        show: Literal['tree', 'headings', 'tree headings', ''] | Iterable[str]=("tree", "headings"),

        # Frame options
        bg_color: Color="transparent",
        border_color: Color | None=None,
        border_width: int | str | None=None,
        corner_radius: int | str | None=None,
        fg_color: Color | None=None,
        width: int=200,
        **kw
    ):
        """
        Initialize a treeview object with a given master.

        :param Any master: The master of this widget

        :keyword columns: A list of data columns. May be a single
                          string to define a single column or a
                          list of strings for multiple columns. The
                          list may also contain integers
        :type columns: str or Iterable[str or int]

        :keyword displaycolumns: The list of columns to display,
                                 and in what order. The columns are
                                 referenced by their symbolic names
                                 (as in `columns`), or their
                                 numerical index into the list
                                 passed in `columns`. If ``"#all"``
                                 or ``("#all",)`` (the default), all
                                 columns are displayed in the order
                                 that they are defined
        :type displaycolumns: str or Iterable[str or int]

        :keyword int height: The widget height in rows

        :keyword str selectmode: Controls how the selection is
                                 handled. Valid modes are
                                 ``browse``, ``extended``, and
                                 ``none``

        :keyword str show: Controls what elements of the tree to
                           display. Values can be ``'tree'``,
                           ``'headings'``, ``tree headings'``, an
                           empty string, or a tuple consisting of
                           any combination of ``'tree'`` and
                           ``'headings'``

        :keyword Color bg_color: Sets the background color of this
                                 widget. But what it really sets is
                                 the background color of the
                                 containing frame. The special value
                                 ``"transparent"`` (the default)
                                 makes the frame transparent

        :keyword border_color: Sets the border color. In reality,
                               this is an option for the containing
                               frame. If omitted or ``None``, the
                               border is not displayed
        :type border_color: Color or None

        :keyword int border_width: Sets the border width. In
                                   reality, this is an option for
                                   the containing frame

        :keyword corder_radius: Currently unused
        :type corder_radius: int or str or None

        :keyword Color fg_color: Sets the forground color. In
                                 reality, this is an option for the
                                 containing frame

        :keyword int width: Sets the width. In reality, this is an
                            option for the containing frame

        Any remaining keyword options are forwarded to
        :py:meth:`tkinter.ttk.Treeview.__init__`.
        """
        # Attributes:tree
        self._columns = columns
        self._displaycolumns = displaycolumns
        self._height = height
        self._selectmode = selectmode
        self._show = show

        # Attributes:frame
        self._bg_color = bg_color
        self._border_color = border_color
        self._border_width = border_width
        self._corner_radius = corner_radius
        self._fg_color = fg_color
        self._width = width

        self.frame = ctk.CTkFrame(master)

        # Treeview
        super().__init__(
            self.frame,
            height=height,
            columns=cast("Any", columns),
            **kw
        )
        # grid(self, row=0, column=0, sticky='ewns')
        self.pack(fill='both', expand=True, side="left")

        # Scrollbar
        self.scrollbar = ctk.CTkScrollbar(
            self.frame,
            orientation="vertical",
            command=self.yview
        )
        # grid(self.scrollbar, row=0, column=1, sticky='ns')
        self.scrollbar.pack(fill='y', expand=True, side="right")

        # Pass init keywords into configure()
        self.configure(
            True,
            # Tree
            displaycolumns=displaycolumns,
            fg_color=fg_color,
            # height=height,
            selectmode=selectmode,
            show=show,
            yscrollcommand=self.scrollbar.set,

            # Frame
            bg_color=bg_color,
            border_color=border_color,
            border_width=border_width,
            corner_radius=corner_radius,
            width=width,
            **kw
        )

        # Override the grid, pack, and place methods to point to the parent frame
        treeview_methods = vars(ttk.Treeview)
        pack_methods = vars(Grid).keys() | vars(Pack).keys() | vars(Place).keys()
        pack_methods = pack_methods.difference(treeview_methods)
        for m in pack_methods:
            if m[0] != "_" and m != "config" and m != "configure":
                setattr(self, m, getattr(self.frame, m))

        self.bind("<Double-1>", self.on_double_clicked, True)

    def columns(self):
        return Columns(self)

    def configure(self, require_redraw=False, **kw):
        # Frame options
        # INT_PROP_PATTERN = re.compile(r'border_width|corner_radius|height|width')
        frame_options = pop_kwargs(kw, self._valid_frame_options)

        # for k in ['background_corner_colors', 'bg_color', 'border_color',
        #           'border_width', 'fg_color', 'corner_radius', 'height', 'width']:
        #     # Specific options are for the frame rather than the treeview
        #     if k in kw:
        #         # These options are not added if they are None
        #         if (v := kw.pop(k)) is not None:
        #             frame_options[k] = v

        # for k in ['overwrite_preferred_drawing_method']:
        #     if k in kw:
        #         v = kw.pop(k)
        #         if INT_PROP_PATTERN.match(k) and v is None:
        #             continue

        #         frame_options[k] = v

        # Our options
        options = {}

        if 'displaycolumns' in kw:
            self.displaycolumns = cast(bool, kw.pop('displaycolumns'))
            options['displaycolumns'] = self.displaycolumns

        if 'fg_color' in kw:
            self._fg_color = cast(Color, kw.pop('fg_color'))
            options['fg_color'] = self._fg_color

        if 'height' in kw:
            self._height = cast("int", kw.pop('height'))
            options['height'] = self._height

        if 'selectmode' in kw:
            self._selectmode = cast("Literal['browse', 'extended', 'none']",
                kw.pop('selectmode'))
            options['selectmode'] = self._selectmode

        if 'show' in kw:
            self._show = cast("Literal['tree', 'headings', 'tree headings', ''] | Iterable[str]",
                kw.pop('show'))
            options['show'] = self._show

        if 'yscrollcommand' in kw:
            self._yscrollcommand = cast("Callable[[float, float], None]", kw.pop('yscrollcommand'))
            options['yscrollcommand'] = self._yscrollcommand

        kw.update(options)

        self.frame.configure(require_redraw, **frame_options)
        super().configure(**kw)

    def headings(self):
        return Headings(self)

    ## Hooks

    def on_double_clicked(self, event: Event[Self]):
        region_clicked = self.identify_region(event.x, event.y)
        if region_clicked not in ("cell", "tree"):
            return

        column = self.identify_column(event.x)
        column_index = int(column[1:]) - 1
        selected_iid = self.focus()
        selected_values = self.item(selected_iid)

        if column == "#0":
            selected_text = selected_values.get('text')
        else:
            try:
                selected_text = selected_values.get('values')[column_index]
            except IndexError:
                return

        column_box = self.bbox(selected_iid, column)

        x, y, w, h = cast("tuple[int, int, int, int]", column_box)

        # Editing entry
        entry = ctk.CTkEntry(self, width=w)
        entry.insert(0, selected_text)

        user_data = {
            'column_index': column_index,
            'item_id': selected_iid,
            'entry': entry,
        }

        entry.place(x=x, y=y, w=w, h=h)
        entry.focus()
        on_focus_out = functools.partial(self.on_entry_focus_out, **user_data)
        entry.bind("<Escape>", on_focus_out)
        entry.bind("<FocusOut>", on_focus_out)
        entry.bind("<Return>", functools.partial(self.on_entry_enter_pressed, **user_data))

    def on_entry_focus_out(self, _event: Event[ctk.CTkEntry], **kw) -> None:
        entry: ctk.CTkEntry = kw['entry']
        assert isinstance(entry, ctk.CTkEntry)
        entry.destroy()

    def on_entry_enter_pressed(self, _event: Event, **kw) -> None:
        entry: ctk.CTkEntry = kw['entry']
        assert isinstance(entry, ctk.CTkEntry)

        new_text = entry.get()
        edited_column_index: int = kw['column_index']
        edited_item_id: str = kw['item_id']

        assert edited_column_index >= -1

        if edited_column_index == -1:
            self.item(edited_item_id, text=new_text)
        else:
            current_values = list(self.item(edited_item_id, "values"))
            current_values[edited_column_index] = new_text
            self.item(edited_item_id, values=current_values)

        entry.destroy()
