from llm.llm_client import call_llm
from typing import Dict, Optional, List
import json
import copy
from utils.tarot_examples import load_tarot_examples
import os
from pathlib import Path

def load_question_templates(path: str = "data/tarot_cards/question_templates.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

async def generate_core_dilemma(card_name: str, meaning: str, history: Optional[List[Dict]] = None) -> Optional[str]:
    templates = load_question_templates()
    sample = list(templates.values())[:2]  # take first two templates
    examples = "\n".join(
        f"- {t['question']} -> {t['choices'][0]}, {t['choices'][1]}, {t['choices'][2]}, {t['choices'][3]}"
        for t in sample
    )
    prompt = (
        f"You are a narrative designer in a symbolic fantasy game. Each tarot card represents a new moral or mythic tension in the player's journey.\n"
        f"Based on the card below, return ONLY a symbolic 'core dilemma' — the distilled tension the character must face. Keep it short and evocative (e.g., 'sacrificing a loved one for the greater good', 'seizing power at the cost of your soul').\n\n"
        f"Card: {card_name}\nMeaning: {meaning}\n\n"
        "{ \"core_dilemma\": string }"
    )
    messages = [
        {
            "role": "system",
            "content": (
                "You are a story seed engine. Your job is to distill a tarot card and its meaning into a concise core dilemma. "
                "Each core dilemma must:\n"
                "- Be a single declarative phrase (not a question).\n"
                "- Name at least one concrete catalyst (person, object, force, or event).\n"
                "- Imply a specific consequence or cost if unresolved.\n"
                "Return ONLY JSON like this:\n"
                '{ "core_dilemma": string }'
                "\n\nHere are example question-to-dilemma mappings:\n"
                f"{examples}\n"
            )
        },
        { "role": "user", "content": prompt }
    ]
    response = await call_llm(messages, model="gpt-4o-mini")
    if not response:
        print("No response from core dilemma generator.")
        return None
    try:
        if response.startswith("```") and response.endswith("```"):
            response = response.strip("`").strip()
            if response.startswith("json"):
                response = response[4:].strip()
        parsed = json.loads(response)
        return parsed.get("core_dilemma")
    except Exception as e:
        print(f"Failed to parse core dilemma: {e}")
        print("Raw response:")
        print(response)
        return None

async def generate_tarot_question(card_name: str, meaning: str, history: Optional[List[Dict]] = None) -> Optional[Dict]:
    if history:
        history = copy.deepcopy(history)
        for draw in history:
            draw.pop("question", None)

    core_dilemma = await generate_core_dilemma(card_name, meaning, history)
    if not core_dilemma:
        return None

    prompt = build_tarot_prompt(card_name, meaning, core_dilemma, history or [])
    messages = [
        {
            "role": "system",
            "content": (
                "You are a narrative arc generator. Each tarot draw adds one symbolic trial. "
                "You will receive a tarot card, a core dilemma, and prior draws. Use the core dilemma verbatim. "
                "Construct a single-sentence SCENARIO that:\n"
                "- Is under 80 characters total.\n"
                "- Uses generic descriptors (e.g., 'a merchant', 'a battlefield').\n"
                "- Includes one concrete CATALYST, one clear CONSEQUENCE, and one RELATIONAL or EMOTIONAL STAKE.\n\n"
                "Then provide exactly 4 CHOICES, each a brief action phrase (no punctuation) for example, in general:\n"
                "A. Accept the offer\n"
                "B. Reject the offer\n"
                "C. Perform a self-serving action unique to this catalyst\n"
                "D. Take an unexpected action that dramatically subverts the core dilemma\n\n"
                "Return ONLY JSON in this format:\n"
                "{\n"
                "  \"core_dilemma\": string,\n"
                "  \"scenario\": string,\n"
                "  \"choices\": [ {\"text\": string, \"tag\": \"A\"|\"B\"|\"C\"|\"D\"} ],\n"
                "  \"complete\": boolean,\n"
                "  \"justification\": string (optional)\n"
                "}"
            )
        },
        { "role": "user", "content": prompt }
    ]
    response = await call_llm(messages, model="gpt-4o-mini")
    if not response:
        print("No response from tarot engine.")
        return None

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

def build_tarot_prompt(card_name: str, meaning: str, core_dilemma: str, history: List[Dict]) -> str:
    history_json = json.dumps(history, indent=2)
    return (
        f"You are continuing a symbolic narrative arc in a tarot-based story game.\n"
        f"Card: {card_name}\nMeaning: {meaning}\n"
        f"Core Dilemma: {core_dilemma}\n\n"
        f"Use the core dilemma as the engine of the scene. Incorporate a symbolic catalyst that provokes the action.\n\n"
        f"Prior Draws:\n{history_json}"
    )
