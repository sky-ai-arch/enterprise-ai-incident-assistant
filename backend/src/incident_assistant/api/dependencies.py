from __future__ import annotations

from incident_assistant.application.agent_runtime.runtime import AgentRuntime
from incident_assistant.application.agent_runtime.runtime_registry import (
    RuntimeRegistry,
)
from incident_assistant.application.agent_runtime.sequential_runtime import (
    SequentialAgentRuntime,
)
from incident_assistant.application.analyzers.investigation_analyzer import (
    InvestigationAnalyzer,
)
from incident_assistant.application.orchestrators.investigation_orchestrator import (
    InvestigationOrchestrator,
)
from incident_assistant.application.prompts.investigation_prompt_builder import (
    InvestigationPromptBuilder,
)

from incident_assistant.domain.interfaces.llm.llm import LLM
from incident_assistant.domain.interfaces.planner import Planner
from incident_assistant.domain.repositories.incident_repository import (
    IncidentRepository,
)

from incident_assistant.infrastructure.agents.git.git_agent import GitAgent
from incident_assistant.infrastructure.agents.logs.logs_agent import LogsAgent
from incident_assistant.infrastructure.agents.metrics.metrics_agent import (
    MetricsAgent,
)
from incident_assistant.infrastructure.agents.planner.simple_planner import (
    SimplePlanner,
)
from incident_assistant.infrastructure.agents.reporter.reporter_agent import (
    ReporterAgent,
)

from incident_assistant.infrastructure.llm.openai_llm import (
    OpenAILLM,
)
from incident_assistant.infrastructure.llm.gemini_llm import (
    GeminiLLM,
)

from incident_assistant.infrastructure.config.settings import (
    settings,
)
from incident_assistant.infrastructure.persistence.memory.incident_repository import (
    InMemoryIncidentRepository,
)

from incident_assistant.infrastructure.tools.git.mock_git_tool import (
    MockGitTool,
)
from incident_assistant.infrastructure.tools.loki.mock_log_tools import (
    MockLogsTool,
)
from incident_assistant.infrastructure.tools.prometheus.mock_prometheus_tool import (
    MockPrometheusTool,
)

from incident_assistant.application.graph.investigation_graph import (
    InvestigationGraph,
)

from incident_assistant.application.graph.investigation_nodes import (
    InvestigationNodes,
)
from incident_assistant.application.graph.investigation_graph import (
    InvestigationGraph,
)
# ------------------------------------------------------------------
# Singletons
# ------------------------------------------------------------------

_repository: IncidentRepository | None = None
_runtime_registry: RuntimeRegistry | None = None
_llm: LLM | None = None
_prompt_builder: InvestigationPromptBuilder | None = None
_analyzer: InvestigationAnalyzer | None = None


# ------------------------------------------------------------------
# Repository
# ------------------------------------------------------------------
def get_investigation_graph() -> InvestigationGraph:

    return InvestigationGraph(
        planner=get_planner(),
        runtime=get_agent_runtime(),
        registry=get_runtime_registry(),
        analyzer=get_investigation_analyzer(),
    )

def get_incident_repository() -> IncidentRepository:
    global _repository

    if _repository is None:
        _repository = InMemoryIncidentRepository()

    return _repository


# ------------------------------------------------------------------
# LLM
# ------------------------------------------------------------------

def get_llm() -> LLM:
    global _llm

    if _llm is None:
        _llm = GeminiLLM(
            api_key=settings.gemini_api_key,
            model=settings.gemini_model,
        )

    return _llm

# ------------------------------------------------------------------
# Investigation Prompt Builder
# ------------------------------------------------------------------

def get_prompt_builder() -> InvestigationPromptBuilder:
    global _prompt_builder

    if _prompt_builder is None:
        _prompt_builder = InvestigationPromptBuilder()

    return _prompt_builder


# ------------------------------------------------------------------
# Investigation Analyzer
# ------------------------------------------------------------------

def get_investigation_analyzer() -> InvestigationAnalyzer:
    global _analyzer

    if _analyzer is None:
        _analyzer = InvestigationAnalyzer(
            llm=get_llm(),
            prompt_builder=get_prompt_builder(),
        )

    return _analyzer


# ------------------------------------------------------------------
# Runtime Registry
# ------------------------------------------------------------------

def get_runtime_registry() -> RuntimeRegistry:
    global _runtime_registry

    if _runtime_registry is None:
        registry = RuntimeRegistry()

        # Metrics
        metrics_tool = MockPrometheusTool()
        registry.register(
            MetricsAgent(metrics_tool)
        )

        # Logs
        logs_tool = MockLogsTool()
        registry.register(
            LogsAgent(logs_tool)
        )

        # Git
        git_tool = MockGitTool()
        registry.register(
            GitAgent(git_tool)
        )

        # Reporter
        registry.register(
            ReporterAgent()
        )

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
        graph=get_investigation_graph(),
    ) 