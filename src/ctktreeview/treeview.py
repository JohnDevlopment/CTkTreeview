"""
CTkTreeview widget and its helper classes.
"""

from __future__ import annotations

import functools
import re
from collections.abc import Callable
from contextlib import AbstractContextManager
from tkinter import Event, ttk
from typing import TYPE_CHECKING, cast

import customtkinter as ctk

from .utils import pop_kwargs

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any, Literal, TypeAlias

    from typing_extensions import Self

    from .typings import Anchor, ImageSpec

    StrDict: TypeAlias = dict[str, Any]


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
        self.obj.tree.heading(column, anchor=anchor)

    def command(
        self, column: str | int, command: str | Callable[[], None] | None = None
    ):
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
            self.obj.tree.heading(column, command=command)
        else:
            return self.obj.tree.heading(column, "heading")

    def image(self, column: str | int, image: ImageSpec | None = None):
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
            self.obj.tree.heading(column, image=image)
        else:
            return self.obj.tree.heading(column, "image")

    def text(self, column: str | int, text: str | None = None):
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
            self.obj.tree.heading(column, text=text)
        else:
            return self.obj.tree.heading(column, "text")


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

    def anchor(self, column: int | str, anchor: Anchor | None = None):
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
            self.obj.tree.column(column, anchor=anchor)
            return

        return cast("Anchor", self.obj.tree.column(column, "anchor"))

    def id(self, column: int | str) -> str:
        """
        Query the ID of a column.

        :param column: String name or index of a column
        :type column: str or int

        :returns: The ID of `column`
        :rtype: str
        """
        return self.obj.tree.column(column, "id")

    def minwidth(self, column: int | str, minwidth: int | None = None):
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
            self.obj.tree.column(column, minwidth=minwidth)
            return

        return self.obj.tree.column(column, "minwidth")

    def width(self, column: int | str, width: int | None = None):
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
            self.obj.tree.column(column, width=width)
            return

        return self.obj.tree.column(column, "width")

    def stretch(self, column: int | str, stretch: bool | None = None):
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
            self.obj.tree.column(column, stretch=stretch)
            return

        return self.obj.tree.column(column, "stretch")


_registered_configurators: dict[str, Callable[[Any, Any, StrDict], None]] = {}


def register_configurator(
    func: Callable[[Any, Any, StrDict], None],
) -> Callable[[Any, Any, StrDict], None]:
    global _registered_configurators

    name = func.__name__
    m = re.fullmatch(r"_configure_([a-z0-9_]+)", name)
    assert m is not None
    key = m[1]
    _registered_configurators[key] = func
    return func


