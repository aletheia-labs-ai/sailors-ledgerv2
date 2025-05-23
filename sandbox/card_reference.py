


cards = {
    1: ("The Fool", "Beginnings, naivety, spontaneity"),
    2: ("The Magician", "Willpower, creation, manifestation"),
    3: ("The High Priestess", "Intuition, secrets, subconscious"),
    4: ("The Empress", "Fertility, beauty, nurturing"),
    5: ("The Emperor", "Authority, structure, control"),
    6: ("The Hierophant", "Tradition, spiritual wisdom, conformity"),
    7: ("The Lovers", "Love, alignment, values"),
    8: ("The Chariot", "Determination, victory, motion"),
    9: ("Strength", "Courage, inner power, compassion"),
    10: ("The Hermit", "Solitude, introspection, guidance"),
    11: ("Wheel of Fortune", "Fate, change, cycles"),
    12: ("Justice", "Truth, fairness, law"),
    13: ("The Hanged Man", "Sacrifice, surrender, new perspective"),
    14: ("Death", "Endings, transformation, release"),
    15: ("Temperance", "Balance, moderation, healing"),
    16: ("The Devil", "Temptation, bondage, materialism"),
    17: ("The Tower", "Upheaval, sudden change, awakening"),
    18: ("The Star", "Hope, renewal, clarity"),
    19: ("The Moon", "Illusion, fear, subconscious"),
    20: ("The Sun", "Joy, success, vitality"),
    21: ("Judgement", "Rebirth, reckoning, inner calling"),
    22: ("The World", "Completion, wholeness, fulfillment")
}

def get_card(index: int):
    return cards.get(index)