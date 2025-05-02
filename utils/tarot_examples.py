

import json
from typing import List, Dict

def load_tarot_examples(path: str = "data/tarot_cards/example_dilemmas.json") -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)