from typing import (
    List, Required, TypedDict, Generic, TypeVar
)

from dataclasses import dataclass


T = TypeVar("T")


@dataclass(frozen=True)
class ArgumentOption(Generic[T]):
    flags: List[str]
    argument: T
    types: T
