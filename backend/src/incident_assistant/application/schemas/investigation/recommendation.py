from __future__ import annotations

from pydantic import BaseModel


class RecommendationResponse(BaseModel):

    title: str

    description: str

    priority: str