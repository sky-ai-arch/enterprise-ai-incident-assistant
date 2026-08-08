from incident_assistant.domain.interfaces.llm.llm import LLM


class MockLLM(LLM):

    def generate(
        self,
        prompt: str,
    ) -> str:

        return """
{
  "findings": [
    {
      "title": "High CPU utilization",
      "description": "CPU utilization reached 98% on the affected API server.",
      "confidence": 0.98,
      "evidence_keys": [
        "cpu_usage"
      ]
    },
    {
      "title": "Application memory failure",
      "description": "Application logs contain an out of memory exception.",
      "confidence": 0.99,
      "evidence_keys": [
        "error"
      ]
    },
    {
      "title": "Recent deployment",
      "description": "A recent deployment was detected before the incident.",
      "confidence": 0.95,
      "evidence_keys": [
        "last_commit"
      ]
    }
  ],
  "hypotheses": [
    {
      "title": "Resource exhaustion after deployment",
      "description": "The recent deployment may have introduced behavior causing increased resource consumption, resulting in memory exhaustion and critically high CPU utilization.",
      "confidence": 0.88,
      "evidence_keys": [
        "cpu_usage",
        "error",
        "last_commit"
      ]
    }
  ],
  "recommendations": [
    {
      "title": "Inspect recent deployment",
      "description": "Review commit 9d5bc7f for changes related to memory allocation, CPU consumption, or application startup behavior.",
      "priority": "HIGH",
      "evidence_keys": [
        "last_commit"
      ]
    },
    {
      "title": "Investigate memory consumption",
      "description": "Analyze the API server memory profile and identify the source of the out of memory exception.",
      "priority": "HIGH",
      "evidence_keys": [
        "error"
      ]
    },
    {
      "title": "Review CPU utilization",
      "description": "Inspect CPU-intensive operations on the affected API server.",
      "priority": "MEDIUM",
      "evidence_keys": [
        "cpu_usage"
      ]
    }
  ],
  "summary": "The incident appears to involve resource exhaustion on the API server. High CPU utilization and an out of memory exception were observed following a recent deployment."
}
"""