from __future__ import annotations

from pydantic import BaseModel


class FindingResponse(BaseModel):

    title: str

    description: str

    confidence: float

    evidence_keys: list[str]