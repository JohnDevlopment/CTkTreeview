from typing import Any, Iterable, TypeAlias, TypeGuard, TypeVar

_ScreenUnits: TypeAlias = str | float

T = TypeVar('T')

def grid(
    widget: Any,
    *,
    column: int=...,
    columnspan: int=...,
    row: int=...,
    rowspan: int=...,
    ipadx: _ScreenUnits=...,
    ipady: _ScreenUnits=...,
    padx: _ScreenUnits | tuple[_ScreenUnits, _ScreenUnits]=...,
    pady: _ScreenUnits | tuple[_ScreenUnits, _ScreenUnits]=...,
    sticky: str=...,
    in_: Any=...,
    **kw: Any
) -> None:
    ...

def is_iterable(obj: T) -> TypeGuard[Iterable[T]]:
    ...

def error(fmt: str, *args: Any):
    ...

def pop_kwargs(dct: dict[str, Any], valid_keys: set[str]) -> dict[str, Any]:
    ...

def check_kwargs_empty(dct: dict[str, Any], raise_error: bool=...) -> bool:
    ...
