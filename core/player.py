from typing import Dict, List, Optional

class Player:
    def __init__(self, name: str):
        self.name = name
        self.characteristics: Dict[str, str] = {}
        self.assets: Dict[str, int] = {}
        self.location: Optional[str] = None
        self.ledger: List[dict] = []
        self.history: List[str] = []

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
