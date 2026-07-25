from __future__ import annotations

from abc import ABC, abstractmethod

from incident_assistant.domain.interfaces.agent import Agent
from incident_assistant.domain.value_objects.agent_context import AgentContext
from incident_assistant.domain.value_objects.agent_result import AgentResult


class AgentRuntime(ABC):

    @abstractmethod
    def execute(
        self,
        agent: Agent,
        context: AgentContext,
    ) -> AgentResult:
        ...