from typing import Any, List, Generator, Union, TypeAlias

from dataclasses import dataclass, field

from Class.dataclass import AudioMetaData, PlaylistMetaData
from Class.abstractclass import StatementQueueABC

from Tools.Decorator.dec import method_dispatch


AudiosMetaData: TypeAlias = List[AudioMetaData]


@dataclass(slots=True, kw_only=True)
class WaitingQueue(StatementQueueABC):
    identification: int
    _queue: AudiosMetaData = field(default_factory=list, init=False)

    def __len__(self) -> int:
        return len(self._queue)
    

    def __iter__(self) -> Generator[AudioMetaData, None, None]:
        for item in self._queue:
            yield item


    @method_dispatch
    def enqueue(self, audio: Any) -> None:
        raise TypeError

    
    @enqueue.register(AudioMetaData)
    def _(self, audio: AudioMetaData) -> None:
        self._queue.append(audio)


    @enqueue.register(PlaylistMetaData)
    def _(self, audio: PlaylistMetaData) -> None:
        self._queue.extend(audio.unpack)

    
    @enqueue.register(list)
    def _(self, audio: AudiosMetaData) -> None:
        for element in audio:
            if not isinstance(element, AudioMetaData):
                raise TypeError
        else:
            self._queue.extend(audio)


    def dequeue(self) -> AudioMetaData:
        return self._queue.pop(0)
    

    def pop(self, index: int=-1) -> AudioMetaData:
        return self._queue.pop(index)
    

    def insert(self, index: int, audio: Union[AudioMetaData, AudiosMetaData]) -> None:
        if isinstance(audio, AudioMetaData):
            self._queue.insert(index, audio)

        elif isinstance(audio, list):
            for element in audio:
                if not isinstance(element, AudioMetaData):
                    raise TypeError
            else:
                self._queue = audio.extend(self._queue)
            
        else:
            raise TypeError


    def clear(self) -> None:
        self._queue = []
    

    def remove(self, index: int) -> None:
        self._queue.pop(index)


    def seek(self, index: int) -> AudioMetaData:
        return AudioMetaData(**self._queue[index].asdict)
    

    @property
    def identification(self) -> int:
        return self.identification
    
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