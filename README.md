# enterprise-ai-incident-assistant
# Enterprise AI Incident Assistant

An AI-powered production incident investigation system that automatically collects evidence from infrastructure and application sources, analyzes the evidence using an LLM, generates root-cause hypotheses and recommended actions, and produces a structured investigation report.

The system is designed around a **multi-agent architecture**, with **LangGraph-based orchestration**, a **planner-driven investigation workflow**, and an **LLM-powered investigation analyzer**.

---

## 1. Overview

Production incidents usually require engineers to correlate information from multiple systems:

* Infrastructure metrics
* Application logs
* Recent deployments
* Application/runtime state
* Historical investigation information

Manually correlating this information is time-consuming and can delay incident resolution.

The Enterprise AI Incident Assistant automates the initial investigation process.

The system:

1. Receives an incident investigation request.
2. Creates an investigation context.
3. Creates an investigation plan.
4. Executes specialized investigation agents.
5. Collects evidence from different sources.
6. Builds an evidence-aware investigation prompt.
7. Sends the evidence to an LLM.
8. Converts the LLM response into a strongly typed investigation report.
9. Evaluates the resulting hypotheses.
10. Can trigger additional targeted investigation rounds.
11. Generates a final report through the Reporter Agent.
12. Returns the structured result through a FastAPI API.

---

# 2. High-Level Architecture

```text
                         ┌──────────────────────┐
                         │      FastAPI API     │
                         │ POST /investigations │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Investigation       │
                         │  Orchestrator        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     LangGraph        │
                         │ Investigation Graph  │
                         └──────────┬───────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     │                             │
                     ▼                             ▼
             ┌───────────────┐             ┌──────────────┐
             │    Planner    │             │ Investigation│
             │               │             │    State     │
             └───────┬───────┘             └──────────────┘
                     │
          ┌──────────┼───────────┐
          │          │           │
          ▼          ▼           ▼
      Metrics      Logs         Git
       Agent       Agent        Agent
          │          │           │
          ▼          ▼           ▼
     Prometheus     Loki       GitHub
          │          │           │
          └──────────┼───────────┘
                     │
                     ▼
              Evidence Collection
                     │
                     ▼
             ┌───────────────┐
             │ LLM Analyzer  │
             │               │
             │ Prompt Builder│
             │      +        │
             │ Gemini / LLM  │
             └───────┬───────┘
                     │
                     ▼
          InvestigationReport
          ┌──────────┼──────────┐
          │          │          │
       Findings  Hypotheses Recommendations
                     │
                     ▼
              Decision / Routing
                     │
            ┌────────┴─────────┐
            │                  │
            ▼                  ▼
      More Investigation      Finish
            │                  │
            ▼                  ▼
       Targeted Agents     Reporter Agent
                               │
                               ▼
                        Final Investigation
                              Report
                               │
                               ▼
                         FastAPI Response
```

---

# 3. Core Design Principles

The project follows several important architectural principles.

### Separation of concerns

Each layer has a specific responsibility.

```text
API
 ↓
Application
 ↓
Domain
 ↓
Infrastructure
```

The domain layer does not depend on FastAPI, Gemini, Prometheus, Loki, GitHub, or other infrastructure implementations.

---

### Dependency inversion

Agents depend on interfaces rather than concrete implementations.

For example:

```text
MetricsAgent
     ↓
MetricsTool
     ↓
PrometheusTool / MockPrometheusTool
```

This allows production integrations to be replaced with mocks during development and testing.

---

### Structured data instead of raw LLM output

The LLM does not directly control the API response.

Instead:

```text
LLM
 ↓
JSON
 ↓
Domain objects
 ↓
InvestigationReport
 ↓
Reporter
 ↓
API schema
```

This makes the system easier to validate, test, and extend.

---

# 4. Project Structure

A simplified project structure is:

