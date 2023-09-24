from enum import Enum


class Playing_mode(Enum):
    __order__ = ""
    
    MODE_LIN: int = 0   # Playing playlist with linear mode
    MODE_LOP: int = 1   # Playing playlist with loop mode
    MODE_RPT: int = 2   # Playing playlist with repeat mode
