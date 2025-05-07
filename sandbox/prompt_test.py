

import asyncio
import json
from llm.llm_client import call_llm

async def test_core_dilemma(card_name: str, meaning: str):
    messages = [
        {
            "role": "system",
            "content": "You are a narrative designer for a symbolic fantasy simulation. Your job is to generate a short, powerful core dilemma based on a tarot card's meaning."
        },
        {
            "role": "user",
            "content": (
                f"Card: {card_name}\n"
                f"Meaning: {meaning}\n\n"
                f"Return ONLY JSON like this:\n"
                f'{{ "core_dilemma": string }}\n\n'
                f"Example: {{ \"core_dilemma\": \"betraying a friend to protect a secret\" }}"
            )
        }
    ]

    response = await call_llm(messages, model="gpt-4o-mini")
    print("CORE DILEMMA RESULT:")
    print(response)

async def test_scenario(core_dilemma: str, card_name: str, meaning: str):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a fantasy scenario generator for a tarot-based game. You will receive a card name, its meaning, and a core dilemma. "
                "You must construct a short scenario (1–2 sentences) with the following:\n"
                "- A specific, named CATALYST (person, object, ritual, creature, etc.)\n"
                "- A visible CONSEQUENCE or threat\n"
                "- A RELATIONAL or EMOTIONAL STAKE (e.g., betrayal, love, legacy, sacrifice)\n"
                "- Logical consistency (avoid magic or consequence without explanation)\n"
                "- Clear tension driving a decision\n"
                "Then output 4 physical CHOICES that the player could take in response. Each must be behavioral and externally visible.\n\n"
                "Do not include passive options or purely emotional states.\n\n"
                "Return JSON ONLY in this format:\n"
                "{\n"
                "  \"core_dilemma\": string,\n"
                "  \"scenario\": string,\n"
                "  \"choices\": [ {\"text\": string, \"tag\": \"A\"|\"B\"|\"C\"|\"D\"} ],\n"
                "  \"complete\": boolean,\n"
                "  \"justification\": string (optional)\n"
                "}"
            )
        },
        {
            "role": "user",
            "content": (
                f"Card: {card_name}\nMeaning: {meaning}\nCore Dilemma: {core_dilemma}"
            )
        }
    ]

    response = await call_llm(messages, model="gpt-4o-mini")
    print("SCENARIO RESULT:")
    print(response)

# Example usage
if __name__ == "__main__":
    asyncio.run(test_core_dilemma("The Hanged Man", "Sacrifice, surrender, seeing from a new perspective"))
    asyncio.run(test_scenario(
        core_dilemma="giving up your position of power to save a friend",
        card_name="The Hanged Man",
        meaning="Sacrifice, surrender, seeing from a new perspective"
    ))