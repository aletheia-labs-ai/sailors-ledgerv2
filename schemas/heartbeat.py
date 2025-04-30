

from pydantic import BaseModel
from typing import Dict, List, Optional

class TownUpdate(BaseModel):
    stat_changes: Optional[Dict[str, int]] = None
    asset_changes: Optional[Dict[str, int]] = None
    event: Optional[str] = None

class HeartbeatResponse(BaseModel):
    world_event: Optional[str]
    town_updates: Dict[str, TownUpdate]
    player_effects: Optional[Dict[str, int]] = None