from dataclasses import dataclass

@dataclass
class Situation:
    index: int
    place: str
    target: str
    reason: str