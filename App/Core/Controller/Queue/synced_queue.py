from typing import Any, List, Iterator

from dataclasses import dataclass, field, asdict

from Class.dataclass import AudioMetaData, PlaylistMetaData
from Class.abstractclass import QueueABC, StatementQueueAbc

from Tools.Decorator.dec import method_dispatch

from ..Error.exceptions import StagedException


@dataclass(slots=True, kw_only=True, frozen=True)
class FinishedQueue(StatementQueueAbc):
    identification: int
    _queue: List[AudioMetaData] = field(default_factory=list, init=False)

    def __len__(self) -> int:
        return len(self._queue)
    

    def __iter__(self) -> Iterator[AudioMetaData]:
        for item in self._queue:
            yield item


    def enqueue(self, audio: AudioMetaData) -> None:
        if not isinstance(audio, AudioMetaData):
            raise TypeError(f"Guild identification: {self.identification} => FinishedQueue.enqueue(audio({type(audio)}))")
        
        self._queue.append(audio)


    def dequeue(self) -> AudioMetaData:
        if not self._queue:
            raise IndexError(f"Guild identification: {self.identification} => FinishedQueue.dequeue()")
        
        return self._queue.pop(0)
    

    def pop(self, index: int=-1) -> AudioMetaData:
        if not isinstance(index, int): 
            raise TypeError(f"Guild identification: {self.identification} => FinishedQueue.pop({index})")

        if index < 0 and len(self._queue) < index * -1:
            raise IndexError(f"Guild identification: {self.identification} => FinishedQueue.pop({index})")
        elif 0 <= index and len(self._queue) <= index:
            raise IndexError(f"Guild identification: {self.identification} => FinishedQueue.pop({index})")
        
        return self._queue.pop(index)
    

    def insert(self, index: int, audio: AudioMetaData) -> None:
        if not isinstance(index, int): 
            raise TypeError(f"Guild identification: {self.identification} => FinishedQueue.insert({index}, ...)")
        
        if not isinstance(audio, AudioMetaData):
            raise TypeError(f"Guild identification: {self.identification} => FinishedQueue.insert(..., audio({type(audio)}))")
        
        if index < 0 and len(self.playlist) < index * -1:
            raise IndexError(f"Guild identification: {self.identification} => FinishedQueue.insert({index}, ...)")
        elif 0 <= index and len(self.playlist) < index:
            raise IndexError(f"Guild identification: {self.identification} => FinishedQueue.insert({index}, ...)")
        
        self._queue.insert(index, audio)

    
    def clear(self) -> bool:
        """
        Returns
        --------
        `bool`: `True` If when queue is cleaned else returns `False`
        """
        self._queue = []

        return not bool(self._queue)
    

    def remove(self, index: int) -> None:
        if not isinstance(index, int): 
            raise TypeError(f"Guild identification: {self.identification} => FinishedQueue.remove({index})")

        if index < 0 and len(self._queue) < index * -1:
            raise IndexError(f"Guild identification: {self.identification} => FinishedQueue.remove({index})")
        elif 0 <= index and len(self._queue) <= index:
            raise IndexError(f"Guild identification: {self.identification} => FinishedQueue.remove({index})")
        
        self._queue.pop(index)


    def seek(self, index: int) -> AudioMetaData:
        if not isinstance(index, int): 
            raise TypeError(f"Guild identification: {self.identification} => FinishedQueue.seek({index})")

        if index < 0 and len(self._queue) < index * -1:
            raise IndexError(f"Guild identification: {self.identification} => FinishedQueue.seek({index})")
        elif 0 <= index and len(self._queue) <= index:
            raise IndexError(f"Guild identification: {self.identification} => FinishedQueue.seek({index})")

        return AudioMetaData(**asdict(self._queue[index]))
    

    @property
    def identification(self) -> int:
        return self.identification
    
    @property
    def queue(self) -> List[AudioMetaData]:
        return self._queue[:]
    
    @property
    def is_empty(self) -> bool:
        return not bool(self._queue)


@dataclass(slots=True, kw_only=True, frozen=True)
class LiveQueue(QueueABC):
    identification: int
    _queue: List[AudioMetaData] = field(default_factory=list, init=False)


    def enqueue(self, audio: AudioMetaData) -> None:
        if not isinstance(audio, AudioMetaData):
            raise TypeError(f"Guild identification: {self.identification} => LiveQueue.enqueue(audio({type(audio)}))")
        
        if self._queue:
            raise StagedException
        
        self._queue.append(audio)


    def dequeue(self) -> AudioMetaData:
        if not self._queue:
            raise IndexError(f"Guild identification: {self.identification} => LiveQueue.dequeue()")
        
        return self._queue.pop(0)


    @property
    def is_empty(self) -> bool:
        return not bool(self._queue)
    
    @property
    def identification(self) -> int:
        return self.identification
    
    @property
    def queue(self) -> List[AudioMetaData]:
        return self._queue[:]


