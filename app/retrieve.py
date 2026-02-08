"""Retrieve and prune facts for question answering."""

from typing import Dict, List

from app.memory import retrieve_facts


CONFIDENCE_THRESHOLD = 0.3
MAX_FACTS = 20


def retrieve_context(question: str) -> List[Dict]:
    """
    Retrieve relevant atomic facts for a given question.
    Applies pruning and limits.
    """
    # Step 1: Get raw facts from memory
    raw_facts = retrieve_facts(query=question, limit=MAX_FACTS * 2)

    if not raw_facts:
        return []

    # Step 2: Prune by confidence
    filtered = [
        fact
        for fact in raw_facts
        if float(fact.get("confidence", 0)) >= CONFIDENCE_THRESHOLD
    ]

    # Step 3: Deduplicate facts
    seen = set()
    deduped = []

    for fact in filtered:
        key = (
            fact.get("subject", "").lower(),
            fact.get("relation", "").lower(),
            fact.get("object", "").lower(),
        )

        if key in seen:
            continue

        seen.add(key)
        deduped.append(fact)

        if len(deduped) >= MAX_FACTS:
            break

    return deduped
