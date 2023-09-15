import collections.abc

from abc import ABCMeta, abstractmethod
from typing import Any, Unpack, TypedDict

from deprecated import deprecated



class QueueABC(collections.abc.Iterator, metaclass=ABCMeta):
    @abstractmethod
    def __len__(self) -> Any: ...

    @abstractmethod
    def __iter__(self) -> Any: ...

    @abstractmethod 
    def enqueue(self, *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...

    @abstractmethod
    def dequeue(self, *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...

    @abstractmethod
    def pop(self, *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...

    @abstractmethod
    def insert(self, *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...

    @abstractmethod
    def clear(self, *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...

    @abstractmethod
    def remove(self, *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...

    @abstractmethod
    def seek(self, *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...


    @deprecated(version="1.0.6.1c", reason="Alternated to queue property")
    @abstractmethod
    def copy(self, *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...

    @property
    @abstractmethod
    def identification(self, *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...

    @property
    @abstractmethod
    def queue(self, *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...

    @property
    @abstractmethod
    def is_empty(self, *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...


    @deprecated(version="1.0.6.1c", reason="Alternated to raw approach")
    @property
    @abstractmethod
    def is_alone(self, *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...
