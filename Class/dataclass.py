from typing import (
    List, Optional, Generic, TypeVar
)

from dataclasses import dataclass


T = TypeVar("T")


@dataclass(frozen=True)
class ArgumentOption(Generic[T]):
    dest: str
    flags: List[str]
    help: Optional[str]
    argument: T
