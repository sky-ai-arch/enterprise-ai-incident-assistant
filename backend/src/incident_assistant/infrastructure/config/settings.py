from __future__ import annotations

import os

from dotenv import load_dotenv


load_dotenv()


class Settings:

    @property
    def openai_api_key(self) -> str:
        value = os.getenv("OPENAI_API_KEY")

        if not value:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured."
            )

        return value


    @property
    def openai_model(self) -> str:
        return os.getenv(
            "OPENAI_MODEL",
            "gpt-4o-mini",
        )


    @property
    def gemini_api_key(self) -> str:
        value = os.getenv("GEMINI_API_KEY")

        if not value:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        return value


    @property
    def gemini_model(self) -> str:
        return os.getenv(
            "GEMINI_MODEL",
            "gAntigravity",
        )

settings = Settings()