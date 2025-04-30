from typing import List, Dict
import datetime
from schemas.seed import TarotDraw, SeedPacket
from llm.narrative_engine import generate_seeded_world_state

class TarotSeedingEngine:
    def __init__(self, player_name: str):
        self.player_name = player_name
        self.draws: List[TarotDraw] = []

    def add_draw(self, draw: TarotDraw):
        self.draws.append(draw)

    def build_packet(self) -> SeedPacket:
        return SeedPacket(
            player_name=self.player_name,
            tarot_draws=self.draws,
            timestamp=datetime.datetime.utcnow().isoformat()
        )

    async def finalize_world_seed(self) -> Dict:
        seed_packet = self.build_packet()
        response = await generate_seeded_world_state(seed_packet.dict())
        return response
