from typing import (Tuple, Union)


class ConfigException:
    class NotAllowedModule(Exception):
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
            
            
 

    class ArgumentDuplication(Exception):...
