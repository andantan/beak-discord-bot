from dataclasses import dataclass, field
from typing import List

@dataclass(slots=True, kw_only=True, frozen=True)
class case:
    identification: int
    queue: List[int] = field(default_factory=list, init=False)


    def enqueue(self, index: int) -> None:
        self.queue.append(index)



a = case(identification=100)

print(a.queue)
a.enqueue(10)
print(a.queue)