from abc import ABC, abstractmethod

from incident_assistant.domain.value_objects.git_result import GitResult


class GitTool(ABC):

    @abstractmethod
    def latest_commit(
        self,
        repository: str,
    ) -> GitResult:
        raise NotImplementedError