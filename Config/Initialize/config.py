import os
import sys
import dotenv
import argparse

from types import FrameType
from typing import (
    List, Dict, Set, Tuple, 
    Any, TypeAlias, Union, Optional
)

from Error.exceptions import ConfigException

from Class.dataclass import ArgumentOption


ActionPairs: TypeAlias = Dict[str, ArgumentOption]
ArgumentConfigPair: TypeAlias = Dict[str, Tuple]
ArgumentConfigPairs: TypeAlias = List[Dict[str, Tuple]]
ArgumentType: TypeAlias = Union[int, float, str, bool, None]


def _config_args() -> argparse.ArgumentParser:
    # TODO
    # import argparse

    # parser = argparse.ArgumentParser()
    # optional = parser._action_groups.pop() #removes the optional arguments section
    # group1 = parser.add_argument_group("Required arguments")
    # group1 = group1.add_mutually_exclusive_group(required=True)
    # group1.add_argument('--enable',  action='store_true',  help='Enable something')
    # group1.add_argument('--disable', action='store_false', help='Disable something')
    # parser._action_groups.append(optional) # add optional arguments section again
    # args = parser.parse_args()

    parser = argparse.ArgumentParser(
        description='Beak discord utility bot arguments'
    )

    parser.add_argument(
        "-d", "--debug",
        dest = "DEBUG",
        action = "store_true",
        required = False,
        help = "[Run-mode] Run beak as debug mode - Only admin can execute commands"
    )

    parser.add_argument(
        "-p", "--patch",
        dest = "PATCH",
        action = "store_true",
        required = False,
        help = "[Run-mode] Run beak as patch mode - User can execute commands except play command"
    )

    parser.add_argument(
        "-j", "--joint",
        dest = "JOINT",
        action = "store_true",
        required = False,
        help = "[Run-mode] empty(joint)"
    )

    parser.add_argument(
        "-w", "--watch",
        dest = "FILE",
        action = "store_true",
        required = False,
        help = "[Run-mode] empty(watch)"
    )
    
    return parser


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
        raise ConfigException.NotAllowedModule(called=_caller, allowed=_allowed_module)

    if initialize:
        _arg_union: ArgumentConfigPairs = [
            {
                "dest": ("PATCH", "DEBUG", "FILE", "JOINT"),
                "type": "bool"
            }
        ]
        
        _pair = _parse_args()

        for _arg in _arg_union:
            match _arg["type"]:
                case "bool":
                    _opts: List[ArgumentOption] = [_pair[_dest] for _dest in _arg["dest"]]

                    if sum([int(_opt.argument) for _opt in _opts]) >= 2:
                        raise ConfigException.ArgumentConflict(opts=_opts)       
                case "str" | "int" | "float":
                    raise NotImplementedError
                case _:
                    raise TypeError

        dotenv.load_dotenv(verbose=True)

        for _dest, _opt in _pair.items():
            os.environ.setdefault(_dest, str(_opt.argument))
        
    if kwargs:
        config_env_keys: Set[str] = set(kwargs.keys())
        env_keys: Set[str] = set(os.environ.keys())

        if duplicated_env_keys := env_keys.intersection(config_env_keys):
            #TODO
            ...
        
        else:
            #TODO
            ...