@dataclass(slots=True, kw_only=True, frozen=True)
class WaitingQueue(StatementQueueAbc):
    identification: int
    _queue: List[AudioMetaData] = field(default_factory=list, init=False)

    def __len__(self) -> int:
        return len(self._queue)
    

    def __iter__(self) -> Iterator[AudioMetaData]:
        for item in self._queue:
            yield item

    @method_dispatch
    def enqueue(self, audio: Any) -> None:
        raise TypeError(f"Guild identification: {self.identification} => WaitingQueue.enqueue(audio({type(audio)}))")

    
    @enqueue.register(AudioMetaData)
    def _(self, audio: AudioMetaData) -> None:
        self._queue.append(audio)


    @enqueue.register(PlaylistMetaData)
    def _(self, audio: PlaylistMetaData) -> None:
        self._queue.extend(audio.unpack)

    
    @enqueue.register(list)
    def _(self, audio: List[AudioMetaData]) -> None:
        for element in audio:
            if not isinstance(element, AudioMetaData):
                raise TypeError(f"Guild identification: {self.identification} => \"AudioMetaData\" types are only allowed, but given List[{type(element)}, Any] type was given")
        else:
            self._queue.extend(audio)


    def dequeue(self) -> AudioMetaData:
        if not self._queue:
            raise IndexError(f"Guild identification: {self.identification} => WaitingQueue.dequeue()")
        
        return self._queue.pop(0)
    

    def pop(self, index: int=-1) -> AudioMetaData:
        if not isinstance(index, int): 
            raise TypeError(f"Guild identification: {self.identification} => WaitingQueue.pop({index})")

        if index < 0 and len(self._queue) < index * -1:
            raise IndexError(f"Guild identification: {self.identification} => WaitingQueue.pop({index})")
        elif 0 <= index and len(self._queue) <= index:
            raise IndexError(f"Guild identification: {self.identification} => WaitingQueue.pop({index})")
        
        return self._queue.pop(index)
    

    def insert(self, index: int, audio: AudioMetaData) -> None:
        if not isinstance(index, int): 
            raise TypeError(f"Guild identification: {self.identification} => WaitingQueue.insert({index}, ...)")
        
        if not isinstance(audio, AudioMetaData):
            raise TypeError(f"Guild identification: {self.identification} => WaitingQueue.insert(..., audio({type(audio)}))")
        
        if index < 0 and len(self.playlist) < index * -1:
            raise IndexError(f"Guild identification: {self.identification} => WaitingQueue.insert({index}, ...)")
        elif 0 <= index and len(self.playlist) < index:
            raise IndexError(f"Guild identification: {self.identification} => WaitingQueue.insert({index}, ...)")
        
        self._queue.insert(index, audio)

    
    def clear(self) -> bool:
        """
        Returns
        --------
        `bool`: `True` If when queue is cleaned else returns `False`
        """
        self._queue = []

        return not bool(self._queue)
    

    def remove(self, index: int) -> None:
        if not isinstance(index, int): 
            raise TypeError(f"Guild identification: {self.identification} => WaitingQueue.remove({index})")

        if index < 0 and len(self._queue) < index * -1:
            raise IndexError(f"Guild identification: {self.identification} => WaitingQueue.remove({index})")
        elif 0 <= index and len(self._queue) <= index:
            raise IndexError(f"Guild identification: {self.identification} => WaitingQueue.remove({index})")
        
        self._queue.pop(index)


    def seek(self, index: int) -> AudioMetaData:
        if not isinstance(index, int): 
            raise TypeError(f"Guild identification: {self.identification} => WaitingQueue.seek({index})")

        if index < 0 and len(self._queue) < index * -1:
            raise IndexError(f"Guild identification: {self.identification} => WaitingQueue.seek({index})")
        elif 0 <= index and len(self._queue) <= index:
            raise IndexError(f"Guild identification: {self.identification} => WaitingQueue.seek({index})")

        return AudioMetaData(**asdict(self._queue[index]))
    

    @property
    def identification(self) -> int:
        return self.identification
    
    @property
    def queue(self) -> List[AudioMetaData]:
        return self._queue[:]
    
    @property
    def is_empty(self) -> bool:
        return not bool(self._queue)