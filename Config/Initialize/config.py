import os
import sys
import dotenv
import argparse

from types import FrameType
from typing import (
    List, Dict, Set, Tuple, 
    Any, TypeAlias, Union
)

from deprecated import deprecated

from Error.exceptions import (NotAllowedModule, AllocatedEnvironments)

from Class.dataclass import ArgumentOption


ActionPairs: TypeAlias = Dict[str, ArgumentOption]
ArgumentConfigPair: TypeAlias = Dict[str, Tuple]
ArgumentConfigPairs: TypeAlias = List[Dict[str, Tuple]]
ArgumentType: TypeAlias = Union[int, float, str, bool, None]


def _config_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Beak discord utility bot arguments'
    )

    _run_mode_group: argparse._ArgumentGroup = parser.add_argument_group(
        title = "Beak runtime mode",
        description = "Runtime mode for beak-system and beak-server as debugging | patch \n If no options run beak as normal-mode"
    )

    _run_mode_ex_group: argparse._MutuallyExclusiveGroup = \
        _run_mode_group.add_mutually_exclusive_group(required=False)

    _run_mode_ex_group.add_argument(
        "-d", "--debug",
        dest = "DEBUG",
        action = "store_true",
        required = False,
        help = "[Run-mode] Run beak as debug mode - Only admin can execute commands"
    )

    _run_mode_ex_group.add_argument(
        "-p", "--patch",
        dest = "PATCH",
        action = "store_true",
        required = False,
        help = "[Run-mode] Run beak as patch mode - User can execute commands except play command"
    )
    
    return parser


@deprecated(version="1.0.5.05", reason="Manually check duplicated argument changed to group argument")
def _parse_args() -> ActionPairs:
    _parser: argparse.ArgumentParser = _config_args()
    _namespace: argparse.Namespace = _parser.parse_args()
    _actions: List[argparse.Action] = _parser._actions

    args_pair: ActionPairs = dict()

    for action in _actions:
        if not isinstance(action, argparse._HelpAction):
            _dest: str = action.dest
            _arg: ArgumentType = _namespace.__dict__[_dest]

            args_pair[_dest] = ArgumentOption[type(_arg)](
                dest = _dest,
                flags = action.option_strings,
                help = action.help,
                argument = _arg
            )

    else:
        return args_pair
    

def config_envs(initialize: bool=False, **kwargs) -> None: 
    _allowed_module: str = "__main__"

    _fl: List[FrameType] = list(sys._current_frames().values())
    _f: FrameType = _fl.__getitem__(0)
    _g: Dict[str, Any] = _f.f_back.f_globals

    _caller: str = _g.get("__name__")

    if not _caller.__eq__(_allowed_module):
        raise NotAllowedModule(called=_caller, allowed=_allowed_module)

    if initialize:
        _parser: argparse.ArgumentParser = _config_args()
        _namespace: argparse.Namespace = _parser.parse_args()

        dotenv.load_dotenv(verbose=True)

        for kwarg in _namespace._get_kwargs():
            os.environ.setdefault(kwarg[0], str(kwarg[1]))
        
    if kwargs:
        config_env_keys: Set[str] = set(kwargs.keys())
        env_keys: Set[str] = set(os.environ.keys())

        if duplicated_env_keys := env_keys.intersection(config_env_keys):
            raise AllocatedEnvironments(conflicts=duplicated_env_keys)
            
        else:
            for _k, _v in kwargs.items():
                os.environ.setdefault(_k, str(_v))
