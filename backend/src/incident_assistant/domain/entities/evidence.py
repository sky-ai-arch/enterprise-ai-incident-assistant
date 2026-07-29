from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4


@dataclass
class Evidence:

    id: UUID = field(default_factory=uuid4)

    source: str = ""

    evidence_type: str = ""

    key: str = ""

    value: Any = None

    confidence: float = 1.0

    collected_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    metadata: dict[str, Any] = field(default_factory=dict)