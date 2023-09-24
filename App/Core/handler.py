from typing import (
    List, Tuple,
    Union, 
    TypeAlias, TypeVar, 
    MutableSequence
)

from Class.dataclass import (
    AudioMetaData,
    PlaylistMetaData
)

T: TypeAlias = TypeVar("T")

TypeInfo: TypeAlias = type
ImmutableSequence: TypeAlias = Tuple

AudiosMetaData: TypeAlias = List[AudioMetaData]
AwaitableAudioMetaData: TypeAlias = Union[AudioMetaData, PlaylistMetaData, AudiosMetaData]


class Handler:
    __slots__ = ()
    
    @staticmethod
    def tender_sift(obj: MutableSequence[T], target: TypeInfo) -> List[T]:
        if not isinstance(obj, MutableSequence):
            raise TypeError
        
        return [element for element in obj if isinstance(obj, target)] 
        
        
    @staticmethod
    def concrete_sift(obj: ImmutableSequence[T], target: object) -> Tuple[T]:
        if not isinstance(obj, ImmutableSequence):
            raise TypeError
        
        return tuple([element for element in obj if isinstance(obj, target)]) 
