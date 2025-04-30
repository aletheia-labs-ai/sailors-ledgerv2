from core.world import World
from llm.narrative_engine import generate_world_narrative_update

class NarrativeEngine:
    def __init__(self):
        pass  # placeholder for configuration or model selection logic

    async def update_narrative(self, world: World):
        # Collect inputs (world state, player data, town spirits)
        seed_info = {
            "world_name": world.name,
            "towns": list(world.towns.keys()),
            "last_events": world.world_chronicle[-3:],
        }

        # Dispatch to LLM via narrative engine
        narrative_result = await generate_world_narrative_update(seed_info)

        # Apply free-text and structured updates
        if narrative_result:
            world.record_world_event(narrative_result.get("event_summary", "World narrative update occurred"))
            for town_name, update in narrative_result.get("town_updates", {}).items():
                town = world.towns.get(town_name)
                if town:
                    if "narrative" in update:
                        town.narrative.append(update["narrative"])
                    if "spirit" in update:
                        town.spirit = update["spirit"]
