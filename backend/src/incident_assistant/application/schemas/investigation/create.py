from __future__ import annotations

from pydantic import BaseModel


class CreateInvestigationRequest(BaseModel):
    incident_id: str