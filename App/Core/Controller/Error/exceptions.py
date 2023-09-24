from typing import List

from Class.abstractclass import QueueABC
from Class.dataclass import AudioMetaData

class ControllerWarning(Warning): ...
class ControllerException(Exception): ...

class EmptyWaitingWarning(ControllerWarning): ...
class EmptyStageWarning(ControllerWarning): ...
class EmptyFinishedWarning(ControllerWarning): ...


class RetriveAudioWarning(ControllerWarning):
    def __init__(self, intercepted: List[AudioMetaData]) -> None:
        self.intercepted = intercepted
        super().__init__()


class AbnormalTypeException(ControllerException):
    def __init__(self, *, obj: object) -> None:
        if isinstance(obj, list):
            for element in obj:
                if not isinstance(element, AudioMetaData):
                    self.abnormal_object = element.__class__
        else:
            self.abnormal_object = obj.__class__
        super().__init__()