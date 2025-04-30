import datetime
from core.world import World

class HeartbeatEngine:
    def __init__(self, cooldown_seconds: int = 120):
        self.last_heartbeat: datetime.datetime = datetime.datetime.utcnow()
        self.cooldown = datetime.timedelta(seconds=cooldown_seconds)

    def should_trigger(self) -> bool:
        return datetime.datetime.utcnow() - self.last_heartbeat >= self.cooldown

    async def trigger_heartbeat(self, world: World):
        # Placeholder: collect inputs, call LLM, apply operational changes
        print(f"[Heartbeat] Triggering heartbeat at {datetime.datetime.utcnow().isoformat()}")
        world.record_world_event("Heartbeat occurred")
        self.last_heartbeat = datetime.datetime.utcnow()
        world.last_heartbeat = self.last_heartbeat
