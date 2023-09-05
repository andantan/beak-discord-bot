import os
import sys
import dotenv
import argparse

from types import FrameType
from typing import (List, Dict, Any)


def _config_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Beak discord utility bot arguments'
    )

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
    

def config_envs() -> None: 
    _allowed_module: str = "__main__"

    _fl: List[FrameType] = list(sys._current_frames().values())
    _f: FrameType = _fl.__getitem__(0)
    _g: Dict[str, Any] = _f.f_back.f_globals

    caller: str = _g.get("__name__")

    if not caller.__eq__(_allowed_module):
        from Error.exceptions import NotAllowedModule

        raise NotAllowedModule(called=caller, allowed=_allowed_module)
    
    args: argparse.Namespace = _config_args()

    dotenv.load_dotenv(verbose=True)

    for _k, _v in args.__dict__.items():
        os.environ.setdefault(_k, str(_v))
