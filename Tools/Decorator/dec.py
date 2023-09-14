from typing import TypeAlias, Any, Callable, Unpack, TypedDict

from functools import singledispatch, update_wrapper

Method: TypeAlias = Callable[..., Any]

def method_dispatch(func: Method) -> Method:
    dispatcher = singledispatch(func)

    def wrapper(*args: Unpack[Any], **kwargs: Unpack[TypedDict]) -> Method:
        # args[0].__class__ == Self
        return dispatcher.dispatch(args[1].__class__)(*args, **kwargs)
    
    wrapper.register = dispatcher.register

    update_wrapper(wrapper, func)
    return wrapper
