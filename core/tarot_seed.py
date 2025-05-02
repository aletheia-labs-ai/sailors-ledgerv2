from typing import List, Dict
import datetime
from schemas.seed import TarotDraw, SeedPacket
from llm.narrative_engine import generate_seeded_world_state
from llm.tarot_question_engine import generate_tarot_question
import random
from utils.tarot_loader import load_tarot_cards
import asyncio

class TarotSeedingEngine:
    def __init__(self, player_name: str, deck_path: str = "data/tarot_cards/cards.json"):
        self.player_name = player_name
        self.deck = load_tarot_cards(deck_path)
        self.remaining_deck = self.deck.copy()
        self.draws: List[TarotDraw] = []

    def draw_random_card(self) -> Dict:
        card = random.choice(self.remaining_deck)
        self.remaining_deck.remove(card)
        return card

    def add_draw(self, draw: TarotDraw):
        self.draws.append(draw)

    def build_packet(self) -> SeedPacket:
        return SeedPacket(
            player_name=self.player_name,
            tarot_draws=self.draws,
            timestamp=datetime.datetime.utcnow().isoformat()
        )

    async def run_draw_chain(self, min_draws: int = 3, max_draws: int = 5):
        for draw_num in range(max_draws):
            card = self.draw_random_card()
            question = random.choice(card["questions"])
            scenario_packet = await generate_tarot_question(
                card_name=card["card_name"],
                meaning=card["meaning"],
                theme_question=question,
                history=[d.model_dump() for d in self.draws]
            )
            if not scenario_packet or "scenario" not in scenario_packet or "choices" not in scenario_packet:
                print("Invalid tarot scenario response. Aborting.")
                return False

            print(f"\nCard Drawn #{draw_num+1}: {card['card_name']}")
            print(f"Meaning: {card['meaning']}")
            print(f"Theme Question: {question}")
            print(f"\n{scenario_packet['scenario']}")
            for idx, choice in enumerate(scenario_packet["choices"], 1):
                print(f"{idx}. {choice['text']}")

            while True:
                try:
                    selected = int(input("Choose 1-4: ").strip())
                    if 1 <= selected <= 4:
                        break
                except ValueError:
                    pass
                print("Invalid choice. Try again.")

            selected_choice = scenario_packet["choices"][selected - 1]
            self.add_draw(TarotDraw(
                card_name=card["card_name"],
                card_meaning=card["meaning"],
                player_response={"text": selected_choice["text"], "tag": selected_choice["tag"]}
            ))

            # Exit if min draws completed and LLM says arc is resolved
            if draw_num + 1 >= min_draws and scenario_packet.get("complete") is True:
                print(f"\nArc resolved: {scenario_packet.get('justification', 'Symbolic closure detected.')}")
                break

    async def finalize_world_seed(self) -> Dict:
        seed_packet = self.build_packet()
        response = await generate_seeded_world_state(seed_packet.model_dump())
        return response
