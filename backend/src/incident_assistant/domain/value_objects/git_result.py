from __future__ import annotations

from dataclasses import dataclass, field

from incident_assistant.domain.value_objects.git_commit import GitCommit


@dataclass(frozen=True)
class GitResult:
    repository: str
    commits: list[GitCommit] = field(default_factory=list)