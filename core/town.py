

from typing import List, Dict, Optional
import os
import json

class Town:
    def __init__(self, name: str):
        self.name = name
        self.narrative: List[str] = []
        self.spirit: Optional[str] = None
        self.stats: Dict[str, int] = {}
        self.assets: Dict[str, int] = {}
        self.ledger: List[dict] = []
        self.chronicle: List[str] = []
        self.rumor_pool: List[str] = []

    def record_event(self, event: str):
        self.chronicle.append(event)

    def add_asset(self, asset_name: str, quantity: int = 1):
        self.assets[asset_name] = self.assets.get(asset_name, 0) + quantity

    def update_stat(self, stat_name: str, value: int):
        self.stats[stat_name] = value

    def add_rumor(self, rumor: str):
        self.rumor_pool.append(rumor)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "narrative": self.narrative,
            "spirit": self.spirit,
            "stats": self.stats,
            "assets": self.assets,
            "ledger": self.ledger,
            "chronicle": self.chronicle,
            "rumor_pool": self.rumor_pool,
        }

    @classmethod
    def from_dict(cls, data: dict):
        town = cls(name=data["name"])
        town.narrative = data.get("narrative", [])
        town.spirit = data.get("spirit")
        town.stats = data.get("stats", {})
        town.assets = data.get("assets", {})
        town.ledger = data.get("ledger", [])
        town.chronicle = data.get("chronicle", [])
        town.rumor_pool = data.get("rumor_pool", [])
        return town