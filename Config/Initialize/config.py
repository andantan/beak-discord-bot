import os
import sys
import dotenv
import argparse

from types import FrameType
from typing import (List, Dict, Set, Tuple, Any, TypeAlias, Union)

from Error.exceptions import ConfigException


ArgumentType: TypeAlias = Union[int, float, str, bool, None]
ActionPair: TypeAlias = Dict[str, List[str]]


def _config_args() -> argparse.ArgumentParser:
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
        "--file",
        dest = "FILE",
        action = "store",
        required = False,
        help = "NOTHING"
    )
    
    return parser


def _parse_args() -> Tuple[argparse.Namespace, ActionPair]:
    _parser: argparse.ArgumentParser = _config_args()
    _namespace: argparse.Namespace = _parser.parse_args()
    _actions: List[argparse.Action] = _parser._actions

    dest_flags_pair: ActionPair = dict()

    for action in _actions:
        if not isinstance(action, argparse._HelpAction):
            destination: str = action.dest
            flags = action.option_strings
            argument: ArgumentType = _namespace.__getattribute__(destination)
            argument_type: ArgumentType = type(argument)
            
            # TODO: Classifier?
            # class City(NamedTuple):
            #     name: str
            #     population: int

            print(destination, flags, argument, argument_type, end="\n\n")

            dest_flags_pair.__setitem__(destination, flags)

    return (_namespace, dest_flags_pair)
    

def config_envs(initialize: bool=False, **kwargs) -> None: 
    _allowed_module: str = "__main__"

    _fl: List[FrameType] = list(sys._current_frames().values())
    _f: FrameType = _fl.__getitem__(0)
    _g: Dict[str, Any] = _f.f_back.f_globals

    caller: str = _g.get("__name__")

    if not caller.__eq__(_allowed_module):
        raise ConfigException.NotAllowedModule(called=caller, allowed=_allowed_module)

    if initialize:
        arg_duplicate_pair: List[Tuple[str]] = [
            ("PATCH", "DEBUG"),
        ]
        
        arg_parser: argparse.ArgumentParser
        arg_action_pair: ActionPair

        arg_parser, arg_action_pair = _parse_args()

        args: Dict[str, Any] = arg_parser.__dict__

        if args.__getitem__("PATCH") & args.__getitem__("DEBUG"):
            raise ConfigException.ArgumentConflict

        dotenv.load_dotenv(verbose=True)

        for _k, _v in args.items():
            os.environ.setdefault(_k, str(_v))
    
    if kwargs:
        config_env_keys: Set[str] = set(kwargs.keys())
        env_keys: Set[str] = set(os.environ.keys())

        if duplicated_env_keys := env_keys.intersection(config_env_keys):
            ...
        
        else:
            ...