```text
backend/
│
├── src/
│   └── incident_assistant/
│
│       ├── api/
│       │   ├── dependencies.py
│       │   └── routers/
│       │       └── v1/
│       │           └── investigations.py
│       │
│       ├── application/
│       │
│       │   ├── analyzers/
│       │   │   └── investigation_analyzer.py
│       │   │
│       │   ├── graph/
│       │   │   └── investigation_graph.py
│       │   │
│       │   ├── orchestrators/
│       │   │   └── investigation_orchestrator.py
│       │   │
│       │   ├── prompts/
│       │   │   └── investigation_prompt_builder.py
│       │   │
│       │   ├── mappers/
│       │   │   └── investigation_mapper.py
│       │   │
│       │   ├── schemas/
│       │   │   └── investigation/
│       │   │
│       │   └── agent_runtime/
│       │
│       ├── domain/
│       │
│       │   ├── entities/
│       │   │   └── evidence.py
│       │   │
│       │   ├── interfaces/
│       │   │   ├── agent.py
│       │   │   ├── planner.py
│       │   │   ├── tools/
│       │   │   └── llm/
│       │   │
│       │   ├── repositories/
│       │   │
│       │   └── value_objects/
│       │       ├── agent_context.py
│       │       ├── agent_result.py
│       │       ├── finding.py
│       │       ├── hypothesis.py
│       │       ├── recommendation.py
│       │       ├── investigation_report.py
│       │       ├── investigation_result.py
│       │       └── investigation_state.py
│       │
│       └── infrastructure/
│
│           ├── agents/
│           │   ├── metrics/
│           │   ├── logs/
│           │   ├── git/
│           │   ├── planner/
│           │   └── reporter/
│           │
│           ├── tools/
│           │   ├── prometheus/
│           │   ├── loki/
│           │   └── git/
│           │
│           ├── llm/
│           │   ├── gemini_llm.py
│           │   ├── openai_llm.py
│           │   └── mock_llm.py
│           │
│           └── persistence/
│
└── README.md
```

---

# 5. Investigation Context

The investigation is represented using `AgentContext`.

Conceptually:

```text
AgentContext
│
├── request_id
├── incident_id
├── request
├── metadata
│
└── state
    │
    ├── evidence
    ├── observations
    ├── artifacts
    └── report
```

The context is passed throughout the investigation.

This prevents individual agents from maintaining disconnected state.

---

# 6. Investigation State

The investigation state represents the accumulated information during the investigation.

Important components include:

### Evidence

Evidence collected from:

* Prometheus
* Loki
* Git

Example:

```json
{
  "source": "prometheus",
  "type": "metric",
  "key": "cpu_usage",
  "value": 98,
  "confidence": 0.98,
  "metadata": {
    "namespace": "production",
    "pod": "api-server-7f98"
  }
}
```

---

### Observations

Agents can also add human-readable observations.

Example:

```text
CPU utilization is critically high (98%).
Error log detected: Out of memory exception.
Recent deployment detected.
```

---

### Report

After analysis:

```text
InvestigationState
        │
        └── report
              │
              ├── findings
              ├── hypotheses
              ├── recommendations
              └── summary
```

---

# 7. Investigation Agents

The system currently has specialized agents.

## Metrics Agent

Responsible for collecting infrastructure metrics.

Current mock example:

```text
CPU = 98%
```

The Metrics Agent communicates through a `MetricsTool` interface.

This allows:

```text
MetricsTool
    ├── MockPrometheusTool
    └── PrometheusTool
```

The mock implementation is useful during development.

---

## Logs Agent

Responsible for collecting application/runtime logs.

Example:

```text
ERROR: Out of memory exception
```

The agent communicates through:

```text
LogsTool
```

Possible implementations:

```text
MockLogsTool
LokiLogsTool
```

---

## Git Agent

Responsible for collecting deployment/code-change information.

Example:

```text
Last commit:
9d5bc7f
```

The agent communicates through a Git tool abstraction.

---

## Reporter Agent

The Reporter Agent is responsible for producing the final report artifact after investigation and analysis.

It receives:

```text
InvestigationReport
```

and stores it in the investigation state/artifacts.

The Reporter Agent does not perform root-cause analysis.

Its responsibility is reporting.

---

# 8. Planner

The planner decides which investigation agents should execute.

The initial plan is:

```text
Metrics
Logs
Git
```

This provides the initial evidence set.

The planner can also use previous investigation hypotheses to determine whether additional targeted investigation is required.

For example:

```text
Hypothesis:
Memory leak introduced by recent deployment

        ↓

Planner

        ↓

Metrics + Logs + Git
```

This creates the basis for iterative investigation.

---

# 9. Investigation Analyzer

The `InvestigationAnalyzer` is the component that converts raw collected evidence into structured reasoning.

It receives:

```text
AgentContext
```

and uses:

```text
InvestigationPromptBuilder
        +
LLM
```

The analyzer generates:

```text
Findings
Hypotheses
Recommendations
Summary
```

---

# 10. Prompt Builder

The `InvestigationPromptBuilder` converts internal investigation state into an LLM prompt.

