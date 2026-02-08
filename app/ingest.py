import json
from typing import List, Dict

from app.llm import llm_client


REQUIRED_FACT_FIELDS = {
    "subject",
    "relation",
    "object",
    "confidence",
    "source_document_id",
}


def build_extraction_prompt(
    document_id: str,
    title: str,
    content: str,
) -> str:
    """Builds a prompt for fact extraction."""
    return f"""
You are given a document.

Extract clear atomic facts from it.

Rules:
- Each fact must be a single, unambiguous statement
- Use simple relation verbs
- Do not invent facts
- Do not explain anything

Return ONLY valid JSON in this format:

{{
  "facts": [
    {{
      "subject": "string",
      "relation": "string",
      "object": "string",
      "confidence": 0.0,
      "source_document_id": "{document_id}"
    }}
  ]
}}

Document title:
{title}

Document content:
{content}
"""


def validate_facts(
    facts: List[Dict],
    document_id: str,
) -> List[Dict]:
    """Validates extracted facts."""
    valid_facts = []
    seen = set()

    for fact in facts:
        # Field check
        if not REQUIRED_FACT_FIELDS.issubset(fact.keys()):
            continue

        # Basic value validation
        if not all(str(fact[k]).strip() for k in ["subject", "relation", "object"]):
            continue

        if fact["source_document_id"] != document_id:
            continue

        if not (0.0 <= float(fact["confidence"]) <= 1.0):
            continue

        # Dedup within document
        dedup_key = (
            fact["subject"].lower(),
            fact["relation"].lower(),
            fact["object"].lower(),
        )

        if dedup_key in seen:
            continue

        seen.add(dedup_key)
        valid_facts.append(fact)

    return valid_facts


def ingest_document(
    document_id: str,
    title: str,
    content: str,
) -> List[Dict]:
    """Ingest a document and extract facts."""
    prompt = build_extraction_prompt(document_id, title, content)

    raw_response = llm_client.extract_facts(prompt)

    try:
        parsed = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise RuntimeError("LLM returned invalid JSON") from exc

    facts = parsed.get("facts", [])
    if not isinstance(facts, list):
        raise RuntimeError("Invalid facts format")

    validated_facts = validate_facts(facts, document_id)

    if not validated_facts:
        raise RuntimeError("No valid facts extracted")

    return validated_facts