class CTkTreeview(ctk.CTkFrame):
    """
    A customized treeview widget.

    For the time being, no customizations are done on this
    widget---such changes will be done at a later update.
    """

    _valid_frame_options = {
        "background_corner_colors",
        "bg_color",
        "border_color",
        "border_width",
        "fg_color",
        "corner_radius",
        "height",
        "width",
    }

    def __init__(
        self,
        master: Any,
        *,
        # Treeview options
        columns,
        displaycolumns=("#all",),
        height=25,
        selectmode="extended",
        show=("tree", "headings"),
        # Frame options
        bg_color="transparent",
        border_color=None,
        border_width=None,
        corner_radius=None,
        fg_color=None,
        width=200,
        **kw,
    ):
        """
        Initialize a treeview object with a given master.

        @param master The master of this widget
        @param columns
        @parblock
        A list of data columns. May be a single string to define a
        single column or a list of strings for multiple columns. The
        list may also contain integers.
        @endparblock
        @param displaycolumns
        @parblock
        The list of columns to display, and in what order. The
        columns are referenced by their symbolic names (as in
        `columns`), or their numerical index into the list passed in
        `columns`. If `#all` or `(#all,)` (the default), all
        columns are displayed in the order that they are defined.
        @endparblock
        @param height The widget height in rows.
        @param selectmode
        @parblock
        Controls how the selection is handled. Valid modes are
        `browse`, `extended`, and `none`.
        @endparblock
        @param show
        @parblock
        Controls what elements of the tree to display. Values can be
        `tree`, `headings`, `tree headings`, an empty string,
        or a tuple consisting of any combination of `tree` and
        `headings`.
        @endparblock
        @param bg\_color
        @parblock
        Sets the background color of this widget. But what it really
        sets is the background color of the containing frame. The
        special value `transparent` (the default) makes the frame
        transparent.
        @endparblock
        @param border_color
        @parblock
        Sets the border color. In reality, this is an option for the
        containing frame. If omitted or `None`, the border is not
        displayed.
        @endparblock
        @param int border_width
        @parblock
        Sets the border width. In reality, this is an option for the
        containing frame.
        @endparblock
        @param corner_radius Currently unused.
        @param Color fg_color
        @parblock
        Sets the forground color. In
        reality, this is an option for the
        containing frame.
        @endparblock
        @param width Sets the width. In reality, this is an option
        for the containing frame.

        @param class
        @parblock
        The window class of this widget. The class is used when
        querying the option database for the window’s other options,
        to determine the default bindtags for the window, and to
        select the widget’s default layout and style.

        This is a read-only option; it can only be set on widget
        creation.
        @endparblock
        @param cursor The mouse cursor to be used for this
        widget. If not specified, defaults to inheriting its
        parent’s cursor.
        @param takefocus Determines whether this widget should take
        focus during keyboard traversal. If `False`, this widget is
        skipped; if `True`, it accepts focus as long as it is
        viewable. If an empty string, the decision is left to
        traversal scripts.
        @param style Custom widget style.
        """
        # Attributes:tree
        self.__columns = columns
        self.__displaycolumns = displaycolumns
        self.__height = height
        self.__selectmode = selectmode
        self.__show = show

        # Attributes:frame
        self.__bg_color = bg_color
        self.__border_color = border_color
        self.__border_width = border_width
        self.__corner_radius = corner_radius
        self.__fg_color = fg_color
        self.__width = width

        super().__init__(
            master,
            bg_color=bg_color,
            border_color=border_color,
            border_width=border_width,
            corner_radius=corner_radius,
            fg_color=fg_color,
            width=width,
        )

        self.tree = ttk.Treeview(
            self,
            columns=cast("Any", columns),
            displaycolumns=cast("Any", displaycolumns),
            height=height,
            selectmode=cast("Any", selectmode),
            show=cast("Any", show),
            **kw,
        )
        self.tree.pack(fill="both", expand=True, side="left")

        # Scrollbar
        self.scrollbar = ctk.CTkScrollbar(
            self, orientation="vertical", command=self.yview
        )
        self.scrollbar.pack(fill="y", expand=True, side="right")

        self.bind("<Double-1>", self.on_double_clicked, True)

    def columns(self):
        return Columns(self)

    def configure(self, require_redraw=False, **kw):
        frame_options = pop_kwargs(kw, self._valid_frame_options)
        options = {}

        for k in list(kw.keys()):
            if k in _registered_configurators:
                fn = _registered_configurators[k]
                fn(self, kw.pop(k), options)

        kw.update(options)
        self.tree.configure(**kw)

        super().configure(require_redraw, **frame_options)

    def headings(self):
        return Headings(self)

    ## Pack, Grid and Place wrapper methods

    def pack(self, **kw) -> None:
        """
        Pack a widget in the parent widget.

        @param after Pack the widget after this.

        @param anchor
        @parblock
        Position widget according to a given direction. Must be one
        of the cardinal directions nw, n, ne, e, se, s, sw,  or w,
        or center. Defaults to center.
        @endparblock

        @param before Pack the widget before this.

        @param expand Whether to expand widget if parent size grows.

        @param fill
        @parblock
        One of NONE, X, Y, or BOTH. Fill widget if this direction if
        parent grows.
        @endparblock

        @param in Contain self in this widget.
        @param in_ Alias of `in`.

        @param ipadx Internal padding in X direction.
        @param ipady Internal padding in Y direction.
        @param padx External padding in X direction.
        @param pady External padding in Y direction.

        @param side Where to add this widget, one of TOP, BOTTOM,
        LEFT, or RIGHT.
        """
        return self.pack_configure(**kw)

    def pack_configure(self, cnf={}, **kw) -> None:
        """
        Pack a widget in the parent widget.

        @param after Pack the widget after this.

        @param anchor
        @parblock
        Position widget according to a given direction. Must be one
        of the cardinal directions nw, n, ne, e, se, s, sw,  or w,
        or center. Defaults to center.
        @endparblock

        @param before Pack the widget before this.

        @param expand Whether to expand widget if parent size grows.

        @param fill
        @parblock
        One of NONE, X, Y, or BOTH. Fill widget if this direction if
        parent grows.
        @endparblock

        @param in Contain self in this widget.
        @param in_ Alias of `in`.

        @param ipadx Internal padding in X direction.
        @param ipady Internal padding in Y direction.
        @param padx External padding in X direction.
        @param pady External padding in Y direction.

        @param side Where to add this widget, one of TOP, BOTTOM,
        LEFT, or RIGHT.
        """
        return super().pack_configure(cnf, **kw)

    def pack_forget(self) -> None:
        """
        Unmap this widget and remove it from the packing order.
        """
        return super().pack_forget()

    def pack_info(self):
        """
        Return the packing options for this widget.

        @return
        @parblock
        A dictionary containing the options that were passed to
        @ref pack. It contains the following keys: `in`, `anchor`,
        `expand`, `fill`, `side`, `ipadx`, `ipady`, `padx`, `pady`.
        @endparblock

        @see pack.
        """
        return super().pack_info()

    def pack_propagate(self, *args):
        """
        Set or get the status for packing propagation.

        @param flag If provided, sets the propagation flag.

        @return The current propagation flag unless `flag` is
        provided, in which case `None`.
        """
        return super().propagate(*args)

    def slaves(self):
        """
        Return a list of this widget's slaves in its packing order.
        """
        return super().slaves()

    ## Treeview wrapper functions

    def bbox(self, item: str | int, column: str | int | None = None):
        """
        Get the bounding box of the specified item.

        @param item The string ID or index of an item.
        @param column A column ID or index (optional).

        @return A bounding box (relative to the widget’s window) in
                the form x y width height; If `column` is specified,
                the bounding box of that cell; an empty string if
                `item` is not visible (i.e., it is a descendant of a
                closed item or is scrolled offscreen).
        """
        return self.tree.bbox(item, column)

    def delete(self, *items: str | int):
        """
        Delete the specified items.

        Each item’s descendants are also deleted.

        @param items The items to delete.

        @note The parent item cannot be deleted.
        """
        return self.tree.delete(*items)

    def detach(self, *items):
        # TODO: Write docstring
        return self.tree.detach(*items)

    def exists(self, item):
        # TODO: Write docstring
        return self.tree.exists(item)

    def get_children(self, item=None):
        # TODO: Write docstring
        return self.tree.get_children(item)

    def focus(self, item=None):
        # TODO: Write docstring
        return self.tree.focus(item)

    def identify(self, component, x: int, y: int):
        # Internal method.
        return self.tree.identify(component, x, y)

    def identify_column(self, x: int):
        """
        Identify the region at the given x coordinate.

        :param int x: The X coordinate of column

        :returns: The column identifier of the cell at position `x`
        :rtype: str
        """
        return self.tree.identify_column(x)

    def identify_element(self, x: int, y: int):
        # TODO: Write docstring
        return self.tree.identify_element(x, y)

    def identify_region(self, x: int, y: int):
        """
        Identify the region.

        The region will be one of:
        * cell: data cell
        * heading: tree heading area
        * separator: space between two columns headings;
        * tree: the tree area

        @param x The X coordinate.
        @param y The Y coordinate.

        @return One of `cell`, `heading`, `separator`, `tree`.
        """
        return self.tree.identify_region(x, y)

    def identify_row(self, y: int):
        # TODO: Write docstring
        return self.tree.identify_row(y)

    def index(self, item):
        # TODO: Write docstring
        return self.tree.index(item)

    def insert(self, parent, index: int | Literal["end"], iid=None, **kw):
        # TODO: Write docstring
        return self.tree.insert(parent, index, iid, **kw)

    def item(self, item, option=None, **kw):
        # TODO: Write docstring
        return self.tree.item(item, option, **kw)

    def move(self, item, parent, index):
        # TODO: Write docstring
        return self.tree.move(item, parent, index)

    def next(self, item):
        # TODO: Write docstring
        return self.tree.next(item)

    def parent(self, item):
        # TODO: Write docstring
        return self.tree.parent(item)

    def prev(self, item):
        # TODO: Write docstring
        return self.tree.prev(item)

    reattach = next

    def see(self, item):
        """
        Ensure that the specified item is visible.
        """
        return self.tree.see(item)

    def selection(self):
        """
        Return a tuple of selected items.
        """
        return self.tree.selection()

    def selection_add(self, *items):
        """
        Add the specified items to the selection.
        """
        return self.tree.selection_add(*items)

    def selection_remove(self, *items):
        """
        Remove the specified items from the selection.
        """
        return self.tree.selection_remove(*items)

    def selection_set(self, *items):
        """
        Set the specified items as the new selection.
        """
        return self.tree.selection_set(*items)

    def selection_toggle(self, *items):
        """
        Toggle the selection state of of each specified item.
        """
        return self.tree.selection_toggle(*items)

    def set(self, item, column=None, value=None):
        # TODO: Write docstring
        return self.tree.set(item, column, value)

    def set_children(self, item, *newchildren):
        # TODO: Write docstring
        return self.tree.set_children(item, *newchildren)

    def tag_bind(self, tagname: str, sequence=None, callback=None):
        # TODO: Write docstring
        # TODO: Function that calls CALLBACK with Event using CTkTreeview instead of ttk.Treeview
        return self.tree.tag_bind(tagname, sequence, callback)

    def tag_configure(self, tagname, option=None, **kw):
        """
        Query or modify the options for a tag.

        @param tagname The tag for which to modify options.
        @param option If specified, the name of an option to query.
        @param foreground Text foreground color to apply to the tag.
        @param background Text background color to apply to the tag.
        @param font Text font to apply to the tag.

        @return
        @parblock
        If *option* and keywords are not provided, a dictionary of the option settings for *tagname*.
        If *option* is specified, the result is the value for that option.
        Otherwise, the result is `None` and the specified options are set for *tagname*.
        @endparblock
        """
        return self.tree.tag_configure(tagname, option, **kw)

    def tag_has(self, tagname, item=None):
        """
        Query whether an item or all items have a specific tag.

        @param tagname Query the item(s) for this tag.

        @param item Check the whether this item has *tag*.

        @return True if *item* has *tag*, if *item* is specified. Otherwise, a tuple of
                items which have the tag.
        """
        return self.tree.tag_has(tagname, item)

    def xview(self, *args):
        """
        Query or modify the x-view of the window.

        @param index The index which, if provided, adjusts the x-view such that it is
                     displayed at the top edge of the window.

        @return If `index` is omitted, a tuple of floats each in
                the range [0,1]. Together, they describe the
                vertical span that is visible in the window. For
                example, the value `(0.2, 0.4)` describes that
                20% of the window is cut off from the top, 40% of
                the content is visible, and 40% is cut off from
                the bottom.
        """
        return self.tree.xview(*args)

    def xview_moveto(self, fraction: float):
        """
        Adjust the x-view of the window to a certain position.

        The result of this function is that the x-view is moved such
        that `fraction` of the total height of the canvas is
        off-screen to the top.

        :param float fraction: A fraction of the total height of the
                               canvas
        """
        return self.tree.xview_moveto(fraction)

    def xview_scroll(self, number: int, what):
        """
        Shift the x-view of the window.

        @param number The number of *what* units to scroll
        @param what The unit to measure *number* in. Can be either `units` or `pages`.
        """
        return self.tree.xview_scroll(number, what)

    def yview(self, *args):
        """
        Query or modify the y-view of the window.

        :param index: If provided, adjusts the y-view such that this
                      is displayed at the top edge of the window
        :type index: int or None

        :returns: If ``index`` is omitted, a tuple of floats each in
                  the range [0,1]. Together, they describe the
                  vertical span that is visible in the window. For
                  example, the value ``(0.2, 0.4)`` describes that
                  20% of the window is cut off from the top, 40% of
                  the content is visible, and 40% is cut off from
                  the bottom
        :rtype: tuple[float, float] or None
        """
        self.tree.yview(*args)

    def yview_moveto(self, fraction):
        """
        Adjust the y-view of the window to a certain position.

        The result of this function is that the y-view is moved such
        that `fraction` of the total height of the canvas is
        off-screen to the top.

        :param float fraction: A fraction of the total height of the
                               canvas
        """
        self.tree.yview_moveto(fraction)

    def yview_scroll(self, number, what):
        """
        Shift the y-view of the window.

        :param int number: The number of `what` units to scroll

        :param str what: The unit to measure `number` in. Can be
                         either "units" or "pages"
        """
        return self.tree.yview_scroll(number, what)

    ## Configurators

    @register_configurator
    def _configure_displaycolumns(self, value, options: StrDict):
        self.__displaycolumns = value
        options["displaycolumns"] = value

    @register_configurator
    def _configure_fg_color(self, value, options: StrDict):
        self.__fg_color = value
        options["fg_color"] = value

    @register_configurator
    def _configure_height(self, value, options: StrDict):
        self.__height = value
        options["height"] = value

    @register_configurator
    def _configure_selectmode(self, value, options: StrDict):
        self.__selectmode = value
        options["selectmode"] = value

    @register_configurator
    def _configure_show(self, value, options: StrDict):
        self.__show = value
        options["show"] = value

    @register_configurator
    def _configure_yscrollcommand(self, value, options: StrDict):
        self.__yscrollcommand = value
        options["yscrollcommand"] = value

    ## Hooks

    def on_double_clicked(self, event: Event[Self]) -> None:
        """
        Callback for when an item is double-clicked.
        """
        region_clicked = self.identify_region(event.x, event.y)
        if region_clicked not in ("cell", "tree"):
            return

        column = self.identify_column(event.x)
        column_index = int(column[1:]) - 1
        selected_iid = self.focus()
        selected_values = self.item(selected_iid)

        if column == "#0":
            selected_text = selected_values.get("text")
            assert isinstance(selected_text, str)
        else:
            try:
                selected_text = selected_values.get("values")[column_index]
            except IndexError:
                return

        column_box = self.bbox(selected_iid, column)

        x, y, w, h = cast("tuple[int, int, int, int]", column_box)

        # Editing entry
        entry = ctk.CTkEntry(self, width=w)
        entry.insert(0, selected_text)

        user_data = {
            "column_index": column_index,
            "item_id": selected_iid,
            "entry": entry,
        }

        entry.place(x=x, y=y, w=w, h=h)
        entry.focus()
        on_focus_out = functools.partial(self.on_entry_focus_out, **user_data)
        entry.bind("<Escape>", on_focus_out)
        entry.bind("<FocusOut>", on_focus_out)
        on_enter_pressed = functools.partial(self.on_entry_enter_pressed, **user_data)
        entry.bind("<Return>", on_enter_pressed)
        entry.bind('<KP_Enter>', on_enter_pressed)

    def on_entry_focus_out(self, _event: Event[ctk.CTkEntry], **kw) -> None:
        entry: ctk.CTkEntry = kw["entry"]
        assert isinstance(entry, ctk.CTkEntry)
        entry.destroy()

    def on_entry_enter_pressed(self, _event: Event, **kw) -> None:
        entry: ctk.CTkEntry = kw["entry"]
        assert isinstance(entry, ctk.CTkEntry)

        new_text = entry.get()
        edited_column_index: int = kw["column_index"]
        edited_item_id: str = kw["item_id"]

        assert edited_column_index >= -1

        if edited_column_index == -1:
            self.item(edited_item_id, text=new_text)
        else:
            current_values = list(self.item(edited_item_id, "values"))
            current_values[edited_column_index] = new_text
            self.item(edited_item_id, values=current_values)

        entry.destroy()
