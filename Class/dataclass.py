from typing import (
    List, Optional, Generic, TypeVar
)

from dataclasses import dataclass

from deprecated import deprecated

T = TypeVar("T")


@deprecated(version="1.0.5.6c")
@dataclass(frozen=True)
class ArgumentOption(Generic[T]):
    dest: str
    flags: List[str]
    help: Optional[str]
    argument: T
