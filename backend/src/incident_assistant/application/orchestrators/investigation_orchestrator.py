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
from incident_assistant.application.analyzers.investigation_analyzer import (
    InvestigationAnalyzer,
)


class InvestigationOrchestrator:

    def __init__(
        self,
        planner: Planner,
        runtime: AgentRuntime,
        registry: RuntimeRegistry,
        analyzer: InvestigationAnalyzer,

    ):
        self._planner = planner
        self._runtime = runtime
        self._registry = registry
        self._analyzer = analyzer
        

    def execute(
        self,
        context: AgentContext,
    ) -> InvestigationResult:

        plan = self._planner.create_plan(context)

        results = []

        # Execute all investigation agents
        for step in plan.steps:

            agent = self._registry.get(step.agent)

            result = self._runtime.execute(
                agent=agent,
                context=context,
            )

            results.append(result)

        # Analyze collected evidence
        report = self._analyzer.analyze(context)
        print(f"report: {report}")
        context.report = report

        # Execute reporter agent
        reporter = self._registry.get("reporter")

        reporter_result = reporter.execute(
            context=context,
            report=report,
        )

        results.append(reporter_result)
        print(f"reporter_result : {reporter_result}")
        return InvestigationResult(
            success=True,
            report=report,
            results=results,
        )