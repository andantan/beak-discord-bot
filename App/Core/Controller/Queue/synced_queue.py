from typing import Any, List, Iterator

from dataclasses import dataclass, field

from Class.dataclass import AudioMetaData, PlaylistMetaData
from Class.abstractclass import QueueABC


@dataclass(slots=True, kw_only=True)
class FinishedQueue(QueueABC):
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

        return AudioMetaData(**self._queue[index].pseudo_dict)
    

    @property
    def identification(self) -> int:
        return self.identification
    
    @property
    def queue(self) -> List[AudioMetaData]:
        return self._queue[:]
    
    @property
    def is_empty(self) -> Any:
        return not bool(self._queue)


@dataclass(slots=True, kw_only=True)
class Live:
    pass


@dataclass(slots=True, kw_only=True)
class WaitingQueue(QueueABC):
    ...