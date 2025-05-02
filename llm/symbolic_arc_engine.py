

from typing import Optional, Dict
import json
from llm.llm_client import call_llm

async def generate_symbolic_arc(seed_packet: Dict) -> Optional[str]:
    prompt = build_symbolic_arc_prompt(seed_packet)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a mythographer. Given a symbolic tarot draw sequence, distill the sequence into a single short mythic journey. "
                "Avoid literal repetition of cards or answers. Instead, extract the symbolic arc that underlies the character's transformation. "
                "Your output should be a poetic but clear narrative (3–5 sentences) describing the path the player took through symbolic trials. "
                "This arc will be used to inspire a fantasy world's formation and a player’s fortune. Output plain text only—no labels, no JSON."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    response = await call_llm(messages, model="gpt-4o")
    return response.strip() if response else None

def build_symbolic_arc_prompt(seed_packet: Dict) -> str:
    return (
        f"Here is the Seed Packet. It includes tarot cards drawn, the symbolic questions asked, and the player's selected answers. "
        f"Use this to synthesize the symbolic arc:\n\n{json.dumps(seed_packet, indent=2)}\n\n"
        f"Write a 3–5 sentence mythic summary of the symbolic transformation implied."
    )