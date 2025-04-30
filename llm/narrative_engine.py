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

async def generate_seeded_world_state(seed_packet: Dict) -> Optional[Dict]:
    prompt = build_seed_prompt(seed_packet)

    messages = [
        {"role": "system", "content": "You are a fantasy world generator. Interpret tarot-based Seed Packet and generate a starting world summary, town spirits, and tone."},
        {"role": "user", "content": prompt}
    ]

    response = await call_llm(messages, model="gpt-4o")
    if response:
        try:
            return json.loads(response)
        except Exception as e:
            print(f"Failed to parse seed generation response: {e}")
            return None
    return None

def build_seed_prompt(seed: Dict) -> str:
    return f"Here is the tarot Seed Packet:\n\n{seed}\n\nGenerate a structured JSON describing the starting world state."
