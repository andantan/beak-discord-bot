from typing import List, TypeAlias

from dataclasses import dataclass, field

from .Error.exceptions import StagedException

from Class.dataclass import AudioMetaData
from Class.abstractclass import QueueABC


AudiosMetaData: TypeAlias = List[AudioMetaData]


@dataclass(slots=True, kw_only=True)
class StageQueue(QueueABC):
    identification: int
    _queue: AudiosMetaData = field(default_factory=list, init=False)


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
    def queue(self) -> AudiosMetaData:
        return self._queue[:]
    
    @property
    def queue_ownership(self) -> AudiosMetaData:
        ownership, self._queue = self._queue[:], []

        return ownership