from sandbox.card_reference import cards, get_card
import asyncio, json
from llm.tarot_question_engine import generate_core_dilemma, generate_tarot_question

if __name__ == "__main__":
    print("Available Tarot Cards:")
    for idx, (name, _) in cards.items():
        print(f"{idx}. {name}")
    choice = input("Choose a card number (1–22): ").strip()
    try:
        index = int(choice)
        selected = get_card(index)
        if not selected:
            print("Invalid selection.")
        else:
            card_name, meaning = selected
            core = asyncio.run(generate_core_dilemma(card_name, meaning))
            print("\nGenerated Core Dilemma:")
            print(core or "No dilemma returned.")
            packet = asyncio.run(generate_tarot_question(card_name, meaning))
            print("\nGenerated Scenario and Choices:")
            print(json.dumps(packet, indent=2))
    except ValueError:
        print("Please enter a valid number.")