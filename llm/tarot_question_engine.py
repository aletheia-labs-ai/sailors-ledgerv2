from llm.llm_client import call_llm
from typing import Dict, Optional, List
import json
import copy
from utils.tarot_examples import load_tarot_examples

async def generate_core_dilemma(card_name: str, meaning: str, history: Optional[List[Dict]] = None) -> Optional[str]:
    prompt = (
        f"You are a narrative designer in a symbolic fantasy game. Each tarot card represents a new moral or mythic tension in the player's journey.\n"
        f"Based on the card below, return ONLY a symbolic 'core dilemma' — the distilled tension the character must face. Keep it short and evocative (e.g., 'sacrificing a loved one for the greater good', 'seizing power at the cost of your soul').\n\n"
        f"Card: {card_name}\nMeaning: {meaning}\n\n"
        f"Return JSON with only this structure:\n"
        f"{{ \"core_dilemma\": string }}"
    )
    messages = [
        { "role": "system", "content": "You generate distilled symbolic conflicts for a tarot-based story game." },
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
                "You are a narrative arc generator in a fantasy simulation game. Each tarot draw contributes one symbolic trial. "
                "You will receive a tarot card, a symbolic dilemma, and prior draws. Use the dilemma to drive the scene.\n\n"
                "Write a SCENARIO (1–2 sentences max) centered on a present decision. The scenario must:\n"
                "- Be grounded in a dramatic moment with visible tension\n"
                "- Include a named CATALYST: a specific person, object, ritual, creature, or force that causes the conflict\n"
                "- Include a CONSEQUENCE: what is threatened, gained, or lost\n"
                "- Include a RELATIONAL or EMOTIONAL STAKE: betrayal, love, fear, legacy, sacrifice, etc.\n"
                "- Avoid vague settings (e.g., 'a festival') unless made highly specific or unusual\n"
                "- Avoid internal states or reflection as the main driver\n\n"
                "Then provide exactly 4 physical CHOICES, each labeled A-D. Each must be a concrete action the player takes in response to the scenario. "
                "Do NOT use passive verbs (e.g., 'think', 'feel', 'reflect'). Use strong, outward verbs: 'strike', 'burn', 'steal', 'flee', 'confront', etc.\n\n"
                "Return ONLY JSON matching this format:\n"
                "{\n"
                "  \"core_dilemma\": string,\n"
                "  \"scenario\": string,\n"
                "  \"choices\": [ {\"text\": string, \"tag\": \"A\"|\"B\"|\"C\"|\"D\"} ],\n"
                "  \"complete\": boolean,\n"
                "  \"justification\": string (optional, only if complete is true)\n"
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
