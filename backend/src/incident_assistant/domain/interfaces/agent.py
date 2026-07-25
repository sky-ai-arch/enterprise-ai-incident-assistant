from __future__ import annotations

from abc import ABC, abstractmethod

from incident_assistant.domain.value_objects.agent_context import AgentContext
from incident_assistant.domain.value_objects.agent_result import AgentResult

class Agent(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def execute(
        self,
        context: AgentContext,
    ) -> AgentResult:
        ...