It serializes:

```text
Evidence
+
Observations
```

into structured JSON.

The LLM is instructed to return only the expected JSON structure.

Example:

```json
{
  "findings": [],
  "hypotheses": [],
  "recommendations": [],
  "summary": ""
}
```

This keeps the LLM interaction deterministic and easier to parse.

---

# 11. LLM Layer

The project uses an LLM abstraction.

Conceptually:

```text
LLM Interface
     │
     ├── MockLLM
     ├── GeminiLLM
     └── OpenAILLM
```

The application depends on the interface rather than directly depending on Gemini or OpenAI.

This is important because the LLM provider can be changed without rewriting the analyzer.

---

# 12. Example LLM Analysis

Given:

```text
CPU = 98%

OOM exception

Recent deployment = 9d5bc7f
```

the LLM may infer:

### Finding

```text
Critical CPU Utilization
```

### Finding

```text
Out of Memory Exception
```

### Finding

```text
Recent Deployment
```

### Hypothesis

```text
Memory Leak in Recent Deployment
```

### Recommendation

```text
Rollback Deployment
```

The resulting domain object becomes:

```text
InvestigationReport
│
├── Finding
│   ├── Critical CPU Utilization
│   ├── Out of Memory Exception
│   └── Recent Deployment
│
├── Hypothesis
│   └── Memory Leak in Recent Deployment
│
├── Recommendation
│   ├── Rollback Deployment
│   └── Scale Pod Resources
│
└── Summary
```

---

# 13. LangGraph

LangGraph is responsible for controlling the investigation workflow.

Instead of simply executing:

```text
Agent A
 ↓
Agent B
 ↓
Agent C
 ↓
Report
```

the graph can represent:

```text
Planner
   ↓
Investigation Agents
   ↓
Analyzer
   ↓
Decision
   │
   ├── More investigation
   │       ↓
   │   Planner
   │
   └── Investigation complete
           ↓
        Reporter
```

This is one of the most important architectural features of the project.

It allows the system to become **iterative rather than purely sequential**.

---

# 14. Targeted Investigation

Suppose the first investigation produces:

```text
Hypothesis:
Memory leak caused by recent deployment

Confidence:
0.55
```

If the confidence is below the configured investigation threshold, the graph can decide that more evidence is required.

The planner can then create another plan.

For example:

```text
Round 1

Metrics
Logs
Git
 ↓
LLM
 ↓
Hypothesis:
Possible memory leak
Confidence = 0.55
 ↓
More investigation required
 ↓
Round 2
 ↓
Metrics
Logs
Git
 ↓
LLM
 ↓
Updated report
```

This is the beginning of an actual **agentic investigation loop**.

---

# 15. Investigation Report

The central domain object is:

```text
InvestigationReport
```

It contains:

```text
findings
hypotheses
recommendations
summary
```

A finding contains:

```text
title
description
confidence
evidence_keys
```

A hypothesis contains:

```text
title
description
confidence
evidence_keys
```

A recommendation contains:

```text
title
description
priority
evidence_keys
```

The `evidence_keys` provide traceability between reasoning and collected evidence.

For example:

```text
Hypothesis
    │
    ├── cpu_usage
    ├── error
    └── last_commit
```

This is important for explainability.

---

# 16. End-to-End Request Flow

A request arrives at:

```text
POST /api/v1/investigations
```

Example:

```json
{
  "incident_id": "..."
}
```

The FastAPI router creates:

```text
AgentContext
```

with:

```text
request_id
incident_id
request
```

Then:

```text
orchestrator.execute(context)
```

is called.

---

# 17. Orchestrator

The `InvestigationOrchestrator` is the application-level coordinator.

Its job is not to perform investigation itself.

It coordinates:

```text
Planner
Graph
Agents
Analyzer
Reporter
```

In the current architecture, the orchestrator delegates workflow execution to the investigation graph.

Conceptually:

```text
API
 ↓
InvestigationOrchestrator
 ↓
InvestigationGraph
```

---

# 18. Investigation Graph Execution

The graph maintains the investigation workflow.

Typical sequence:

```text
START
  ↓
PLANNER
  ↓
METRICS
  ↓
LOGS
  ↓
GIT
  ↓
ANALYZER
  ↓
DECISION
```

Then:

```text
DECISION
   │
   ├── More investigation
   │       ↓
   │    PLANNER
   │
   └── Complete
           ↓
        REPORTER
           ↓
          END
```

