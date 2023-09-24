from typing import (
    List, Tuple, Dict, 
    Union, Optional, Any,
    TypeAlias, TypeVar, Final,
    Generator
)

from discord import VoiceClient, FFmpegPCMAudio
from discord.errors import ClientException

from Class.dataclass import (
    AudioMetaData,
    PlaylistMetaData
)

from .Controller.controller import SyncedQueueController as Controller

from .Controller.Error.exceptions import EmptyWaitingWarning

from .Error.exceptions import (
    StopPlayer,
    NotConnectedException,
    AlreadyPlayingException
)



T: TypeAlias = TypeVar("T")

TypeInfo: TypeAlias = type
AudiosMetaData: TypeAlias = List[AudioMetaData]
AwaitableAudioMetaData: TypeAlias = Union[AudioMetaData, 
                                          PlaylistMetaData, 
                                          AudiosMetaData]


FFMPEG_OPTION: Final[Dict[str, str]] = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
    'options': '-vn'
}


class Player:
    __slots__ = (
        "vc",             # Beak VoiceClient
        "controller",     # SyncedQueueController
        "id",               # Guild identification
                            # =====================================
        "mode"              # Playing mode (Linear | Loop | Repeat)
                            # LIN_MODE = 0
                            # LOP_MODE = 1
                            # RPT_MODE = 2
                            # =====================================
    )


    def __init__(self, *, vc: VoiceClient, id: int) -> None:
        self.vc = vc
        self.id = id
        self.mode = 0
        self.controller = Controller(guild_identification=id)
        
        
    def __iter__(self) -> Generator[AudioMetaData, None, None]:
        for queue in self.controller:
            for audio in queue:
                yield audio
                
    
    def __str__(self) -> str:
        return f"Player({self.id}): size={self.controller.size}"
    
    
    def play_audio(self) -> None:
        try:
            staged_audio = self.controller.seek
            
            self.vc.play(FFmpegPCMAudio(
                source=staged_audio.audio_url, **FFMPEG_OPTION))
        
        except ClientException:
            if not self.vc.is_connected():
                raise NotConnectedException
        
            if self.vc.is_playing():
                raise AlreadyPlayingException

    
    def add_audio(self, source: AwaitableAudioMetaData) -> None:
        self.controller.wait(audio=source)
            

    def stage_audio(self) -> None:
        try:
            self.controller.stage()
                
        except EmptyWaitingWarning:
            raise StopPlayer
            
    
    def leave_audio(self) -> None:
        self.controller.leave()
        
        if self.is_repeat:
            self.controller.retrive()
        
        elif self.is_loop & self.controller.is_waiting_empty:
            self.controller.loop()
            
    
    def prev_audio(self) -> None:
        self.controller.backward()
        self.vc.stop()
    
    
    def shuffle_audio(self) -> None:
        self.controller.shuffle()
        
    
    def pause(self) -> None:
        self.vc.pause()
        
        
    def resume(self) -> None:
        self.vc.resume()
        
    
    def stop(self) -> None:
        self.vc.stop()
        
    
    def change_mode(self) -> None:
        self.mode = (self.mode + 1) % 3
    
    
    @property
    def is_linear(self) -> bool:
        return self.mode == 0
    @property
    def is_loop(self) -> bool:
        return self.mode == 1
    @property
    def is_repeat(self) -> bool:
        return self.mode == 2