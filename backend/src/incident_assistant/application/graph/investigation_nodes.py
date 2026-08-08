from __future__ import annotations

from incident_assistant.application.agent_runtime.runtime import (
    AgentRuntime,
)
from incident_assistant.application.agent_runtime.runtime_registry import (
    RuntimeRegistry,
)
from incident_assistant.application.analyzers.investigation_analyzer import (
    InvestigationAnalyzer,
)
from incident_assistant.domain.value_objects.agent_context import (
    AgentContext,
)


class InvestigationNodes:

    def __init__(
        self,
        runtime: AgentRuntime,
        registry: RuntimeRegistry,
        analyzer: InvestigationAnalyzer,
    ):
        self._runtime = runtime
        self._registry = registry
        self._analyzer = analyzer

    def execute_agent(
        self,
        agent_name: str,
        context: AgentContext,
    ):
        agent = self._registry.get(agent_name)

        return self._runtime.execute(
            agent=agent,
            context=context,
        )

    def analyze(
        self,
        context: AgentContext,
    ):
        return self._analyzer.analyze(context)

    def report(
        self,
        context: AgentContext,
    ):
        reporter = self._registry.get("reporter")

        return reporter.execute(
            context=context,
            report=context.report,
        )