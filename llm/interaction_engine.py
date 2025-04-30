from llm.llm_client import call_llm
from typing import Dict, Optional
import json

async def generate_interaction_response(interaction_packet: Dict) -> Optional[Dict]:
    prompt = build_interaction_prompt(interaction_packet)

    messages = [
        {"role": "system", "content": "You simulate direct player interactions in a fantasy world. Respond with a short narrative and JSON of resulting asset/stat changes."},
        {"role": "user", "content": prompt}
    ]

    response = await call_llm(messages, model="gpt-4o-mini")
    if response:
        try:
            return json.loads(response)
        except Exception as e:
            print(f"Failed to parse interaction response: {e}")
            return None
    return None

def build_interaction_prompt(packet: Dict) -> str:
    return f"Given this interaction input:\n\n{packet}\n\nReturn a structured JSON with 'narrative', 'asset_changes', and 'stat_modifiers'."
