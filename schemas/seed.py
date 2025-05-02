from pydantic import BaseModel
from typing import List, Literal

class Choice(BaseModel):
    text: str
    tag: Literal["A", "B", "C", "D"]

class TarotDraw(BaseModel):
    card_name: str
    card_meaning: str
    player_response: Choice

class SeedPacket(BaseModel):
    player_name: str
    tarot_draws: List[TarotDraw]
    timestamp: str  # ISO 8601 datetime string
