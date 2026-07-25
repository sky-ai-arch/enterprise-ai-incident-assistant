from __future__ import annotations

from abc import ABC, abstractmethod

from incident_assistant.domain.value_objects.agent_context import AgentContext


class Planner(ABC):

    @abstractmethod
    def create_plan(
        self,
        context: AgentContext,
    ) -> list[str]:
        ...