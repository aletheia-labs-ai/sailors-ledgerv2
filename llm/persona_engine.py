from llm.llm_client import call_llm
from typing import Dict, Optional
import json

async def generate_persona_prophecy(seed_packet: Dict) -> Optional[str]:
    prompt = build_persona_prompt(seed_packet)

    messages = [
        {
            "role": "system",
            "content": (
                "You are an ancient oracle in a fantasy simulation game. You will receive a tarot-based Seed Packet. "
                "From this, generate a prophetic character profile that blends personality archetypes with mythic fate. "
                "Do not summarize or repeat any player choices or tarot card names. Extract symbolic meaning. "
                "Your tone must be poetic, cryptic, and fate-driven—less biography, more omen. "
                "Present the player as a figure of prophecy, whose traits hint at coming glories or calamities. "
                "Output a single paragraph (4–6 sentences) of pure text. No headings. No JSON. No numbered lists."
            )
        },
        {"role": "user", "content": prompt}
    ]

    response = await call_llm(messages, model="gpt-4o")
    if not response:
        print("No response from persona engine.")
        return None

    return response.strip()

def build_persona_prompt(seed: Dict) -> str:
    return (
        f"Seed Packet:\n\n"
        f"{json.dumps(seed, indent=2)}\n\n"
        f"From this, generate the player's prophetic character description."
    )
