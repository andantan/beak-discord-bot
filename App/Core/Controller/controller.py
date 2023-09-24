import traceback

from random import shuffle

from typing import Generator, List, Tuple, TypeAlias, Union

from dataclasses import (
    dataclass as controller, 
    field
)

from .Error.exceptions import (
    RetriveAudioWarning,
    EmptyWaitingWarning,
    EmptyStageWarning,
    EmptyFinishedWarning
)

from ..Queue.wait import WaitingQueue
from ..Queue.stage import StageQueue
from ..Queue.finish import FinishedQueue
from ..Queue.Error.exceptions import StagedException

from Class.dataclass import AudioMetaData, PlaylistMetaData


AudiosMetaData: TypeAlias = List[AudioMetaData]
AwaitableAudioMetaData: TypeAlias = Union[AudioMetaData, PlaylistMetaData, AudiosMetaData]


@controller(slots=True, kw_only=True, frozen=True)
class SyncedQueueController:
    finished_queue: FinishedQueue = field(init=False)
    stage_queue: StageQueue = field(init=False)
    waiting_queue: WaitingQueue = field(init=False)


    def __post_init__(self) -> None:
        attributes = {
            "finished_queue": FinishedQueue(),
            "stage_queue": StageQueue(),
            "waiting_queue": WaitingQueue()
        }

        for _k, _v in attributes.items():
            object.__setattr__(self, _k, _v)
   

    def __len__(self) -> int:
        return len(self.finished_queue) + len(self.stage_queue) + len(self.waiting_queue)
    

    def __iter__(self) -> Generator[AudiosMetaData, None, None]:
        for queue in self.queues:
            yield queue

    
    def wait(self, audio: AwaitableAudioMetaData) -> None:
        self.waiting_queue.enqueue(audio=audio)
            

    def priority_wait(self, priority: int, audio: Union[AudioMetaData, AudiosMetaData]) -> None:
        self.waiting_queue.insert(index=priority, audio=audio)
        

    def stage(self) -> None:
        try:
            while audio := self.waiting_queue.dequeue():
                if not audio.is_dummy:
                    self.stage_queue.enqueue(audio=audio)
                    break

        except IndexError:
            raise EmptyWaitingWarning
        
        except StagedException as ero:
            self.waiting_queue.insert(index=0, audio=ero.intercepted_audio)
            self.finished_queue.enqueue(audio=self.stage_queue.queue_ownership)
            self.stage_queue.enqueue(audio=self.waiting_queue.pop(index=0))
        
        except Exception:
            print(traceback.format_exc())

        
    def retrive(self) -> None:
        self.waiting_queue.insert(index=0, audio=self.finished_queue.pop())

    
    def loop(self) -> None:
        self.waiting_queue.enqueue(audio=self.finished_queue.queue_ownership)
        
    
    def leave(self) -> None:
        try:
            self.finished_queue.enqueue(audio=self.stage_queue.dequeue())
            
        except StagedException as ero:
            self.finished_queue.enqueue(audio=ero.intercepted_audio[0])
            self.waiting_queue.insert(index=0, audio=ero.intercepted_audio[1:])
      

    def backward(self) -> None:
        try:
            audio = self.stage_queue.dequeue()
    
        except StagedException as ero:
            self.waiting_queue.insert(index=0, audio=ero.intercepted_audio)
            return
        
        self.waiting_queue.insert(index=0, audio=audio)


    def shuffle(self) -> None:
        looping_audio = self.finished_queue.queue_ownership + \
            self.waiting_queue.queue_ownership
            
        shuffle(looping_audio)
        self.waiting_queue.enqueue(audio=looping_audio)

    
    def create_dummy(self) -> None:
        self.waiting_queue.insert(0, audio=AudioMetaData())
        
        
    def reset(self, include_stage: bool=False) -> None:
        if include_stage:
            del self.queues_ownership
        else:
            del self.queues_ownership_exclude_stage


    @property
    def size(self) -> Tuple(int):
        return (len(self.finished_queue), len(self.stage_queue), len(self.waiting_queue))
    
    @property
    def seek(self) -> AudioMetaData:
        return self.stage_queue.seek

    @property
    def queues(self) -> List[AudiosMetaData]:
        return [
            self.finished_queue.queue,
            self.stage_queue.queue,
            self.waiting_queue.queue
        ]
    
    @property
    def queues_ownership(self) -> List[AudiosMetaData]:
        return [
            self.finished_queue.queue_ownership,
            self.stage_queue.queue_ownership,
            self.waiting_queue.queue_ownership
        ]
    
    @property
    def queues_ownership_exclude_stage(self) -> List[AudiosMetaData]:
        return [
            self.finished_queue.queue_ownership,
            self.waiting_queue.queue_ownership
        ]
        
    @property
    def is_waiting_empty(self) -> bool:
        return not bool(self.waiting_queue.queue)

