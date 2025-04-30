

from core.player import Player
from core.town import Town
from llm.interaction_engine import generate_interaction_response

class InteractionEngine:
    def __init__(self):
        pass  # placeholder for model config or routing

    async def handle_interaction(self, player: Player, town: Town, intent: str, payload: dict = None):
        interaction_input = {
            "player_name": player.name,
            "location": town.name,
            "intent": intent,
            "assets": player.assets,
            "characteristics": player.characteristics,
            "payload": payload or {}
        }

        response = await generate_interaction_response(interaction_input)

        if response:
            # Apply free-text narrative
            if "narrative" in response:
                town.record_event(response["narrative"])

            # Apply asset modifications
            for asset, delta in response.get("asset_changes", {}).items():
                player.assets[asset] = player.assets.get(asset, 0) + delta

            # Apply stat changes
            for stat, val in response.get("stat_modifiers", {}).items():
                player.characteristics[stat] = val

        return response