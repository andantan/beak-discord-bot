from typing import Any


class Singleton(type):
    _instance = {}
    
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if not cls in cls._instance:
            cls._instance[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            
        return cls._instance[cls]
