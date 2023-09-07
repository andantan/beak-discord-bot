from typing import (Tuple, Union)


class ConfigException:
    class NotAllowedModule(Exception):
        def __init__(self, called: str, allowed: Union[str, Tuple[str]]):            
            super().__init__(called, allowed)

    class ArgumentDuplication(Exception):...