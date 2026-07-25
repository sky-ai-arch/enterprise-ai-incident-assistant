from __future__ import annotations

from incident_assistant.application.agent_runtime.runtime import AgentRuntime
from incident_assistant.application.agent_runtime.sequential_runtime import (
    SequentialAgentRuntime,
)
from incident_assistant.application.orchestrators.investigation_orchestrator import (
    InvestigationOrchestrator,
)
from incident_assistant.domain.interfaces.planner import Planner
from incident_assistant.domain.repositories.incident_repository import (
    IncidentRepository,
)
from incident_assistant.infrastructure.agents.git.git_agent import GitAgent
from incident_assistant.infrastructure.agents.logs.logs_agent import LogsAgent
from incident_assistant.infrastructure.agents.metrics.metrics_agent import MetricsAgent
from incident_assistant.infrastructure.agents.planner.simple_planner import (
    SimplePlanner,
)
from incident_assistant.infrastructure.agents.reporter.reporter_agent import (
    ReporterAgent,
)
from incident_assistant.infrastructure.persistence.memory.incident_repository import (
    InMemoryIncidentRepository,
)
from incident_assistant.application.agent_runtime.runtime_registry import (
    RuntimeRegistry,
)

# ------------------------------------------------------------------
# Repository Singleton
# ------------------------------------------------------------------

_repository: IncidentRepository | None = None


def get_incident_repository() -> IncidentRepository:
    global _repository

    if _repository is None:
        _repository = InMemoryIncidentRepository()

    return _repository


# ------------------------------------------------------------------
# Runtime Registry Singleton
# ------------------------------------------------------------------

_runtime_registry: RuntimeRegistry | None = None


def get_runtime_registry() -> RuntimeRegistry:
    global _runtime_registry

    if _runtime_registry is None:
        registry = RuntimeRegistry()

        registry.register(MetricsAgent())
        registry.register(LogsAgent())
        registry.register(GitAgent())
        registry.register(ReporterAgent())

        _runtime_registry = registry

    return _runtime_registry


# ------------------------------------------------------------------
# Planner
# ------------------------------------------------------------------

def get_planner() -> Planner:
    return SimplePlanner()


# ------------------------------------------------------------------
# Runtime
# ------------------------------------------------------------------

def get_agent_runtime() -> AgentRuntime:
    return SequentialAgentRuntime()


# ------------------------------------------------------------------
# Investigation Orchestrator
# ------------------------------------------------------------------

def get_investigation_orchestrator() -> InvestigationOrchestrator:
    return InvestigationOrchestrator(
        planner=get_planner(),
        runtime=get_agent_runtime(),
        registry=get_runtime_registry(),
    )