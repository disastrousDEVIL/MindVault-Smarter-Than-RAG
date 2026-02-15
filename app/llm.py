"""OpenAI client wrapper for fact extraction and answer generation."""

import json

from openai import BadRequestError, OpenAI
from app.settings import settings


class LLMClient:
    """Wraps the OpenAI API for structured LLM calls."""

    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("LLM_API_KEY is not set in environment variables")

        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    def _json_chat_completion(self, system_prompt: str, user_prompt: str):
        """Request a completion and fallback if model lacks json_object support."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        try:
            return self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0,
                response_format={"type": "json_object"},
            )
        except BadRequestError as exc:
            message = str(exc)
            if "response_format" not in message or "not supported" not in message:
                raise
            # Fallback for models that do not support response_format=json_object.
            return self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0,
            )


    def extract_facts(self, prompt: str) -> str:
        """
        Calls OpenAI to extract atomic facts.
        Must return structured JSON as a string.
        """
        response = self._json_chat_completion(
            "You extract structured atomic facts from text.",
            prompt,
        )

        return response.choices[0].message.content

    def generate_answer(self, prompt: str) -> dict:
        """
        Calls OpenAI to generate an answer strictly from provided facts.
        Must return structured JSON.
        """
        response = self._json_chat_completion(
            "You answer questions using only the provided facts.",
            prompt,
        )

        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"answer": content, "sources": []}


llm_client = LLMClient()
