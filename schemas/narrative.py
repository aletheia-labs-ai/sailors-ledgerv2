from pydantic import BaseModel
from typing import Dict, Optional

class TownNarrativeUpdate(BaseModel):
    narrative: Optional[str]
    spirit: Optional[str]

class NarrativeResponse(BaseModel):
    event_summary: Optional[str]
    town_updates: Dict[str, TownNarrativeUpdate]
