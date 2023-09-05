from typing import Any


class Singleton(type):
    _instance = {}
    
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if not cls in cls._instance:
            cls._instance[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            
        return cls._instance[cls]


class Block:
    class Instanctiating:
        def __new__(cls: type[object], *args, **kwargs) -> type[object]:
            raise TypeError(f"{cls.__name__} can not be instanctiated")