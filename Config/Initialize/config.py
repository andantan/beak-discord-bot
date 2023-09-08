import os
import sys
import dotenv
import argparse

from types import FrameType
from typing import (
    List, Dict, Set, Tuple, 
    Any, TypeAlias, Union
)

from Error.exceptions import ConfigException

from Class.dataclass import ArgumentOption


ActionPairs: TypeAlias = Dict[str, ArgumentOption]
ArgumentConfigPair: TypeAlias = Dict[str, Tuple]
ArgumentConfigPairs: TypeAlias = List[Dict[str, Tuple]]
ArgumentType: TypeAlias = Union[int, float, str, bool, None]


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
        "-f", "--file",
        dest = "FILE",
        action = "store",
        required = False,
        help = "FOR DEBUGGING"
    )
    
    return parser


def _parse_args() -> ActionPairs:
    _parser: argparse.ArgumentParser = _config_args()
    _namespace: argparse.Namespace = _parser.parse_args()
    _actions: List[argparse.Action] = _parser._actions

    args_pair: ActionPairs = dict()

    for action in _actions:
        if not isinstance(action, argparse._HelpAction):
            _destination: str = action.dest
            _flags: List[str] = action.option_strings
            _argument: ArgumentType = _namespace.__getattribute__(_destination)
            _type = type(_argument)

            options = ArgumentOption[_type](
                flags = _flags,
                argument = _argument,
                types = _type
            )

            args_pair.__setitem__(_destination, options)
    else:
        return args_pair
    

def config_envs(initialize: bool=False, **kwargs) -> None: 
    _allowed_module: str = "__main__"

    _fl: List[FrameType] = list(sys._current_frames().values())
    _f: FrameType = _fl.__getitem__(0)
    _g: Dict[str, Any] = _f.f_back.f_globals

    caller: str = _g.get("__name__")

    if not caller.__eq__(_allowed_module):
        raise ConfigException.NotAllowedModule(called=caller, allowed=_allowed_module)

    if initialize:
        _arg_config_pairs: ArgumentConfigPairs = [
            {
                "dest": ("PATCH", "DEBUG", ),
                "type": (bool)
            }
        ]
        
        _pair = _parse_args()

        for config_pair in _arg_config_pairs:
            _duplicate_dest: Tuple[str] = config_pair.__getitem__("dest")
            _dest_type = config_pair.__getitem__("type")

            if _dest_type is bool:
                _arg_basket: List[bool] = list()

                for _dest in _duplicate_dest:
                    _opt: ArgumentOption = _pair.__getitem__(_dest)
                    _arg_basket.append(_opt.argument)

                else:
                    dest_len = len(_duplicate_dest)

                    if dest_len == 2 and all(_arg_basket):
                        raise ConfigException.ArgumentConflict
                    
                    elif dest_len >= 3:
                        count: int = 0

                        for _basket_element in _arg_basket:
                            count += int(_basket_element)

                            if count == 2:
                                raise ConfigException.ArgumentConflict
                
            elif _dest_type is str:
                raise NotImplementedError("_dest_type str type does not implemented")
            elif _dest_type is int:
                raise NotImplementedError("_dest_type int type does not implemented")
            elif _dest_type is float:
                raise NotImplementedError("_dest_type float type does not implemented")
            else:
                raise TypeError

            dotenv.load_dotenv(verbose=True)

            for dest, _opt in _pair.items():
                argument = _opt.argument

                os.environ.setdefault(dest, str(argument))
        
    if kwargs:
        config_env_keys: Set[str] = set(kwargs.keys())
        env_keys: Set[str] = set(os.environ.keys())

        if duplicated_env_keys := env_keys.intersection(config_env_keys):
            #TODO
            ...
        
        else:
            #TODO
            ...

