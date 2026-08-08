from __future__ import annotations

from google import genai

from incident_assistant.domain.interfaces.llm.llm import LLM


class GeminiLLM(LLM):

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-2.5-flash",
    ):
        self._client = genai.Client(
            api_key=api_key,
        )

        self._model = model

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
        )
        print(f"input: {prompt}\noutput : {response}")
        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return response.text