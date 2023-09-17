import logging
import traceback

from typing import Generator, List, Tuple, TypeAlias, Union

from dataclasses import (
    dataclass as controller, 
    field
)

from .Error.exceptions import (
    RetriveAudioWarning,
    AbnormalTypeException,
    EmptyQueueWarning,
)
from ..Queue.synced_queue import FinishedQueue, StageQueue, WaitingQueue
from ..Queue.Error.exceptions import StagedException

from Class.dataclass import AudioMetaData, PlaylistMetaData


AwaitableAudioMetaData: TypeAlias = Union[AudioMetaData, PlaylistMetaData, List[AudioMetaData]]



@controller(slots=True, kw_only=True, frozen=True)
class SyncedQueueController:
    guild_identification: int

    finished_queue: FinishedQueue = field(init=False)
    stage_queue: StageQueue = field(init=False)
    waiting_queue: WaitingQueue = field(init=False)


    def __post_init__(self) -> None:
        attributes = {
            "finished_queue": FinishedQueue(identification=self.guild_identification),
            "stage_queue": StageQueue(identification=self.guild_identification),
            "waiting_queue": WaitingQueue(identification=self.guild_identification)
        }

        for _k, _v in attributes.items():
            object.__setattr__(self, _k, _v)
   

    def __len__(self) -> int:
        return len(self.finished_queue) + len(self.stage_queue) + len(self.waiting_queue)
    

    def __iter__(self) -> Generator[List[AudioMetaData], None, None]:
        for queue in self.queues:
            yield queue

    
    def wait(self, audio: AwaitableAudioMetaData) -> None:
        try:
            self.waiting_queue.enqueue(audio=audio)

        except TypeError:
            raise AbnormalTypeException(obj=audio)
        
        except Exception:
            print(traceback.format_exc())


    def stage(self) -> None:
        try:
            while audio := self.waiting_queue.dequeue():
                if not audio.is_dummy:
                    self.stage_queue.enqueue(audio=audio)
                    break

        except IndexError:
            raise EmptyQueueWarning(target=self.waiting_queue)
        
        except TypeError:
            raise AbnormalTypeException(obj=audio)
        
        except StagedException as ero:
            self.waiting_queue.insert(0, ero.intercepted_audio)
            raise RetriveAudioWarning
        
        except Exception:
            print(traceback.format_exc())

    
    def leave(self) -> None:
        try:
            audio = self.stage_queue.dequeue()
            self.finished_queue.enqueue(audio=audio)
        
        except IndexError:
            raise EmptyQueueWarning(target=self.stage_queue)
        
        except TypeError:
            raise AbnormalTypeException(obj=audio)
        
        except StagedException as ero:
            self.waiting_queue.insert(0, ero.intercepted_audio)
            raise RetriveAudioWarning

        except Exception:
            print(traceback.format_exc())


    def backward(self) -> None:
        try:
            audio = self.stage_queue.dequeue()
    
        except IndexError:
            raise EmptyQueueWarning(target=self.stage_queue)
        
        except StagedException as ero:
            self.waiting_queue.insert(0, ero.intercepted_audio)
            raise RetriveAudioWarning

        except Exception:
            print(traceback.format_exc())


        try:
            self.waiting_queue.insert(index=0, audio=audio)
        
        except TypeError:
            raise AbnormalTypeException(obj=audio)
        
        except Exception:
            print(traceback.format_exc())

    
    def create_dummy(self) -> None:
        self.waiting_queue.insert(0, audio=AudioMetaData())


    @property
    def size(self) -> Tuple(int):
        return (len(self.finished_queue), len(self.stage_queue), len(self.waiting_queue))

    @property
    def queues(self) -> List[List[AudioMetaData]]:
        return [
            self.finished_queue.queue,
            self.stage_queue.queue,
            self.waiting_queue.queue
        ]