import os

from typing import (
    List, Optional, Generic, TypeVar
)

from dataclasses import dataclass, field

from deprecated import deprecated

from discord import (Guild, Member, Interaction, VoiceState)
from discord.channel import (VoiceChannel, StageChannel)

T = TypeVar("T")


@deprecated(version="1.0.5.6c")
@dataclass(frozen=True)
class ArgumentOption(Generic[T]):
    dest: str
    flags: List[str]
    help: Optional[str]
    argument: T


@dataclass(frozen=True)
class GuildProperties:
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
