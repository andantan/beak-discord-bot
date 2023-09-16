import asyncio

from concurrent.futures import ThreadPoolExecutor

from typing import List, Dict, Any, Type, TypeVar, Optional


from yt_dlp import YoutubeDL

from Class.superclass import BlockingInstanctiate
from Class.dataclass import AudioMetaData, PlaylistMetaData

T = TypeVar("T", bound="YoutubeDlExtractor")


class YoutubeDlExtractor(BlockingInstanctiate):
    YTDL_OPTION: Dict[str, Any] = {
        'outtmpl': '%(title)s.%(uploader)s',
        "format": "bestaudio/best",
        "quiet": False
    }

    @classmethod
    async def get_playlist(cls: Type[T], URL: str, create_dummy: bool=False) -> PlaylistMetaData:
        if create_dummy: 
            return PlaylistMetaData()
        else: 
            return cls.create_playlist(data=await cls.extract(URL=URL), URL=URL)


    @classmethod
    async def extract(cls: Type[T], URL: str) -> Dict[str, Any]:
        ytdl = YoutubeDL(cls.YTDL_OPTION)
        ytdl.cache.remove()

        try:
            loop = asyncio.get_event_loop()

            with ThreadPoolExecutor() as pool:
                data = await loop.run_in_executor(pool, lambda: ytdl.extract_info(URL, download=False))
            
        except Exception as ERO:
            loop.close()

            print(ERO)

        return data
    

    @classmethod
    def create_playlist(cls: Type[T], data: Dict[str, Any], URL: str) -> PlaylistMetaData:

        def __get_audio_meta_data(entity: Dict[str, Any], URL: str, playlist_title: Optional[str]) -> AudioMetaData:
            return AudioMetaData(
                    title = entity.get("title"),
                    playlist_title = playlist_title,
                    uploader = entity.get("uploader"),
                    duration = entity.get("duration"),
                    original_url = URL,
                    audio_url = entity.get("url"),
                    thumbnail_url = entity.get("thumbnail")
                )
        
        playlist: PlaylistMetaData = PlaylistMetaData()

        if "playlist" in URL:
            playlist_entities: List[Dict[str, Any]] = data["entries"]

            playlist_title = playlist_entities[0]["playlist_title"]

            for entity in playlist_entities:
                playlist.append(__get_audio_meta_data(entity=entity, URL=URL, playlist_title=playlist_title))
                
        else:
            playlist.append(__get_audio_meta_data(entity=data, URL=URL, playlist_title=None))

        return playlist
