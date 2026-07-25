from __future__ import annotations

from pydantic import BaseModel


class InvestigationResponse(BaseModel):
    success: bool

    observations: list[str]