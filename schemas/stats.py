from pydantic import BaseModel, Field
from typing import List

class CharacterStats(BaseModel):
    strength: int = Field(0, ge=0, description="Physical power and melee prowess")
    dexterity: int = Field(0, ge=0, description="Agility and finesse")
    constitution: int = Field(0, ge=0, description="Endurance and toughness")
    intelligence: int = Field(0, ge=0, description="Reasoning and arcane aptitude")
    wisdom: int = Field(0, ge=0, description="Insight and perception")
    charisma: int = Field(0, ge=0, description="Force of personality")
    luck: int = Field(0, ge=0, description="Chance and serendipity")
    alignment: int = Field(50, ge=0, le=100, description="Virtue (0=corrupt, 100=virtuous)")
    courage: int = Field(50, ge=0, le=100, description="Bravery and resolve")
    tags: List[str] = Field(default_factory=list, description="Personality or background tags")
