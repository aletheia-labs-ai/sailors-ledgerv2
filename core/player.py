from typing import Dict, List, Optional
from schemas.stats import CharacterStats

class Player:
    def __init__(self, name: str):
        self.name = name
        self.characteristics: Dict[str, str] = {}
        self.assets: Dict[str, int] = {}
        self.location: Optional[str] = None
        self.ledger: List[dict] = []
        self.history: List[str] = []
        self.stats: CharacterStats = CharacterStats()

    def move_to(self, town_name: str):
        self.location = town_name
        self.history.append(f"Traveled to {town_name}")

    def acquire_asset(self, asset_name: str, quantity: int = 1):
        self.assets[asset_name] = self.assets.get(asset_name, 0) + quantity

    def update_characteristic(self, trait: str, value: str):
        self.characteristics[trait] = value

    def record_transaction(self, transaction: dict):
        self.ledger.append(transaction)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "characteristics": self.characteristics,
            "assets": self.assets,
            "location": self.location,
            "ledger": self.ledger,
            "history": self.history,
        }

    @classmethod
    def from_dict(cls, data: dict):
        player = cls(name=data["name"])
        player.characteristics = data.get("characteristics", {})
        player.assets = data.get("assets", {})
        player.location = data.get("location")
        player.ledger = data.get("ledger", [])
        player.history = data.get("history", [])
        return player

    def apply_stat_changes(self, changes: dict):
        for key, delta in changes.items():
            if hasattr(self.stats, key):
                current = getattr(self.stats, key)
                # calculate new value
                new_value = current + delta
                # clamp to valid range
                field = self.stats.__fields__[key]
                min_v = field.field_info.ge or 0
                max_v = field.field_info.le if field.field_info.le is not None else new_value
                new_value = max(min_v, min(max_v, new_value))
                setattr(self.stats, key, new_value)