---

# 19. Evidence Collection

During the first round:

### Metrics Agent

adds:

```text
cpu_usage = 98
```

### Logs Agent

adds:

```text
error = Out of memory exception
```

### Git Agent

adds:

```text
last_commit = 9d5bc7f
```

The state now contains:

```text
Evidence
│
├── cpu_usage
├── error
└── last_commit
```

and observations:

```text
CPU utilization is critically high.
Error log detected.
Recent deployment detected.
```

---

# 20. LLM Analysis

The analyzer receives the accumulated state.

The prompt builder creates something similar to:

```text
You are an expert production incident investigation agent.

Analyze the collected incident evidence.

Evidence:
[...]

Observations:
[...]

Identify:

1. Findings
2. Root-cause hypotheses
3. Recommended actions
4. Overall summary

Return ONLY valid JSON.
```

The LLM generates structured JSON.

---

# 21. Parsing LLM Output

The raw LLM response is not exposed directly to the API.

Instead:

```text
Raw LLM response
       ↓
JSON parsing
       ↓
Finding
Hypothesis
Recommendation
       ↓
InvestigationReport
```

This is an important design decision.

It prevents the API from becoming dependent on raw LLM response formatting.

---

# 22. Reporter

Once the investigation is complete:

```text
InvestigationReport
        ↓
ReporterAgent
```

The Reporter Agent creates/stores the final report artifact.

The report is then included in the investigation result.

---

# 23. API Mapping

The API does not directly expose domain objects.

Instead:

```text
InvestigationResult
       ↓
InvestigationMapper
       ↓
InvestigationResponse
```

The mapper converts application/domain objects into API schemas.

This keeps the API layer independent from the internal domain representation.

---

# 24. Example Final Response

The current richer API response can look conceptually like:

```json
{
  "success": true,
  "report": {
    "findings": [
      {
        "title": "Critical CPU Utilization",
        "description": "CPU usage for api-server-7f98 has reached 98%.",
        "confidence": 0.98,
        "evidence_keys": [
          "cpu_usage"
        ]
      },
      {
        "title": "Out of Memory Exception",
        "description": "An Out of Memory exception was detected.",
        "confidence": 1.0,
        "evidence_keys": [
          "error"
        ]
      }
    ],
    "hypotheses": [
      {
        "title": "Memory Leak in Recent Deployment",
        "description": "The recent deployment may have introduced a memory leak.",
        "confidence": 0.55,
        "evidence_keys": [
          "cpu_usage",
          "error",
          "last_commit"
        ]
      }
    ],
    "recommendations": [
      {
        "title": "Rollback Deployment",
        "description": "Rollback the recent deployment.",
        "priority": "HIGH",
        "evidence_keys": [
          "last_commit",
          "error",
          "cpu_usage"
        ]
      }
    ],
    "summary": "The incident is likely related to a recent deployment."
  }
}
```

---

# 25. Why This Architecture Is Agentic

This project is not simply:

```text
LLM → answer
```

Instead:

```text
Incident
   ↓
Planner
   ↓
Specialized Agents
   ↓
Evidence
   ↓
LLM Reasoning
   ↓
Hypotheses
   ↓
Decision
   ↓
Targeted Investigation
   ↓
Updated Evidence
   ↓
LLM Reasoning
   ↓
Final Report
```

The important characteristic is the **feedback loop**.

The output of one reasoning step can influence what happens next.

---

# 26. Why Multiple Agents?

Each agent has a specialized responsibility.

```text
Metrics Agent
    → infrastructure state

Logs Agent
    → application behavior

Git Agent
    → deployment/code changes

Planner
    → investigation strategy

Analyzer
    → reasoning

Reporter
    → final presentation
```

This makes the system easier to extend.

For example, future agents could include:

```text
Trace Agent
Database Agent
Kubernetes Agent
Cloud Agent
Security Agent
Dependency Agent
```

without redesigning the entire system.

---

# 27. Mock Infrastructure

The project currently supports mock tools.

Examples:

```text
MockPrometheusTool
MockLogsTool
MockGitTool
MockLLM
```

This allows the entire investigation workflow to be developed without requiring all production integrations.

For example:

```text
MetricsAgent
      ↓
MetricsTool
      ↓
MockPrometheusTool
```

Later:

```text
MetricsAgent
      ↓
MetricsTool
      ↓
PrometheusTool
```

The agent itself does not need to change.

---

# 28. Dependency Injection

