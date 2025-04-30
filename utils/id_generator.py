import uuid

def generate_world_id() -> str:
    return f"world_{uuid.uuid4().hex[:8]}"

def generate_town_id() -> str:
    return f"town_{uuid.uuid4().hex[:8]}"

def generate_player_id() -> str:
    return f"player_{uuid.uuid4().hex[:8]}"
