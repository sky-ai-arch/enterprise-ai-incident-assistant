from dataclasses import dataclass, field


@dataclass(frozen=True)
class ExecutionStep:
    agent: str
    depends_on: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ExecutionPlan:
    steps: list[ExecutionStep] = field(default_factory=list)