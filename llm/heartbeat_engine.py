from llm.llm_client import call_llm
from typing import Dict, Optional
import json

async def generate_heartbeat_update(heartbeat_packet: Dict) -> Optional[Dict]:
    prompt = build_heartbeat_prompt(heartbeat_packet)

    messages = [
        {"role": "system", "content": "You are a world simulation engine. Respond with JSON structured updates and a brief narrative."},
        {"role": "user", "content": prompt}
    ]

    response = await call_llm(messages, model="gpt-4o")
    if response:
        try:
            return json.loads(response)
        except Exception as e:
            print(f"Failed to parse heartbeat response: {e}")
            return None
    return None

def build_heartbeat_prompt(packet: Dict) -> str:
    # Simple serialization for now — later move to template-based
    return f"Given this heartbeat input:\n\n{packet}\n\nGenerate a structured JSON output with stat changes, asset shifts, town events, and player effects."
