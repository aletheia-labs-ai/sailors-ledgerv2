

import json
import random
from typing import List, Dict

def load_tarot_cards(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def draw_random_cards(deck: List[Dict], count: int = 3) -> List[Dict]:
    draws = random.sample(deck, count)
    for draw in draws:
        draw["question"] = random.choice(draw["questions"])
    return draws