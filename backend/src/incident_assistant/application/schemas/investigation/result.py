from __future__ import annotations

from pydantic import BaseModel


class AgentResultResponse(BaseModel):

    agent: str

    success: bool

    observations: list[str]