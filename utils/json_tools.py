import json
from typing import Any

def try_parse_json(raw: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse failed: {e}")
        return None

def pretty_print_json(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False)
