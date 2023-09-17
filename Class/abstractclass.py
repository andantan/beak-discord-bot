from abc import ABCMeta, abstractmethod
from typing import Any, Unpack, TypedDict


class QueueABC(metaclass=ABCMeta):
    @abstractmethod
    def enqueue(self, *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...

    @abstractmethod
    def dequeue(self, *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...
        
    @property
    @abstractmethod
    def is_empty(self, *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...

    @property
    @abstractmethod
    def queue(self, *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...

    @property
    @abstractmethod
    def queue_ownership(self, *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...


class StatementQueueABC(QueueABC, metaclass=ABCMeta):
    @abstractmethod
    def __len__(self) -> Any: ...

    @abstractmethod
    def __iter__(self) -> Any: ...

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

    @property
    @abstractmethod
    def identification(self, *args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Any: ...
