from __future__ import annotations

import json

from incident_assistant.domain.interfaces.llm.llm import LLM
from incident_assistant.domain.value_objects.agent_context import AgentContext
from incident_assistant.domain.value_objects.investigation_report import (
    InvestigationReport,
)
from incident_assistant.application.prompts.investigation_prompt_builder import (
    InvestigationPromptBuilder,
)


class InvestigationAnalyzer:

    def __init__(
        self,
        llm: LLM,
        prompt_builder: InvestigationPromptBuilder,
    ):
        self._llm = llm
        self._prompt_builder = prompt_builder

    def analyze(
        self,
        context: AgentContext,
    ) -> InvestigationReport:

        prompt = self._prompt_builder.build(context)

        response = self._llm.generate(prompt)

        return self._parse_response(response)

    def _parse_response(
        self,
        response: str,
    ) -> InvestigationReport:

        data = json.loads(response)

        return InvestigationReport.from_dict(data)
    
    def analyze(
        self,
        context: AgentContext,
    ) -> InvestigationReport:

        prompt = self._prompt_builder.build(context)

        response = self._llm.generate(prompt)

        report = self._parse_response(response)

        context.metadata["additional_investigation_required"] = (
            any(
                hypothesis.confidence < 0.70
                for hypothesis in report.hypotheses
            )
        )

        return report

    def _requires_additional_investigation(
        self,
        report: InvestigationReport,
    ) -> bool:

        if not report.hypotheses:
            return False

        for hypothesis in report.hypotheses:
            if hypothesis.confidence < 0.70:
                return True

        return False