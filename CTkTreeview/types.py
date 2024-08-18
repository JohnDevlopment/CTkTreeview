from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypeAlias

Color: TypeAlias = str | tuple[str, str]
