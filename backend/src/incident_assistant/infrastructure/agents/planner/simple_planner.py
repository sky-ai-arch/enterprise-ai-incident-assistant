from incident_assistant.domain.interfaces.planner import Planner
from incident_assistant.domain.value_objects.execution_plan import (
    ExecutionPlan,
    ExecutionStep,
)
from incident_assistant.domain.value_objects.agent_context import AgentContext


class SimplePlanner(Planner):

    def create_plan(
        self,
        context: AgentContext,
    ) -> ExecutionPlan:

        return ExecutionPlan(
            steps=[
                ExecutionStep(agent="metrics"),
                ExecutionStep(agent="logs"),
                ExecutionStep(agent="git"),
                ExecutionStep(agent="reporter"),
            ]
        )