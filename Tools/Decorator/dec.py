from typing import TypeAlias, Any, Callable, TypeVar, ParamSpec

from functools import singledispatch, update_wrapper


T = TypeVar("T")
P = ParamSpec("P")

Method: TypeAlias = Callable[..., Any]


def method_dispatch(func: Callable[P, T]) -> Callable[P, T]:
    dispatcher = singledispatch(func)

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Method:
        # args[0].__class__ == Self
        return dispatcher.dispatch(args[1].__class__)(*args, **kwargs)
    
    wrapper.register = dispatcher.register

    update_wrapper(wrapper, func)
    return wrapper
