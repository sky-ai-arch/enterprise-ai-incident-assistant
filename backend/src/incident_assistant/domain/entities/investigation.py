from dataclasses import dataclass, field

from incident_assistant.domain.entities.evidence import Evidence


@dataclass(slots=True)
class Investigation:
    incident_id: str
    evidence: list[Evidence] = field(default_factory=list)
    probable_root_cause: str | None = None