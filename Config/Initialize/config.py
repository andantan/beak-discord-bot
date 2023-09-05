import os
import sys
import dotenv
import argparse

from types import FrameType
from typing import (List, Dict, Any)

from Config.Initialize.vars import ArgumentsNamespace

from Error.exceptions import NotAllowedModule

def config_args() -> ArgumentsNamespace:
    _allowed_module = "__main__"

    _fl: List[FrameType] = list(sys._current_frames().values())
    _f: FrameType = _fl.__getitem__(0)
    _g: Dict[str, Any] = _f.f_back.f_globals

    caller: str = _g.get("__name__")

    if not caller.__eq__(_allowed_module):
        raise NotAllowedModule(called=caller, allowed=_allowed_module)

    parser = argparse.ArgumentParser(description='Beak discord utility bot arguments')

    parser.add_argument(
        "-d", "--debug",
        dest="DEBUG",
        action="store_true",
        required=False,
        help="Run beak as debug mode - Only admin can execute commands"
    )

    parser.add_argument(
        "-p", "--patch",
        dest="PATCH",
        action="store_true",
        required=False,
        help="Run beak as patch mode - User can execute commands except play command"
    )

    return parser.parse_args()
    

def config_envs(arguments: ArgumentsNamespace) -> None: 
    _allowed_module = "__main__"

    _fl: List[FrameType] = list(sys._current_frames().values())
    _f: FrameType = _fl.__getitem__(0)
    _g: Dict[str, Any] = _f.f_back.f_globals

    caller: str = _g.get("__name__")

    if not caller.__eq__(_allowed_module):
        raise NotAllowedModule(called=caller, allowed=_allowed_module)
    
    if not isinstance(arguments, argparse.Namespace):
        raise TypeError

    dotenv.load_dotenv(verbose=True)

    for _k, _v in arguments.__dict__.items():
        os.environ.setdefault(_k, str(_v))
