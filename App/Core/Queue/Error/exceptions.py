from typing import List, TypeAlias

from Class.dataclass import AudioMetaData


AudiosMetaData: TypeAlias = List[AudioMetaData]


class QueueException(Exception): ...

class StagedException(QueueException):
    def __init__(self, intercepted_audio: AudiosMetaData) -> None:
        self.intercepted_audio = intercepted_audio
        super().__init__()
