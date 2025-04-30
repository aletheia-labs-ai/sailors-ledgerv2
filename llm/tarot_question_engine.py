from llm.llm_client import call_llm
from typing import Dict, Optional
import json

async def generate_tarot_question(card_name: str, meaning: str, theme_question: str) -> Optional[Dict]:
    prompt = build_tarot_prompt(card_name, meaning, theme_question)

    messages = [
        {"role": "system", "content": "You are a scenario generator for a fantasy simulation game. Given a tarot card, its meaning, and a thematic question, generate a brief scenario (1–2 sentences max) that places the user in a dilemma. The tone can be modern, fantasy, or sci-fi. Avoid verbosity. Provide exactly four emotionally or morally distinct multiple-choice options. Respond only in valid JSON."},
        {"role": "user", "content": prompt}
    ]

    response = await call_llm(messages, model="gpt-4o-mini")
    if not response:
        print("No response from tarot engine.")
        return None

    # Strip Markdown-style code block if present
    if response.startswith("```") and response.endswith("```"):
        response = response.strip("`").strip()
        if response.startswith("json"):
            response = response[4:].strip()

    try:
        return json.loads(response)
    except Exception as e:
        print(f"Failed to parse tarot scenario response: {e}")
        print("Raw response:")
        print(response)
        return None

def build_tarot_prompt(card_name: str, meaning: str, question: str) -> str:
    return (
        f"Tarot Card: {card_name}\n"
        f"Meaning: {meaning}\n"
        f"Theme Question: {question}\n\n"
        f"Return JSON in this format only:\n"
        f"{{\n"
        f"  \"scenario\": \"...\",\n"
        f"  \"choices\": [\"...\", \"...\", \"...\", \"...\"]\n"
        f"}}"
    )
