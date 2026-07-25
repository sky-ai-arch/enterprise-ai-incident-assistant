from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from uuid import UUID, uuid4


class IncidentSeverity(str, Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class IncidentStatus(str, Enum):
    OPEN = "OPEN"
    INVESTIGATING = "INVESTIGATING"
    MITIGATED = "MITIGATED"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class Environment(str, Enum):
    DEVELOPMENT = "development"
    QA = "qa"
    STAGING = "staging"
    PRODUCTION = "production"


class IncidentSource(str, Enum):
    MANUAL = "manual"
    API = "api"
    GRAFANA = "grafana"
    PROMETHEUS = "prometheus"
    PAGERDUTY = "pagerduty"
    GITHUB = "github"


@dataclass(slots=True)
class Incident:
    """
    Core business entity representing a production incident.

    This class intentionally contains NO database or FastAPI code.
    """

    id: UUID = field(default_factory=uuid4)

    title: str = ""
    description: str = ""

    severity: IncidentSeverity = IncidentSeverity.P3
    status: IncidentStatus = IncidentStatus.OPEN

    environment: Environment = Environment.DEVELOPMENT
    source: IncidentSource = IncidentSource.MANUAL

    service: str = ""

    created_by: str = ""
    assigned_to: str | None = None

    tags: list[str] = field(default_factory=list)

    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    resolved_at: datetime | None = None

    evidence_count: int = 0

    probable_root_cause: str | None = None

    confidence: float = 0.0

    def assign(self, investigator: str) -> None:
        """Assign the incident to an investigator."""
        self.assigned_to = investigator
        self.updated_at = datetime.now(UTC)

    def start_investigation(self) -> None:
        """Move the incident into investigation."""
        self.status = IncidentStatus.INVESTIGATING
        self.updated_at = datetime.now(UTC)

    def add_tag(self, tag: str) -> None:
        """Add a tag if it doesn't already exist."""
        tag = tag.strip().lower()

        if tag and tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now(UTC)

    def add_evidence(self) -> None:
        """Increment evidence counter."""
        self.evidence_count += 1
        self.updated_at = datetime.now(UTC)

    def resolve(self, root_cause: str) -> None:
        """Resolve the incident."""
        self.status = IncidentStatus.RESOLVED
        self.probable_root_cause = root_cause
        self.resolved_at = datetime.now(UTC)
        self.updated_at = self.resolved_at

        