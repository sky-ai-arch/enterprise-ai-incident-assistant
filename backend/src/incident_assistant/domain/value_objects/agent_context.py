from __future__ import annotations
from .investigation_state import InvestigationState
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID




@dataclass
class AgentContext:

    request_id: UUID
    incident_id: UUID
    request: dict[str, Any]

    state: InvestigationState = field(
        default_factory=InvestigationState
    )

    metadata: dict[str, Any] = field(default_factory=dict)