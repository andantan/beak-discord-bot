from typing import List, Generator, Union, TypeAlias

from dataclasses import dataclass, field

from Class.dataclass import AudioMetaData
from Class.abstractclass import StatementQueueABC


AudiosMetaData: TypeAlias = List[AudioMetaData]


@dataclass(slots=True, kw_only=True)
class FinishedQueue(StatementQueueABC):
    _queue: AudiosMetaData = field(default_factory=list, init=False)

    def __len__(self) -> int:
        return len(self._queue)
    

    def __iter__(self) -> Generator[AudioMetaData, None, None]:
        for item in self._queue:
            yield item


    def enqueue(self, audio: AudioMetaData) -> None:
        self._queue.append(audio)


    def dequeue(self) -> AudioMetaData:
        return self._queue.pop(0)


    def pop(self, index: int=-1) -> AudioMetaData:
        return self._queue.pop(index)
    

    def insert(self, index: int, audio: Union[AudioMetaData, AudiosMetaData]) -> None:
        raise NotImplementedError
        
    
    def clear(self) -> None:
        self._queue = []
    

    def remove(self, index: int) -> None:
        self._queue.pop(index)


    def seek(self, index: int) -> AudioMetaData:
        return AudioMetaData(**self._queue[index].asdict)
    
    
    @property
    def queue(self) -> AudiosMetaData:
        return self._queue[:]
    
    @property
    def queue_ownership(self) -> AudiosMetaData:
        ownership, self._queue = self._queue[:], []

        return ownership
    
    @property
    def is_empty(self) -> bool:
        return not bool(self._queue)
