from Class.abstractclass import QueueABC

class ControllerWarning(Warning): ...
class ControllerException(Exception): ...

class EmptyQueueWarning(ControllerWarning):
    def __init__(self, *, target: QueueABC) -> None:
        self.empty_queue = target.__class__
        super().__init__()

class RetriveAudioWarning(ControllerWarning): ...

class AbnormalTypeException(ControllerException):
    def __init__(self, *, obj: object) -> None:
        self.abnormal_object = obj.__class__
        super().__init__()