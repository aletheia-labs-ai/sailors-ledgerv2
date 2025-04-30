import asyncio
from core.world import World
from core.player import Player
from core.town import Town
from core.tarot_seed import TarotSeedingEngine
from utils.id_generator import generate_world_id
from utils.tarot_loader import load_tarot_cards, draw_random_cards

async def main():
    print("Welcome to Sailor's Ledger V2")
    player_name = input("Enter your character's name: ").strip()

    # Tarot Seeding with predefined deck
    seeder = TarotSeedingEngine(player_name)
    deck = load_tarot_cards("data/tarot_cards/cards.json")
    draws = draw_random_cards(deck, 3)

    for i, draw in enumerate(draws):
        print(f"\nCard Drawn #{i+1}: {draw['card_name']}")
        print(f"Meaning: {draw['meaning']}")
        response = input(f"{draw['question']} ").strip()
        seeder.add_draw(draw["card_name"], draw["meaning"], response)

    seed_response = await seeder.finalize_world_seed()

    world_id = generate_world_id()
    world = World(name=world_id)

    for town_name, town_data in seed_response.get("towns", {}).items():
        town = Town(name=town_name)
        town.spirit = town_data.get("spirit")
        town.narrative.append(town_data.get("narrative", ""))
        world.add_town(town)

    player = Player(name=player_name)
    world.set_player(player)

    print(f"\nWorld '{world.name}' initialized with {len(world.towns)} towns.")
    for town in world.towns.values():
        print(f"- {town.name}: {town.spirit}")

    print("\nWorld generation complete.")

if __name__ == "__main__":
    asyncio.run(main())
