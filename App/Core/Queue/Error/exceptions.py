from typing import List

from Class.dataclass import AudioMetaData

class QueueException(Exception): ...

class StagedException(QueueException):
    def __init__(self, intercepted_audio: List[AudioMetaData]) -> None:
        self.intercepted_audio = intercepted_audio
        super().__init__()
