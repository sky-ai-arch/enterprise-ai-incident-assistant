from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from incident_assistant.application.agent_runtime.runtime import (
    AgentRuntime,
)
from incident_assistant.application.agent_runtime.runtime_registry import (
    RuntimeRegistry,
)
from incident_assistant.application.analyzers.investigation_analyzer import (
    InvestigationAnalyzer,
)
from incident_assistant.application.graph.investigation_state import (
    InvestigationGraphState,
)
from incident_assistant.domain.interfaces.planner import Planner


MAX_INVESTIGATION_ROUNDS = 2


class InvestigationGraph:

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

        self._graph = self._build_graph()

    # ---------------------------------------------------------
    # Graph construction
    # ---------------------------------------------------------

    def _build_graph(self):

        graph = StateGraph(
            InvestigationGraphState
        )

        graph.add_node(
            "planner",
            self._planning_node,
        )

        graph.add_node(
            "investigation",
            self._investigation_node,
        )

        graph.add_node(
            "analyzer",
            self._analysis_node,
        )

        graph.add_node(
            "reporter",
            self._reporting_node,
        )

        graph.add_edge(
            START,
            "planner",
        )

        graph.add_edge(
            "planner",
            "investigation",
        )

        graph.add_edge(
            "investigation",
            "analyzer",
        )

        graph.add_conditional_edges(
            "analyzer",
            self._route_after_analysis,
            {
                "continue": "planner",
                "finish": "reporter",
            },
        )

        graph.add_edge(
            "reporter",
            END,
        )

        return graph.compile()

    # ---------------------------------------------------------
    # Nodes
    # ---------------------------------------------------------

    def _planning_node(
        self,
        state: InvestigationGraphState,
    ) -> dict:

        plan = self._planner.create_plan(
            state["context"]
        )

        state["context"].metadata["plan"] = plan

        return {
            "context": state["context"],
        }

    def _investigation_node(
        self,
        state: InvestigationGraphState,
    ) -> dict:

        context = state["context"]

        plan = context.metadata["plan"]

        results = list(
            state.get("results", [])
        )

        for step in plan.steps:

            agent = self._registry.get(
                step.agent
            )

            result = self._runtime.execute(
                agent=agent,
                context=context,
            )

            results.append(result)

        return {
            "context": context,
            "results": results,
        }

    def _analysis_node(
        self,
        state: InvestigationGraphState,
    ) -> dict:

        context = state["context"]

        report = self._analyzer.analyze(
            context
        )

        context.report = report

        additional_investigation_required = (
            context.metadata.get(
                "additional_investigation_required",
                False,
            )
        )

        return {
            "context": context,
            "report": report,
            "additional_investigation_required": (
                additional_investigation_required
            ),
        }
    def _reporting_node(
        self,
        state: InvestigationGraphState,
    ) -> dict:

        reporter = self._registry.get(
            "reporter"
        )

        result = reporter.execute(
            context=state["context"],
            report=state["report"],
        )

        results = list(
            state.get("results", [])
        )

        results.append(result)

        return {
            "results": results,
        }

    # ---------------------------------------------------------
    # Conditional routing
    # ---------------------------------------------------------

    def _route_after_analysis(
        self,
        state: InvestigationGraphState,
    ) -> str:

        if not state.get(
            "additional_investigation_required",
            False,
        ):
            return "finish"

        current_round = state.get(
            "current_round",
            0,
        )

        if current_round >= MAX_INVESTIGATION_ROUNDS - 1:
            return "finish"

        state["current_round"] = current_round + 1

        return "continue"

    # ---------------------------------------------------------
    # Public execution API
    # ---------------------------------------------------------

    def execute(
        self,
        state: InvestigationGraphState,
    ) -> InvestigationGraphState:

        return self._graph.invoke(
            state
        )