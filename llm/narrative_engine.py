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
        {"role": "system", "content": (
            "You are a fantasy world generator. You will receive a tarot-based Seed Packet. "
            "Extract symbolic themes and use them as inspiration—do not copy player answers or card names literally. "
            "Generate three towns. Each must have a:\n"
            "- name (symbolic, original, world-appropriate)\n"
            "- narrative (1–2 sentences describing the town’s identity and mood)\n"
            "- spirit (a poetic phrase representing the town’s governing ethos)\n"
            "Return valid JSON in this structure:\n"
            "{ \"towns\": { \"TownName\": { \"narrative\": \"...\", \"spirit\": \"...\" }, ... } }"
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

def build_seed_prompt(seed: Dict) -> str:
    return (
        f"You are a fantasy world generator. Use the following tarot Seed Packet to define a starting world.\n\n"
        f"Return only valid JSON with this exact structure:\n\n"
        f"{{\n"
        f'  "towns": {{\n'
        f'    "TownName1": {{\n'
        f'      "narrative": "Short descriptive paragraph for the town.",\n'
        f'      "spirit": "A short label representing the town’s governing energy or ethos."\n'
        f"    }},\n"
        f'    "TownName2": {{ ... }}\n'
        f"  }}\n"
        f"}}\n\n"
        f"Here is the tarot Seed Packet:\n\n{seed}"
    )
