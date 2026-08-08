from __future__ import annotations

from openai import OpenAI

from incident_assistant.domain.interfaces.llm.llm import LLM


class OpenAILLM(LLM):

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
    ):
        self._client = OpenAI(
            api_key=api_key,
        )

        self._model = model

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert production "
                        "incident investigation assistant."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError(
                "LLM returned an empty response."
            )

        return content