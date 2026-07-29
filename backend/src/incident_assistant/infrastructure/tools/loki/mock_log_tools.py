from incident_assistant.domain.interfaces.tools.logs_tools import LogsTool
from incident_assistant.domain.value_objects.log_entry import LogEntry
from incident_assistant.domain.value_objects.log_result import LogResult


class MockLogsTool(LogsTool):

    def query(
        self,
        expression: str,
    ) -> LogResult:

        return LogResult(
            query=expression,
            entries=[
                LogEntry(
                    level="ERROR",
                    message="Out of memory exception",
                    labels={
                        "pod": "api-server-7f98",
                        "namespace": "production",
                    },
                ),
            ],
        )