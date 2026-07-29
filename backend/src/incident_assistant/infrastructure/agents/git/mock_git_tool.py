from datetime import UTC, datetime

from incident_assistant.domain.interfaces.tools.git_tools import GitTool
from incident_assistant.domain.value_objects.git_commit import GitCommit
from incident_assistant.domain.value_objects.git_result import GitResult


class MockGitTool(GitTool):

    def latest_commit(
        self,
        repository: str,
    ) -> GitResult:

        return GitResult(
            repository=repository,
            commits=[
                GitCommit(
                    sha="a7c91b2",
                    author="John Doe",
                    message="Increase API timeout",
                    timestamp=datetime.now(UTC),
                )
            ],
        )