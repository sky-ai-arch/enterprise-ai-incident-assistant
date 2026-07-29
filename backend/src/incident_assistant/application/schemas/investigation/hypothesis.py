from __future__ import annotations

from pydantic import BaseModel


class HypothesisResponse(BaseModel):

    title: str

    description: str

    confidence: float