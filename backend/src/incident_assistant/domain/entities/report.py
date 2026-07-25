from dataclasses import dataclass


@dataclass(slots=True)
class Report:
    summary: str
    root_cause: str
    recommendation: str