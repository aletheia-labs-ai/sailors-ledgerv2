# Sailor's Ledger V2 — Developer Notes

This file captures implementation notes, temporary workarounds, deferred design decisions, and general build context. Do not delete without review.

---

## Prompt Design Notes

### Tarot Prompt (generate_tarot_question)
- Current prompt instructs LLM to return JSON with a `"scenario"` and four labeled `"choices"` each with a `"text"` and `"tag"` field.
- Example schema:
  ```json
  {
    "scenario": "You're offered two paths...",
    "choices": [
      { "text": "Take the path of fire.", "tag": "A" },
      { "text": "Take the path of shadow.", "tag": "B" },
      ...
    ]
  }
  ```
- Prompt enforces brevity (1–2 sentences), tone variation (modern, fantasy, sci-fi), and structural integrity.
- Display still uses 1–4 for clarity, but `tag` is available for future logic/UX use.

### Town Generator (generate_seeded_world_state)
- LLM is instructed to generate three towns, each with:
  - a poetic, symbolic name
  - a 1–2 sentence narrative
  - a governing "spirit"
- Prompt explicitly prohibits literal reuse of tarot card names or user answers.

### Persona Prophecy (generate_persona_prophecy)
- Output is a single symbolic paragraph synthesizing themes from tarot draws.
- Prompt forbids mechanical summary and encourages fate-based mythic tone.

---

## Visibility Notes

- Meaning and Theme Question for each tarot card are currently shown to the player during draw.
- These are intended for LLM use only.
- Visibility will be removed or hidden in production build.

---

## Structure/Schema Notes

- `TarotDraw` now includes:
  - `card_name: str`
  - `card_meaning: str`
  - `player_response: { "text": str, "tag": Literal["A", "B", "C", "D"] }`

- All tarot choice generation now assumes this structured response.

---

## TODO Review Zone

This section is for in-progress ideas, deferred problems, or loose thoughts. Revisit periodically.

- [ ] Determine where/how to log world initialization and heartbeat events for persistent replay/debug.
- [ ] Decide if world/town/player data should be autosaved after each significant event.
- [ ] Build function to regenerate or export a Seed Packet summary post-hoc (for display or share).
- [ ] Revisit tarot prompt diversity — verify genre distribution and moral distinction hold across samples.
- [ ] Suppress narrative/spirit printout after seed once UX stabilizes.

BIG FEATURE IDEAS
- [ ] Make Tarot choices determine parameters of character creation. Right now, character is just a name. Implementation depends on how the concept of character is actually addressed
- [ ] Character implementation: parameter based? freeform? mixed. Parameter based would essentially be traditional game stats (STR, DEX, CON, WIS, INT, ETC) and tarot answers each modify scores from baseline (hidden). Most choices are more about moral dillemma rather than...how strong are you..but we could connect more aggresive dillema choices to things like strength, endurance/perseverence choices to con, wily or impulsive choices to dex, contemplative/insightful to wis/int or whatever. If we went that way, we might want to tell the LLM that it is the point before hand... like say "you need to come up with some parameter questions that align with the card"...specifying that each answer choice should have implications for the character's attributes based on something like the schema above. From a functional perspective, we could even seed each card with 4 relevant parameters, then tell the LLM to create answer choices that correspond with the (hidden) parameter change. E.g., card is death, we predetermine that the answers would correspond to (HP, STR, CON, LUK)..then have the LLM specifically generates the question and answers to fit that schema. So for Death, the LLM would be fed the Card Name, maybe the meaning/question, then the four relevant parameters (HP, STR, CON, LUK), and a request to create a question that fits the theme and whose questions make sense for each parameter. So for example: On your deathbed after years of peaceful rule, what do you tell your historian was the key to your success: 
1. My friends and family.
2. An indomintable will.
3. The bravery of my soldiers.
4. The will of the gods. 
- This would be a big shift, but I like the idea of it.  And not every question would need to be that straightforward, but there are benefits to the approach.
- [ ] Another thing, i'd like for the tarot draws to feel a little more connected...so we get Draw 1 -> question 1 -> options 1 (x4) ----> user decision -> feed back to LLM, generate question 2 by looking at question and selection of draw 1 + stuff about draw 2...then we hopefully get a little contiunity between them, which will weave into a more cohesive narrative for generating the world narrative.  So for instance, lets say we get the following: 
- Draw 1: Fortune  
- Question 1: A genie offers to make you a tempting wager, the bigger the cost, the bigger reward. What do you put on the table?
- Option 1.1: All the money I have. (+100 gold OR -100 gold)
- Option 1.2: 10 years of my life. (+1 CON/HP OR -1 CON/HP)
- Option 1.3: My friendships (-1 ALIGNMENT, +1 STR)
- Option 1.4: I offer nothing. (+1 INT)
- User selects 1.2: 10 years of my life. Parameter choices are recorded (not shown though)
- New Draw: Lovers [LLM is sent Lovers data, Q1 question and answer data, asked to generate a followup question with that in mind. ]
- Question 2: With luck, you find your ideal partner, but they are captured by your enemy and are forced to betray you. 
- Option 2.1: You gather your armies to destroy your enemy. (+1 CON)
- Option 2.2: You mourn their loss and forgive the betrayal. (+1 ALI, +1 WIS)
- Option 2.3: You steal into the enemy camp to attempt a rescue. (+1 DEX)
- Option 2.4: Such is war, find a way to use it to your advantage (+1 STR, -1 ALI)
- User selects 2.3: You steal into the enemy camp to attempt a rescue. Parameter changes are recorded, not shown
- New Draw: Tower --> LLM is sent Tower data, Q1 and Q2 question and answer data, asked to generate a followup question with those in mind. 
- Question 3: While stealing into an enemy camp, you see an opportunity to set the camp ablaze.
- Option 3.1: You set the camp on fire, guaranteeing victory at all costs. (+1 STR, -1 ALI)
- Option 3.2: You attempt your mission first, then plan to set the fire as you leave. (+1 DEX)
- Option 3.3: Set a smaller fire to create a distraction. (+1 INT)
- Option 3.4: You abhor the unrestrained danger of wildfire. (+1 WIS)
- User selects 3.4: You abhor the unrestrained danger of wilffire. Parameter changes are recorded but not shown.  
- The mini narrative (Q1->Choice1->Q2->Choice2->Q3->Choice3) is then fed to the LLM to seed character fortune as well as world...maybe phrase it like the little micro story is an allegory for the greater narrative of the land, write the narrative for which this is an allegory. 
- TWO MAJOR APPROACHES. Paramter changes seed Q&A choices or parameter changes arise from Q&A choices. Actually, the idea of linking questions and answers together is independent of parameters really. These are two ideas. Explore both options.

