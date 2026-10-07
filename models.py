from dataclasses import dataclass, field
from enum import Enum


class Route(str, Enum):
    PYTHON = "PYTHON"
    DATABRICKS = "DATABRICKS"
    BOTH = "BOTH"
    UNSUPPORTED = "UNSUPPORTED"


@dataclass
class Evidence:
    source: str
    topic: str
    content: str
    score: float | None = None


@dataclass
class SpecialistResult:
    specialist: str
    evidence: list[Evidence] = field(default_factory=list)

    @property
    def has_evidence(self) -> bool:
        return bool(self.evidence)
