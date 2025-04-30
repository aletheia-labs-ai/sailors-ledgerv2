from pydantic import BaseModel
from typing import Dict, Optional

class InteractionResponse(BaseModel):
    narrative: Optional[str]
    asset_changes: Optional[Dict[str, int]]
    stat_modifiers: Optional[Dict[str, str]]
