from llm.llm_client import call_llm
from typing import Dict, Optional, List
import json
from utils.tarot_examples import load_tarot_examples

async def generate_tarot_question(card_name: str, meaning: str, theme_question: str, history: Optional[List[Dict]] = None) -> Optional[Dict]:
    prompt = build_tarot_prompt(card_name, meaning, theme_question, history or [])
    examples = load_tarot_examples()
    examples_json = json.dumps(examples, indent=2)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a narrative arc generator in a fantasy simulation game. "
                "Each tarot draw contributes one step in a symbolic trial that defines the player's inner myth. "
                "You will receive a tarot card (with meaning and theme question) and the full history of previous draws. "
                "Use that history to evolve the symbolic arc — each scenario should build upon prior events and dilemmas. "
                "The result must feel like the next chapter in an unfolding inner journey. "
                "Return JSON only in this format:\n"
                "{\n"
                "  \"scenario\": string,\n"
                "  \"choices\": [ {\"text\": string, \"tag\": \"A\"|\"B\"|\"C\"|\"D\"}, ... ],\n"
                "  \"complete\": boolean,\n"
                "  \"justification\": string (optional, shown if complete is true)\n"
                "}\n\n"
                "Here are several reference examples for format and tone:\n"
                f"{examples_json}"
            )
        },
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

def build_tarot_prompt(card_name: str, meaning: str, question: str, history: List[Dict]) -> str:
    history_json = json.dumps(history, indent=2)
    return (
        f"You are a scenario generator for a fantasy simulation game. You will receive tarot draw history so far, "
        f"plus a new card to continue the symbolic arc. Build a brief dilemma and 4 labeled choices. "
        f"Afterward, decide if the arc is resolved. Return JSON matching this schema:\n\n"
        f"{{\n"
        f"  \"scenario\": string,\n"
        f"  \"choices\": [{{\"text\": string, \"tag\": \"A\"|\"B\"|\"C\"|\"D\"}}],\n"
        f"  \"complete\": boolean,\n"
        f"  \"justification\": string (if complete is true)\n"
        f"}}\n\n"
        f"Card: {card_name}\nMeaning: {meaning}\nQuestion: {question}\n\n"
        f"Prior Draws:\n{history_json}"
    )