---

## Tarot Seeding Logic — Dual Model Overview + Draw Chain Flow

We now support two complementary models for tarot-driven character/world seeding:

### Model A: Parameter-First Mapping (Deterministic)
- Each tarot card is pre-tagged with 4 relevant parameters (e.g., STR, INT, LUK, CON).
- When a card is drawn, the LLM is instructed to generate a scenario and four choices aligned with those parameters.
- Each choice implicitly boosts or defines one parameter (hidden from the player).
- Enables clean RPG-style stat shaping from symbolic moral trials.

### Model B: Narrative-First Mapping (Inference)
- Tarot card and meaning are passed to the LLM with no parameter constraint.
- LLM freely generates scenario + answers based on symbolic themes.
- A second pass or external logic may map selected responses to traits/stats.
- Useful for more mythic or literary narrative branching, less deterministic.

**Both models can coexist.** Use Model A when shaping quantifiable stats. Use Model B when generating symbolic narratives or world tone.

---

## Semi-Dynamic Draw Chaining (Narrative Arc Completion)

- Player must complete a minimum of 3 draws.
- After each draw, the LLM is prompted with the entire prior Q&A chain to determine if the arc is resolved.
- If unresolved, the LLM returns:
  ```json
  {
    "complete": false,
    "next_card": "The Tower",
    "scenario": "...",
    "choices": [ ... ]
  }
  ```
- If resolved:
  ```json
  {
    "complete": true,
    "justification": "The arc has reached symbolic closure with the final sacrifice."
  }
  ```

- Maximum draw limit: 5 (failsafe to avoid infinite loops)
- After completion, the entire draw chain is passed to both:
  - `generate_seeded_world_state()`
  - `generate_persona_prophecy()`
- Prompt language should refer to the sequence as a symbolic trial or allegory.

---

## Implementation Notes

- `seed_engine.py` will need to track full tarot response chain (card, scenario, selected answer, tag, and param if applicable).
- Prompts must distinguish between Mode A (parameter shaping) and Mode B (theme evolution).
- Completion evaluation prompt must be consistent in tone and structure — the LLM must learn what “closure” looks like narratively.

---

## Example Questions and Choices ##
- Logic: Card --> Core Concepts --> LLM Creates Core Dilemma --> LLM Creates Question/Answers to illustrate dilemma. Maybe it is better to call the question a "narrative dilemma" and the "choices" aren't really answers, just next steps or decisions. In short we don't necessarily have to make it Q-A. Sometimes that can be restrictive. Not included in the below section, but potentially could be, are the parameters that we determine are affiliated with each card. 
## We Send ##
- Card: Empress
- Concepts: Abundance, fertility, sustenance
## LLM Generates ##
- Core Dilemma: To take sustenance at the expense of others
- Narrative Dilemma: When settling anew, you find a beautiful glade flourishing with more creatures and fruits that have ever been seen. Surely the gods have smiled upon you.
- Choice A: Immediately settle the area and start your new life in abundance
- Choice B: Draw from the spring, eat from the trees, thank the gods and move on.
- Choice C: Set up a small cottage to live in harmony with the glade.
- Choice D: Stake a claim to the land and sell it to the nearby lord.
## We Send ##
- Card: Fool
- Concepts: Journey, idealism, freedom
## LLM Generates ##
- Core Dilemma: To trade freedom and idealism for obligation and reward.
- Narrative Dilemma: After years as a wandering hedge knight, the local tyrant demands that you give fealty to his court in exchange for position, wealth and power.
- Choice A: Swear fealty to the tyrant and uphold your oaths of service to his court.
- Choice B: Join his court but secretly undermine the tyrant and rebel. 
- Choice C: Join the tyrant's court and vow to do good where you can. 
- Choice D: Flee the tyrant and his court, continuing your journey in freedom. 
## We Send ##
- Card: Magician
- Concepts: Willpower, desire, ability
## LLM Generates ##
- Core Dilemma: Paying costs to achieve your ambitions
- Narrative Dilemma: Victory is within your grasp! Your people are tired and battle-worn, but they could give a little more.
- Choice A: Victory is everything. Force a final march.
- Choice B: Try to rally your forces with a rousing speech, inspiring them to courage. 
- Choice C: Put together a team of elite volunteers to pursue the critical mission.
- Choice D: Retreat and regroup, live to fight another day. 

----
Fortune Examples

---