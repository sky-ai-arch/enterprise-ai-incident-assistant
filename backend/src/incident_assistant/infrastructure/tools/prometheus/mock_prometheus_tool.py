from incident_assistant.domain.interfaces.tools.metrics_tools import MetricsTool
from incident_assistant.domain.value_objects.metrics_result import (
    MetricResult,
)

from incident_assistant.domain.value_objects.metric_sample import (
    MetricSample,
)


class MockPrometheusTool(MetricsTool):

    def query(
        self,
        expression: str,
    ) -> MetricResult:

        return MetricResult(
            query=expression,
            samples=[
                MetricSample(
                            labels={
                                "namespace": "production",
                                "pod": "api-server-7f98",
                            },
                            value=98,
                        )
                    ],
                )