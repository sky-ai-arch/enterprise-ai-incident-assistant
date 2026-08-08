from __future__ import annotations

from incident_assistant.domain.interfaces.planner import Planner
from incident_assistant.domain.value_objects.agent_context import AgentContext
from incident_assistant.domain.value_objects.execution_plan import (
    ExecutionPlan,
    ExecutionStep,
)


class SimplePlanner(Planner):

    def create_plan(
        self,
        context: AgentContext,
    ) -> ExecutionPlan:

        # --------------------------------------------------
        # First investigation round
        # --------------------------------------------------
        # No report means we have not performed the initial
        # investigation yet.
        if context.state.report is None:

            return ExecutionPlan(
                steps=[
                    ExecutionStep(agent="metrics"),
                    ExecutionStep(agent="logs"),
                    ExecutionStep(agent="git"),
                ]
            )

        # --------------------------------------------------
        # Targeted investigation based on previous report
        # --------------------------------------------------

        steps: list[ExecutionStep] = []

        for hypothesis in context.state.report.hypotheses:

            title = hypothesis.title.lower()
            description = hypothesis.description.lower()

            # --------------------------------------------------
            # Memory-related hypothesis
            # --------------------------------------------------
            if (
                "memory" in title
                or "memory" in description
                or "oom" in title
                or "out of memory" in description
            ):
                steps.append(
                    ExecutionStep(
                        agent="metrics"
                    )
                )

                steps.append(
                    ExecutionStep(
                        agent="logs"
                    )
                )

            # --------------------------------------------------
            # Deployment-related hypothesis
            # --------------------------------------------------
            if (
                "deployment" in title
                or "deployment" in description
                or "commit" in title
                or "commit" in description
            ):
                steps.append(
                    ExecutionStep(
                        agent="git"
                    )
                )

        # --------------------------------------------------
        # Avoid an empty investigation plan
        # --------------------------------------------------

        if not steps:
            steps = [
                ExecutionStep(
                    agent="metrics"
                )
            ]

        return ExecutionPlan(
            steps=steps
        )