Dependencies are assembled in:

```text
api/dependencies.py
```

The dependency layer creates:

```text
LLM
PromptBuilder
Analyzer
Agents
Registry
Planner
Graph
Orchestrator
```

This gives the application a centralized composition root.

For example:

```text
GeminiLLM
     ↓
InvestigationAnalyzer
     ↓
InvestigationGraph
     ↓
InvestigationOrchestrator
```

---

# 29. Technology Stack

### Backend

* Python
* FastAPI
* Pydantic

### Agent orchestration

* LangGraph

### AI

* Gemini
* OpenAI-compatible LLM abstraction
* Mock LLM

### Observability sources

* Prometheus
* Loki
* Git/GitHub

### Architecture

* Domain-driven design principles
* Dependency inversion
* Interface-based integrations
* Dependency injection
* Multi-agent architecture

---

# 30. Current Development Strategy

The project intentionally uses mocks during development.

This allows the investigation architecture to be validated before connecting every production system.

The development path is:

```text
Mock Tools
   ↓
Working Investigation Architecture
   ↓
LLM Integration
   ↓
Agentic Loop
   ↓
Real Prometheus/Loki/Git integrations
   ↓
Production Hardening
```

---

# 31. Future Improvements

Potential next steps include:

### Production integrations

* Real Prometheus queries
* Real Loki queries
* GitHub API integration
* Kubernetes integration

### Agent improvements

* Dedicated Kubernetes agent
* Trace analysis agent
* Database investigation agent
* Deployment diff agent

### Agentic reasoning

* Confidence-based routing
* Maximum investigation rounds
* Evidence gap detection
* Hypothesis verification
* Hypothesis ranking

### Reliability

* LLM retries
* Timeout handling
* Circuit breakers
* Structured output validation
* Rate limiting
* Request tracing

### Persistence

* PostgreSQL
* Incident history
* Investigation history
* Previous hypotheses
* Similar incident retrieval

### RAG

A future RAG layer can provide historical incident knowledge:

```text
Current Incident
      ↓
Evidence
      ↓
Retrieve Similar Incidents
      ↓
Historical Context
      ↓
LLM
      ↓
Improved Investigation
```

---

# 32. Key Architectural Flow

The most important flow to understand is:

```text
FastAPI
   ↓
AgentContext
   ↓
InvestigationOrchestrator
   ↓
InvestigationGraph
   ↓
Planner
   ↓
Investigation Agents
   ↓
Evidence
   ↓
Investigation Analyzer
   ↓
Prompt Builder
   ↓
LLM
   ↓
Structured JSON
   ↓
InvestigationReport
   ↓
Decision
   │
   ├── More investigation → Planner
   │
   └── Complete → Reporter
                         ↓
                  InvestigationResult
                         ↓
                    API Mapper
                         ↓
                  FastAPI Response
```

This is the central architecture of the project.

---

# 33. Example Incident

Consider:

```text
Incident:
API service experiencing elevated latency.
```

The initial investigation discovers:

```text
CPU = 98%
OOM exception
Recent deployment = 9d5bc7f
```

The LLM generates:

```text
Finding:
Critical CPU utilization

Finding:
Out of memory exception

Finding:
Recent deployment

Hypothesis:
Potential memory leak introduced by deployment

Confidence:
0.55
```

The graph can determine:

```text
0.55 < investigation threshold
```

and trigger another investigation.

The second round can collect additional evidence.

The final analyzer then reassesses the hypothesis.

If confidence increases:

```text
0.55
 ↓
0.87
```

the hypothesis becomes strongly supported.

If confidence decreases:

```text
0.55
 ↓
0.21
```

the system can reject the original hypothesis and investigate alternative causes.

---

# 34. Summary

The Enterprise AI Incident Assistant is designed as an extensible, multi-agent production incident investigation platform.

The core workflow is:

```text
Collect
   ↓
Correlate
   ↓
Reason
   ↓
Hypothesize
   ↓
Investigate
   ↓
Validate
   ↓
Report
```

The most important architectural idea is that **the LLM is a reasoning component, not the entire system**.

The deterministic parts of the system are responsible for:

* collecting evidence
* maintaining state
* selecting agents
* controlling workflow
* validating output
* producing API responses

The LLM is responsible primarily for:

* interpreting evidence
* generating findings
* generating hypotheses
* recommending actions
* summarizing the incident

This separation makes the system significantly more maintainable and suitable for evolving toward a production-grade incident investigation platform.
