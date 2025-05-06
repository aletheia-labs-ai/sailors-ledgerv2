import asyncio
from core.world import World
from core.player import Player
from core.town import Town
from core.tarot_seed import TarotSeedingEngine
from utils.id_generator import generate_world_id
from utils.tarot_loader import load_tarot_cards, draw_random_cards
from llm.symbolic_arc_engine import generate_symbolic_arc
from utils.dilemma_logger import log_dilemma

async def main():
    print("Welcome to Sailor's Ledger V2")
    player_name = input("Enter your character's name: ").strip()

    # Tarot Seeding with predefined deck
    seeder = TarotSeedingEngine(player_name)
    deck = load_tarot_cards("data/tarot_cards/cards.json")
    draws = draw_random_cards(deck, 3)

    from schemas.seed import TarotDraw
    from llm.tarot_question_engine import generate_tarot_question

    for i, draw in enumerate(draws):
        print(f"\nCard Drawn #{i+1}: {draw['card_name']}")
        print(f"Meaning: {draw['meaning']}")

        scenario_packet = await generate_tarot_question(draw["card_name"], draw["meaning"])
        if not scenario_packet:
            print("Failed to generate tarot scenario. Exiting.")
            return

        print(f"\n{scenario_packet['scenario']}")
        for idx, choice in enumerate(scenario_packet["choices"], 1):
            print(f"{idx}. {choice['text']}")

        while True:
            try:
                selected = int(input("Choose 1-4: ").strip())
                if 1 <= selected <= len(scenario_packet["choices"]):
                    break
            except ValueError:
                pass
            print("Invalid choice. Try again.")

        selected_response = scenario_packet["choices"][selected - 1]
        # Log the dilemma after a valid choice is made
        log_dilemma(
            draw_number=i + 1,
            card_name=draw["card_name"],
            scenario=scenario_packet["scenario"],
            core_dilemma=scenario_packet.get("core_dilemma", "N/A"),
            choices=scenario_packet["choices"],
            selected_tag=selected_response["tag"]
        )
        seeder.add_draw(TarotDraw(
            card_name=draw["card_name"],
            card_meaning=draw["meaning"],
            player_response={"text": selected_response["text"], "tag": selected_response["tag"]}
        ))

    seed_response = await seeder.finalize_world_seed()
    if not seed_response or not isinstance(seed_response, dict) or "towns" not in seed_response:
        print("World generation failed. The response was invalid or improperly formatted.")
        return

    arc_summary = await generate_symbolic_arc(seeder.build_packet().model_dump())
    if arc_summary:
        print("\nYour Symbolic Arc:")
        print(arc_summary)
        print("\n" + "-"*40 + "\n")

    from llm.persona_engine import generate_persona_prophecy
    persona_text = await generate_persona_prophecy(seeder.build_packet().model_dump())
    if persona_text:
        print("\nYour Prophecy:")
        print(persona_text)
        print("\n" + "-"*40 + "\n")

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
        print(f"  Narrative: {town.narrative[-1] if town.narrative else 'No narrative.'}")

    print("\nWorld generation complete.")

if __name__ == "__main__":
    asyncio.run(main())
