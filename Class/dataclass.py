import os
import collections

from typing import List, Optional, Generic, TypeVar, Any, Self
from dataclasses import dataclass, field

from deprecated import deprecated

from discord import Guild, Member, Interaction, VoiceState

from Tools.Decorator.dec import method_dispatch


T = TypeVar("T")


@deprecated(version="1.0.5.6c")
@dataclass(frozen=True)
class ArgumentOption(Generic[T]):
    dest: str
    flags: List[str]
    help: Optional[str]
    argument: T


@dataclass(slots=True, frozen=True, kw_only=True)
class InteractionProperty:
    itc: Interaction

    guild: Guild = field(init=False)
    guild_id: int = field(init=False)
    guild_name: str = field(init=False)

    author: Member = field(init=False)
    author_id: int = field(init=False)
    author_name: str = field(init=False)
    author_vc: Optional[VoiceState] = field(init=False)
    author_vc_id: Optional[int] = field(init=False)
    author_vc_name: Optional[str] = field(init=False)

    beak: Member = field(init=False)
    beak_vc: Optional[VoiceState] = field(init=False)
    beak_vc_id: Optional[int] = field(init=False)
    beak_vc_name: Optional[str] = field(init=False)


    def __post_init__(self) -> None:
        _beak = self.itc.guild.get_member(int(os.getenv("BEAK_IDENTIFICATION")))

        attributes = {
            "itc" : self.itc,
            "guild" : self.itc.guild,
            "guild_name" : self.itc.guild.name,
            "guild_id" : self.itc.guild.id,
            "author" : self.itc.user,
            "author_id" : self.itc.user.id,
            "author_name" : self.itc.user.name,
            "author_vc" : self.itc.user.voice,
            "author_vc_id" : self.itc.user.voice.channel.id if self.itc.user.voice else None,
            "author_vc_name" : self.itc.user.voice.channel.name if self.itc.user.voice else None,
            "beak" : _beak,
            "beak_vc" : _beak.voice,
            "beak_vc_id" : _beak.channel.id if _beak.voice else None,
            "beak_vc_name" : _beak.channel.name if _beak.voice else None
        }

        for _k, _v in attributes.items():
            object.__setattr__(self, _k, _v)


    @property
    def author_connected(self) -> bool: return bool(self.author_vc)
    @property
    def beak_connected(self) -> bool: return bool(self.beak_vc)
    @property
    def synced(self) -> bool:
        if not (self.author_connected and self.beak_connected):
            return False
        
        return self.author_vc_id == self.beak_vc_id


@dataclass(slots=True)
class GuildProperty:
    guild_id = None
    player = None
    message = None



@dataclass(slots=True, frozen=True, kw_only=True)
class AudioMetaData:
    title: Optional[str] = field(default=None)
    uploader: Optional[str] = field(default=None)
    duration: Optional[str] = field(default=None)

    original_url: Optional[str] = field(default=None)
    audio_url: Optional[str] = field(default=None)
    thumbnail_url: Optional[str] = field(default=None)


    @property
    def purity(self) -> bool:
        return all([getattr(self, v) for v in self.__slots__])
    @property
    def is_dummy(self) -> bool:
        return not any([getattr(self, v) for v in self.__slots__])
    

@dataclass(slots=True, kw_only=True)
class PlaylistMetaData(collections.Iterator):
    playlist_title: Optional[str] = field(default=None, init=False)
    playlist: List[AudioMetaData] = field(default_factory=list, init=False)
    seek: int = field(default=0, init=False)
    length: int = field(default=1, init=False)

    def __len__(self) -> int:
        return self.length


    def __iter__(self) -> Self:
        return self
    

    def __next__(self) -> AudioMetaData:
        if self.seek < self.length:
            _pointer = self.seek
            self.seek += 1

            return self.playlist[_pointer]
        else:
            raise StopIteration


    @method_dispatch
    def append(self, audio_meta_data: Any) -> None:
        raise TypeError(f"\"AudioMetaData | List[AudioMetaData]\" types are only allowed, but given {type(audio_meta_data)} type was given")


    @append.register(AudioMetaData)
    def _(self, audio_meta_data: AudioMetaData) -> None:
        self.playlist.append(audio_meta_data)
        self.length = len(self.playlist)


    @append.register(list)
    def _(self, audio_meta_data: List[AudioMetaData]) -> None:
        for element in audio_meta_data:
            if not isinstance(element, AudioMetaData):
                raise TypeError(f"\"AudioMetaData | List[AudioMetaData]\" types are only allowed, but given List[{type(element)}, Any] type was given")
        else:
            self.playlist = self.playlist + audio_meta_data[:]
            self.length = len(self.playlist)

    
    @property
    def is_playlist(self) -> bool:
        return bool(self.playlist_title)

