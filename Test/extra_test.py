from typing import (
    List, Tuple, Dict, 
    Union, Optional, 
    TypeAlias, TypeVar, 
    Generator, MutableSequence
)



T: TypeAlias = TypeVar("T")

TypeInfo: TypeAlias = type
ImmutableSequence: TypeAlias = Tuple
a = [1, 2, 3]
b = (1, 2, 3)

print(isinstance(a, MutableSequence))
print(isinstance(a, ImmutableSequence))
print(isinstance(b, MutableSequence))
print(isinstance(b, ImmutableSequence))