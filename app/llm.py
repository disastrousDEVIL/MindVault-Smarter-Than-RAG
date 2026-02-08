"""OpenAI client wrapper for fact extraction and answer generation."""

from openai import OpenAI
from app.settings import settings


class LLMClient:
    """Wraps the OpenAI API for structured LLM calls."""

    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is not set")

        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    def extract_facts(self, prompt: str) -> dict:
        """
        Calls OpenAI to extract atomic facts.
        Must return structured JSON.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You extract structured atomic facts from text."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )

        return response.choices[0].message.content

    def generate_answer(self, prompt: str) -> dict:
        """
        Calls OpenAI to generate an answer strictly from provided facts.
        Must return structured JSON.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You answer questions using only the provided facts."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )

        return response.choices[0].message.content


llm_client = LLMClient()
