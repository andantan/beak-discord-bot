class Block:
    class Instanctiating:
        def __new__(cls: type[object], *args, **kwargs) -> type[object]:
            raise TypeError(f"{cls.__name__} can not be instanctiated")