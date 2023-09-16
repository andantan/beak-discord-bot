from typing import (List, Tuple, Set, Union)

from deprecated import deprecated

from Class.dataclass import ArgumentOption


class ConfigException(Exception): ...
class DeprecationClassException(DeprecationWarning): ...


class NotAllowedModule(ConfigException):
    def __init__(self, called: str, allowed: Union[str, Tuple[str]]):      
        self._called_module: str = called
        self._allowed_module: Union[str, Tuple[str]] = allowed

        super().__init__()


    def __str__(self) -> str:
        if isinstance(self._allowed_module, tuple):
            return f"Can only be called from module {self._allowed_module} (called module: \'{self._called_module}\')"
        
        return f"Can only be called from module \'{self._allowed_module}\' (called module: \'{self._called_module}\')"
        
        
    def __repr__(self) -> str:
        if isinstance(self._allowed_module, tuple):
            return f"Allowed module: {self._allowed_module} (called module: \'{self._called_module}\')"
        
        return f"Allowed module: \'{self._allowed_module}\' (called module: \'{self._called_module}\')"
    

    @property
    def called_module(self) -> str: 
        return tuple(self._called_module)
    
    @property
    def allowed_module(self) -> Tuple[str]:
        if isinstance(self._allowed_module, tuple):
            return self._allowed_module
        
        return tuple(self._allowed_module)
        

@deprecated(
    version = "v1.0.5.05", 
    reason = "Manually check duplicated argument changed to group argument",
    category = DeprecationClassException,
    action = "error"
)
class ArgumentConflict(ConfigException):
    def __init__(self, opts: List[ArgumentOption]) -> None:
        self._opts = opts

        super().__init__()


    def __str__(self) -> str:
        message_prefix: str = "Choose only one of mode"

        for _opt in self._opts:
            message_prefix += f"\n\t${_opt.flags} | {_opt.help}"
        else:
            return message_prefix
        
        
    def __repr__(self) -> str:
        return f"Conflict arguments: {self._opts}"


class AllocatedEnvironments(ConfigException):
    def __init__(self, conflicts: Set[str]) -> None:
        self._conflicts = conflicts

        super().__init__()


    def __str__(self) -> str:
        return f"Environment variables[{self._conflicts}] already assigned"
    

    def __repr__(self) -> str:
        return f"Assigned variables: [{self._conflicts}]"
        