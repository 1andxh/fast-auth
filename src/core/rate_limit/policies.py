from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Ratelimit:
    limit: str
    key: Callable
