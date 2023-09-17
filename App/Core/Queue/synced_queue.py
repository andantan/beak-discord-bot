from typing import Any, List, Generator, Union

from dataclasses import dataclass, field

from .Error.exceptions import StagedException

from Class.dataclass import AudioMetaData, PlaylistMetaData
from Class.abstractclass import QueueABC, StatementQueueABC

from Tools.Decorator.dec import method_dispatch



@dataclass(slots=True, kw_only=True)
class FinishedQueue(StatementQueueABC):
    identification: int
    _queue: List[AudioMetaData] = field(default_factory=list, init=False)

    def __len__(self) -> int:
        return len(self._queue)
    

    def __iter__(self) -> Generator[AudioMetaData, None, None]:
        for item in self._queue:
            yield item


    def enqueue(self, audio: AudioMetaData) -> None:
        if not isinstance(audio, AudioMetaData):
            raise TypeError
        
        self._queue.append(audio)


    def dequeue(self) -> AudioMetaData:
        return self._queue.pop(0)


    def pop(self, index: int=-1) -> AudioMetaData:
        return self._queue.pop(index)
    

    def insert(self, index: int, audio: Union[AudioMetaData, List[AudioMetaData]]) -> None:
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
    def queue(self) -> List[AudioMetaData]:
        return self._queue[:]
    
    @property
    def queue_ownership(self) -> List[AudioMetaData]:
        ownership, self._queue = self._queue[:], []

        return ownership
    
    @property
    def is_empty(self) -> bool:
        return not bool(self._queue)


@dataclass(slots=True, kw_only=True)
class StageQueue(QueueABC):
    identification: int
    _queue: List[AudioMetaData] = field(default_factory=list, init=False)


    def __len__(self) -> int:
        return len(self._queue)
    

    def enqueue(self, audio: AudioMetaData) -> None:
        if not isinstance(audio, AudioMetaData):
            raise TypeError
   
        if self._queue:
            bring_out_audios, self._queue = self._queue[1:].append(audio), self._queue[:1]

            raise StagedException(intercepted_audio=bring_out_audios)
        
        self._queue.append(audio)


    def dequeue(self) -> AudioMetaData:
        audio = self._queue.pop(0)

        if self._queue:
            bring_out_audios, self._queue = self._queue[:], []

            raise StagedException(intercepted_audio=bring_out_audios)
        
        return audio
    

    def clear(self) -> None:
        self._queue = []


    @property
    def is_empty(self) -> bool:
        return not bool(self._queue)
    
    @property
    def identification(self) -> int:
        return self.identification
    
    @property
    def queue(self) -> List[AudioMetaData]:
        return self._queue[:]
    
    @property
    def queue_ownership(self) -> List[AudioMetaData]:
        ownership, self._queue = self._queue[:], []

        return ownership


@dataclass(slots=True, kw_only=True)
class WaitingQueue(StatementQueueABC):
    identification: int
    _queue: List[AudioMetaData] = field(default_factory=list, init=False)

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
    def _(self, audio: List[AudioMetaData]) -> None:
        for element in audio:
            if not isinstance(element, AudioMetaData):
                raise TypeError
        else:
            self._queue.extend(audio)


    def dequeue(self) -> AudioMetaData:
        return self._queue.pop(0)
    

    def pop(self, index: int=-1) -> AudioMetaData:
        return self._queue.pop(index)
    

    def insert(self, index: int, audio: Union[AudioMetaData, List[AudioMetaData]]) -> None:
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
    def queue(self) -> List[AudioMetaData]:
        return self._queue[:]
    
    @property
    def queue_ownership(self) -> List[AudioMetaData]:
        ownership, self._queue = self._queue[:], []

        return ownership

    @property
    def is_empty(self) -> bool:
        return not bool(self._queue)