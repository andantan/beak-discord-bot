import collections

from abc import ABCMeta, abstractmethod
from typing import Any, Unpack, TypedDict, Type, TypeVar, Self


T = TypeVar("T")


class QueueABC(collections.Iterator, metaclass=ABCMeta):
    @abstractmethod
    def __len__(self: Type[T]) -> int: ...

    @abstractmethod
    def __iter__(self: Type[T]) -> Self: ...

    @abstractmethod
    def __next__(self: Type[T]) -> Any: ...

    @abstractmethod 
    def enqueue(self: Type[T], *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...

    @abstractmethod
    def dequeue(self: Type[T], *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...

    @abstractmethod
    def pop(self: Type[T], *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...

    @abstractmethod
    def insert(self: Type[T], *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...

    @abstractmethod
    def clear(self: Type[T], *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...

    @abstractmethod
    def remove(self: Type[T], *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...

    @abstractmethod
    def seek(self: Type[T], *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...

    @abstractmethod
    def copy(self: Type[T], *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...

    @property
    @abstractmethod
    def is_empty(self: Type[T], *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...

    @property
    @abstractmethod
    def is_alone(self: Type[T], *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...
