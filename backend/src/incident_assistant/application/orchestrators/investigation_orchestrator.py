from __future__ import annotations

from incident_assistant.application.agent_runtime.runtime import AgentRuntime
from incident_assistant.domain.interfaces.planner import Planner
from incident_assistant.domain.value_objects.agent_context import AgentContext
from incident_assistant.domain.value_objects.investigation_result import (
    InvestigationResult,
)
from incident_assistant.application.agent_runtime.runtime_registry import (
    RuntimeRegistry,
)



class InvestigationOrchestrator:

    def __init__(
        self,
        planner: Planner,
        runtime: AgentRuntime,
        registry: RuntimeRegistry,
    ):
        self._planner = planner
        self._runtime = runtime
        self._registry = registry

    def execute(
        self,
        context: AgentContext,
    ) -> InvestigationResult:

        plan = self._planner.create_plan(context)

        results = []

        for step in plan.steps:
            agent = self._registry.get(step.agent)

            result = self._runtime.execute(
                agent=agent,
                context=context,
            )

            results.append(result)

        return InvestigationResult(
            success=True,
            results=results,
        )