from __future__ import annotations

from incident_assistant.application.agent_runtime.runtime import AgentRuntime
from incident_assistant.domain.interfaces.agent import Agent
from incident_assistant.domain.value_objects.agent_context import AgentContext
from incident_assistant.domain.value_objects.agent_result import AgentResult


class SequentialAgentRuntime(AgentRuntime):

    def execute(
        self,
        agent: Agent,
        context: AgentContext,
    ) -> AgentResult:

        return agent.execute(context)