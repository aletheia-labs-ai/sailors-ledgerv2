from llm.llm_client import call_llm
from typing import Dict, Optional
import json

async def generate_world_narrative_update(world_summary: Dict) -> Optional[Dict]:
    prompt = build_narrative_prompt(world_summary)

    messages = [
        {"role": "system", "content": "You are a world narrative engine. Respond with a short summary and town-specific narrative and spirit changes in structured JSON."},
        {"role": "user", "content": prompt}
    ]

    response = await call_llm(messages, model="gpt-4o")
    if response:
        try:
            return json.loads(response)
        except Exception as e:
            print(f"Failed to parse narrative response: {e}")
            return None
    return None

def build_narrative_prompt(summary: Dict) -> str:
    return f"Given this world summary:\n\n{summary}\n\nReturn a JSON object with an 'event_summary' string and a 'town_updates' object mapping town names to narrative updates and spirit changes."

async def generate_seeded_world_state(arc_summary: str) -> Optional[Dict]:
    prompt = build_seed_prompt(arc_summary)

    messages = [
        {"role": "system", "content": (
            "You are a fantasy world generator. You will receive a tarot-based Seed Packet. "
            "Extract symbolic themes and use them as inspiration—do not copy player answers or card names literally. "
            "Generate exactly three towns. Each must include:\n"
            "- A symbolic town name (use as JSON key, not inside object)\n"
            "- A 'narrative': 1–2 sentence description of the town’s identity and tone\n"
            "- A 'spirit': short poetic phrase representing the town’s governing energy or mood\n\n"
            "Respond only with valid JSON in this exact format:\n\n"
            "{\n"
            "  \"towns\": {\n"
            "    \"TownName1\": { \"narrative\": \"...\", \"spirit\": \"...\" },\n"
            "    \"TownName2\": { \"narrative\": \"...\", \"spirit\": \"...\" },\n"
            "    \"TownName3\": { \"narrative\": \"...\", \"spirit\": \"...\" }\n"
            "  }\n"
            "}\n\n"
            "Do not use lists or arrays. Town names must be the dictionary keys. Do not include markdown. Respond with pure JSON only."
        )},
        {"role": "user", "content": prompt}
    ]

    response = await call_llm(messages, model="gpt-4o")
    if not response:
        print("No response from LLM.")
        return None

    # Strip Markdown-style code block wrappers
    if response.startswith("```") and response.endswith("```"):
        response = response.strip("`").strip()
        if response.startswith("json"):
            response = response[4:].strip()

    try:
        return json.loads(response)
    except Exception as e:
        print(f"Failed to parse seed generation response: {e}")
        print("Raw response:")
        print(response)
        return None

def build_seed_prompt(arc_summary: str) -> str:
    return (
        f"You are a fantasy world generator. Use the following symbolic narrative arc to define the mood and themes of a new world. "
        f"Generate three distinct towns that symbolically reflect or contrast with this arc. "
        f"Do not reference tarot cards, characters, or specific events — instead, reflect symbolic qualities, such as transformation, rebirth, deception, intuition, or strength. "
        f"Each town must have:\n"
        f"- A symbolic name (used as dictionary key)\n"
        f"- A 'narrative': 1–2 sentence poetic description of the town’s tone and identity\n"
        f"- A 'spirit': short phrase representing its underlying energy or mood\n\n"
        f"Return valid JSON only in this format:\n"
        f"{{\n"
        f"  \"towns\": {{\n"
        f"    \"TownName1\": {{ \"narrative\": \"...\", \"spirit\": \"...\" }},\n"
        f"    \"TownName2\": {{ \"narrative\": \"...\", \"spirit\": \"...\" }},\n"
        f"    \"TownName3\": {{ \"narrative\": \"...\", \"spirit\": \"...\" }}\n"
        f"  }}\n"
        f"}}\n"
    )
