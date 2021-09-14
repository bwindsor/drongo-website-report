import dataclasses
from typing import Optional


@dataclasses.dataclass
class Section:
    title: Optional[str]
    content: str
