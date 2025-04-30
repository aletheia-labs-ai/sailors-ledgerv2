


from typing import Dict, List, Optional
from core.town import Town
from core.player import Player
import os
import json
import datetime

class World:
    def __init__(self, name: str):
        self.name = name
        self.towns: Dict[str, Town] = {}
        self.player: Optional[Player] = None
        self.aggregate_ledger: List[dict] = []
        self.world_chronicle: List[str] = []
        self.last_heartbeat: Optional[datetime.datetime] = None

    def add_town(self, town: Town):
        self.towns[town.name] = town

    def set_player(self, player: Player):
        self.player = player

    def record_transaction(self, transaction: dict):
        self.aggregate_ledger.append(transaction)

    def record_world_event(self, event: str):
        self.world_chronicle.append(event)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "towns": {name: town.to_dict() for name, town in self.towns.items()},
            "player": self.player.to_dict() if self.player else None,
            "aggregate_ledger": self.aggregate_ledger,
            "world_chronicle": self.world_chronicle,
            "last_heartbeat": self.last_heartbeat.isoformat() if self.last_heartbeat else None,
        }

    @classmethod
    def from_dict(cls, data: dict):
        world = cls(name=data["name"])
        world.aggregate_ledger = data.get("aggregate_ledger", [])
        world.world_chronicle = data.get("world_chronicle", [])
        world.last_heartbeat = (
            datetime.datetime.fromisoformat(data["last_heartbeat"])
            if data.get("last_heartbeat")
            else None
        )
        # Town and player deserialization will require stubs in their respective classes
        return world

    def save(self, path: str):
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, "world.json"), "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: str):
        with open(os.path.join(path, "world.json"), "r") as f:
            data = json.load(f)
        return cls.from_dict(data)