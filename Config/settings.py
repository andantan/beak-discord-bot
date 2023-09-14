from typing import Dict, Any

YTDL_OPTION: Dict[str, Any] = {
    'outtmpl': '%(title)s.%(uploader)s',
    "format": "bestaudio/best",
    'quiet': True
}
