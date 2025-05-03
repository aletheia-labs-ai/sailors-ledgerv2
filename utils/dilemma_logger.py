import json
from typing import List, Dict
from pathlib import Path

LOG_PATH = Path("data/tarot_cards/observed_dilemmas.json")

def log_dilemma(draw_number: int, card_name: str, scenario: str, choices: List[Dict], selected_tag: str):
    record = {
        "draw": draw_number,
        "card": card_name,
        "scenario": scenario,
        "choices": choices,
        "selected": selected_tag
    }

    # Ensure file exists and starts as list
    if not LOG_PATH.exists():
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            json.dump([record], f, indent=2)
    else:
        with open(LOG_PATH, "r+", encoding="utf-8") as f:
            try:
                data = json.load(f)
                assert isinstance(data, list)
            except (json.JSONDecodeError, AssertionError):
                data = []
            data.append(record)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
