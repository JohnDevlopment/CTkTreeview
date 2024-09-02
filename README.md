# CTkTreeview
A Treeview widget for customtkinter (extension/add-on).

This package is built off of the idea from https://github.com/TomSchimansky/CustomTkinter/discussions/1821. Credit goes to @avalon60 for the idea.

## Installation
Since there are no source or wheel distributions, you can install directly from Github.

```sh
pip install git+https://github.com/JohnDevlopment/CTkTreeview.git
```
## Usage
Calling the package directly brings up a demo of the Treeview.

![CTkTreeview demo when it's first launched](./images/treeview-default-state.jpg)

Double-clicking an item lets you edit it. Press Enter to apply the change. Press Escape or focus ouf of the entry to cancel the edit.

![CTkTreeview with an entry displayed over one of its items](./images/treeview-edit-state.jpg)

### In Code
Now to the point of using `CTkTreeview` in code, here is a snippet:

```python
from CTkTreeview import CTkTreeview
from customtkinter import CTk

app = CTk()
tree = CTkTreeview(app, height=25, columns=["First", "Last", "Age"], width=500, show="headings")
tree.grid(row=0, column=0)
...
app.mainloop()
```

This creates a treeview with three columns named "First", "Last", and "Age". It is configured to show only the headings.

To configure the headings, use `headings()`.

```python
with tree.headings() as th:
    th.text("First", "First Name")
    th.text("Last", "Last Name")
    th.text("Age", "Age")
```

To configure the columns, use `columns()`.

```python
with tree.columns() as tc:
    tc.minwidth("First", 150)
    tc.minwidth("Last", 150)
    tc.anchor("Age", "e")
```

## Documentation
Documentation is planned for a future update once the code is more or less finished.
