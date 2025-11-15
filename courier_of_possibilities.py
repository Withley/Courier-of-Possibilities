import os
import sys
import time
import random
import textwrap

# ==========================
# Terminal Helpers & Styles
# ==========================

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"

FG_BLACK = "\033[30m"
FG_RED = "\033[31m"
FG_GREEN = "\033[32m"
FG_YELLOW = "\033[33m"
FG_BLUE = "\033[34m"
FG_MAGENTA = "\033[35m"
FG_CYAN = "\033[36m"
FG_WHITE = "\033[37m"

BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

TEXT_SPEED = 0.02  # seconds per character
FAST_TEXT_SPEED = 0.005


def supports_color():
    if sys.platform == "win32":
        return True  # Modern terminals & Warp support ANSI
    return sys.stdout.isatty()


COLOR_ENABLED = supports_color()


def c(text, *styles):
    if not COLOR_ENABLED:
        return text
    return "".join(styles) + text + RESET


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def slow_print(text, speed=TEXT_SPEED, wrap=76, indent=0):
    if wrap:
        wrapper = textwrap.TextWrapper(width=wrap, subsequent_indent=" " * indent)
        text = wrapper.fill(text)
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        if ch != " " and ch != "\n":
            time.sleep(speed)
    print()


def type_lines(lines, speed=TEXT_SPEED, wrap=76, indent=0):
    for line in lines:
        slow_print(line, speed=speed, wrap=wrap, indent=indent)


def wait_for_enter(prompt="\nPress Enter to continue..."):
    try:
        input(c(prompt, FG_CYAN, BOLD))
    except EOFError:
        pass


def draw_box(title, body_lines, color=FG_CYAN):
    all_lines = [title] + body_lines
    width = max(len(textwrap.fill(line, width=76)) for line in all_lines) + 4
    border = "+" + "-" * (width - 2) + "+"
    print(c(border, color))
    title_line = f"| {title.center(width - 4)} |"
    print(c(title_line, color, BOLD))
    print(c(border, color))
    for line in body_lines:
        wrapped = textwrap.wrap(line, width=width - 4) or [""]
        for w in wrapped:
            print(c("| " + w.ljust(width - 4) + " |", color))
    print(c(border, color))


# ==========================
# Game Data
# ==========================

CIVILIZATIONS = [
    {
        "id": "sky_nomads",
        "name": "Sky Nomads",
        "ascii_art": r"""
           .-._   _ _ _ _ _ _ _ _
        .-"     `-"   " " " " " "`-.
       /  .-.-.                     \
      /  /  \  \   SKY NOMADS       \
     |   |  |   |   balloon cities   |
      \  \__/  /                     /
       `-.___.-'~~~~~~~~~~~~~~~~~~~~'
        """,
        "motto": "We drift, therefore we dream.",
        "preferred_tags": {"calm", "stories", "air", "tea"},
        "hated_tags": {"bureaucracy", "heavy", "fire"},
    },
    {
        "id": "dino_senate",
        "name": "Dino Senate",
        "ascii_art": r"""
           __
        .-"  `-._   DINO SENATE
       /  .-._   `.
      /  /   _)   /
     /  /   (_)  /
    /  /         |
    `-"          |
       ROAR-democracy
        """,
        "motto": "Extinction is just bad scheduling.",
        "preferred_tags": {"order", "food", "tradition"},
        "hated_tags": {"tech", "chaos"},
    },
    {
        "id": "robot_gardeners",
        "name": "Robot Gardeners",
        "ascii_art": r"""
         [ROBOT GARDENERS]
           _
        _ | |  o  o  o
       | ||_| [ ] [ ] [ ]
       |_   _|  |  |  |
         |_|   green by design
        """,
        "motto": "We debug both code and carrots.",
        "preferred_tags": {"nature", "order", "tech"},
        "hated_tags": {"chaos", "noise"},
    },
    {
        "id": "floating_cat_republic",
        "name": "Floating Cat Republic",
        "ascii_art": r"""
           /\_/\   ~ Floating ~
     ____ ( o.o )  Cat Republic
    /    \\ > ^ <
    """"""`-----'   all naps, no kings
        """,
        "motto": "Liberty, treats, and naps for all.",
        "preferred_tags": {"cozy", "play", "food"},
        "hated_tags": {"bureaucracy", "strict"},
    },
    {
        "id": "bureaucracy_dimension",
        "name": "Bureaucracy Dimension",
        "ascii_art": r"""
        [BUREAUCRACY DIMENSION]
         ______________________
        |  FORM 27-B/∞        |
        |  SIGN HERE ->  ____ |
        |  STAMP STAMP STAMP |
        |_____________________|
        eternally queued
        """,
        "motto": "In triplicate we trust.",
        "preferred_tags": {"order", "bureaucracy", "paper"},
        "hated_tags": {"chaos", "play"},
    },
    {
        "id": "atlantis_2",
        "name": "Atlantis 2.0",
        "ascii_art": r"""
          ~   ~    ATLANTIS 2.0
        ~  ~  ~   glass domes below
       ~  ~  ~    and neon corals
        """,
        "motto": "We rose, sank, patched the bug, and relaunched.",
        "preferred_tags": {"tech", "water", "culture"},
        "hated_tags": {"fire", "noise"},
    },
]


PARCELS = [
    {"id": "electricity", "name": "Electricity", "tags": {"tech", "spark"}, "base_ripple": 3},
    {"id": "minimalism", "name": "Minimalism", "tags": {"calm", "aesthetic"}, "base_ripple": 2},
    {"id": "fireworks", "name": "Fireworks", "tags": {"chaos", "fire", "noise"}, "base_ripple": 4},
    {"id": "tea", "name": "Tea", "tags": {"tea", "cozy", "calm"}, "base_ripple": 1},
    {"id": "pizza", "name": "Pizza", "tags": {"food", "cozy"}, "base_ripple": 2},
    {"id": "bubblegum", "name": "Bubblegum", "tags": {"play", "chaos"}, "base_ripple": 3},
    {"id": "diplomacy", "name": "Diplomacy", "tags": {"order", "stories"}, "base_ripple": 2},
    {"id": "meditation", "name": "Meditation", "tags": {"calm", "stories"}, "base_ripple": 1},
    {"id": "fashion", "name": "Fashion", "tags": {"aesthetic", "play"}, "base_ripple": 2},
    {"id": "comedy", "name": "Comedy", "tags": {"play", "stories"}, "base_ripple": 2},
    {"id": "sneezing", "name": "Sneezing", "tags": {"chaos"}, "base_ripple": 3},
    {"id": "password_hygiene", "name": "Password Hygiene", "tags": {"order", "tech"}, "base_ripple": 2},
    {"id": "origami", "name": "Origami", "tags": {"aesthetic", "calm"}, "base_ripple": 1},
    {"id": "cloud_storage", "name": "Cloud Storage", "tags": {"tech", "air"}, "base_ripple": 3},
    {"id": "karaoke", "name": "Karaoke", "tags": {"noise", "play"}, "base_ripple": 3},
    {"id": "gardening", "name": "Gardening", "tags": {"nature", "calm"}, "base_ripple": 1},
    {"id": "street_food", "name": "Street Food", "tags": {"food", "chaos"}, "base_ripple": 3},
    {"id": "board_games", "name": "Board Games", "tags": {"play", "order"}, "base_ripple": 2},
    {"id": "time_management", "name": "Time Management", "tags": {"order", "strict"}, "base_ripple": 3},
    {"id": "cozy_blankets", "name": "Cozy Blankets", "tags": {"cozy", "calm"}, "base_ripple": 1},
]

# Make sure we meet the 20 parcel requirement
assert len(PARCELS) >= 20

PARADOX_THRESHOLD = 12
MAX_RIPPLE = 30


class GameState:
    def __init__(self):
        self.ripple_index = 0
        self.turn = 0
        self.delivered = []  # list of (parcel_id, civ_id)
        self.civ_states = {
            civ["id"]: {
                "harmony": 0,
                "chaos": 0,
                "received": [],
                "notes": [],
            }
            for civ in CIVILIZATIONS
        }
        self.tag_influence = {tag: 0 for tag in [
            "tech",
            "spark",
            "calm",
            "aesthetic",
            "chaos",
            "fire",
            "noise",
            "tea",
            "cozy",
            "food",
            "play",
            "order",
            "stories",
            "nature",
            "water",
            "air",
            "tradition",
            "bureaucracy",
            "paper",
            "strict",
            "culture",
        ]}
        self.paradoxes_resolved = 0
        self.paradoxes_triggered = 0
        self.unlocked_final = False
        self.game_over = False

    def log_delivery(self, parcel_id, civ_id):
        self.delivered.append((parcel_id, civ_id))


# ==========================
# Screens & Animations
# ==========================


def title_screen():
    clear()
    logo_lines = [
        "   ____                          _            __      __           _ _           ",
        "  / ___|___  _   _ _ __ ___  ___| |_ _   _    \\ \    / /__  _ __ (_) | ___  ___",
        " | |   / _ \\| | | | '__/ _ \\/ __| __| | | |    \\ \\  / / _ \\\/ __| | | |/ _ \\/ __|",
        " | |__| (_) | |_| | | |  __/\\__ \\ |_| |_| |     \\ \\/ / (_) \\\__ \\ | | |  __/\\__ \\",
        "  \\____\\___/ \\__,_|_|  \\___||___/\\__|\\__, |      \\__/ \\___/|___/_|_|_|\\___||___/",
        "                                         |___/                                        ",
        "",
        "                        Courier of Possibilities",
    ]
    for line in logo_lines:
        print(c(line, FG_CYAN, BOLD))
        time.sleep(0.05)

    subtitle = "A cozy, time-bending narrative puzzle about delivering ideas."
    slow_print(c(subtitle, FG_MAGENTA, ITALIC), speed=TEXT_SPEED)

    print()
    slow_print(c("Withley presents a very small, extremely polite multiverse.", FG_YELLOW), speed=TEXT_SPEED)
    print()
    wait_for_enter()


def intro_cinematic():
    clear()
    lines = [
        "The multiverse is not held together by physics.",
        "It is held together by half-baked ideas, questionable fashion,",
        "and at least three civilizations arguing about pizza toppings.",
        "",
        "You are a courier in the Interdimensional Idea Postal Service.",
        "Your job: deliver potent conceptual parcels to wildly different timelines.",
        "Every delivery nudges reality. Some nudge harder than others.",
        "",
        "Your mission: gently shepherd chaos toward a harmonious, cozy equilibrium,",
        "without letting the Ripple Index spiral into paradox-flavored soup.",
    ]
    type_lines([c(l, FG_WHITE) for l in lines], speed=TEXT_SPEED)
    print()
    wait_for_enter()


def show_civ_ascii(civ):
    print(c(civ["ascii_art"], FG_CYAN))
    print(c(f"{civ['name']}: \"{civ['motto']}\"", FG_YELLOW))


def ripple_animation(state, parcel, civ):
    clear()
    title = f"Delivering '{parcel['name']}' to {civ['name']}..."
    print(c(title, FG_GREEN, BOLD))
    print()
    phases = [
        "Packing conceptual bubble wrap...",
        "Threading through adjacent maybes...",
        "Politely knocking on causality...",
        "Teaching reality to improvise...",
    ]
    bars = ["[=         ]", "[===       ]", "[=====     ]", "[========  ]", "[==========]"]
    for i, phase in enumerate(phases):
        bar = bars[min(i, len(bars) - 1)]
        line = f" {bar} {phase}"
        print(c(line, FG_MAGENTA))
        time.sleep(0.5)
    print()
    swirl_frames = [
        " ~ ripple ~",
        "  ~~ ripple ~~",
        " ~~~ R I P P L E ~~~",
        "  ~~ ripple ~~",
        "   ~ ripple ~",
    ]
    for frame in swirl_frames:
        sys.stdout.write("\r" + c(frame.ljust(40), FG_CYAN))
        sys.stdout.flush()
        time.sleep(0.2)
    print("\n")


def show_ripple_status(state):
    bar_len = 20
    filled = min(bar_len, max(0, int(bar_len * state.ripple_index / MAX_RIPPLE)))
    bar = "#" * filled + "-" * (bar_len - filled)
    status = f"Ripple Index: [{bar}] {state.ripple_index}/{MAX_RIPPLE}"
    if state.ripple_index < PARADOX_THRESHOLD:
        color = FG_GREEN
        note = "Stable-ish. Reality is only gently humming."
    elif state.ripple_index < MAX_RIPPLE * 0.75:
        color = FG_YELLOW
        note = "Spicy timelines detected. Handle with tea."
    else:
        color = FG_RED
        note = "Paradox sirens warming up. Maybe stop throwing fireworks at history."
    print(c(status, color, BOLD))
    print(c(note, FG_MAGENTA))


# ==========================
# Core Mechanics
# ==========================


def choose_parcel(state):
    clear()
    print(c("=== IDEA PARCEL SELECTION ===", FG_CYAN, BOLD))
    print()
    available = PARCELS[:]  # simple model: all available always
    random.shuffle(available)
    choices = available[:5]

    for idx, parcel in enumerate(choices, start=1):
        tags = ", ".join(sorted(parcel["tags"]))
        print(c(f"[{idx}] {parcel['name']}", FG_YELLOW, BOLD))
        print(c(f"    Tags: {tags}", FG_WHITE))
    print(c("[R] Refresh selection", FG_BLUE))

    while True:
        choice = input(c("Select a parcel (number) or R: ", FG_CYAN)).strip().lower()
        if choice == "r":
            return choose_parcel(state)
        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= len(choices):
                return choices[num - 1]
        print(c("Gentle nudge: that's not in the catalog.", FG_RED))


def choose_civilization(state):
    clear()
    print(c("=== DESTINATION TIMELINE ===", FG_CYAN, BOLD))
    print()
    for idx, civ in enumerate(CIVILIZATIONS, start=1):
        cs = state.civ_states[civ["id"]]
        mood = "balanced"
        if cs["harmony"] > cs["chaos"] + 2:
            mood = "glowingly content"
        elif cs["chaos"] > cs["harmony"] + 2:
            mood = "dramatically wobbly"
        print(c(f"[{idx}] {civ['name']}", FG_YELLOW, BOLD), end=" ")
        print(c(f"(harmony {cs['harmony']:+}, chaos {cs['chaos']:+}) - {mood}", FG_WHITE))
    print()

    while True:
        choice = input(c("Select a destination (number): ", FG_CYAN)).strip()
        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= len(CIVILIZATIONS):
                return CIVILIZATIONS[num - 1]
        print(c("Timeline not found. Did you misplace a digit?", FG_RED))


COMEDIC_SIDE_EFFECTS = [
    "accidentally standardizes the universe-wide definition of 'just a minute'.",
    "causes three parallel universes to agree on pineapple pizza, briefly.",
    "adds a footnote to gravity that says 'when convenient'.",
    "inspires a hit musical about filing cabinets.",
    "teaches clouds to form constructive feedback.",
    "results in polite time-travel tourism brochures.",
]


def apply_parcel_effects(state, parcel, civ):
    cs = state.civ_states[civ["id"]]
    tags = parcel["tags"]

    harmony_delta = 0
    chaos_delta = 0
    ripple_delta = parcel["base_ripple"]

    if tags & civ["preferred_tags"]:
        harmony_delta += 2
        ripple_delta -= 1
    if tags & civ["hated_tags"]:
        harmony_delta -= 2
        chaos_delta += 2
        ripple_delta += 2

    if "chaos" in tags:
        chaos_delta += 1
    if "calm" in tags or "cozy" in tags:
        harmony_delta += 1
        ripple_delta = max(0, ripple_delta - 1)

    harmony_delta += random.choice([-1, 0, 0, 1])

    cs["harmony"] += harmony_delta
    cs["chaos"] += chaos_delta
    cs["received"].append(parcel["id"])

    for tag in tags:
        if tag in state.tag_influence:
            state.tag_influence[tag] += 1

    state.ripple_index = max(0, min(MAX_RIPPLE, state.ripple_index + ripple_delta))
    state.log_delivery(parcel["id"], civ["id"])

    effect_lines = []
    side = random.choice(COMEDIC_SIDE_EFFECTS)
    effect_lines.append(f"The parcel {side}")
    effect_lines.append(
        f"In {civ['name']}, harmony shifts by {harmony_delta:+}, chaos by {chaos_delta:+}."
    )

    if harmony_delta > 1:
        cs["notes"].append(f"Grateful for {parcel['name']}")
    elif harmony_delta < 0:
        cs["notes"].append(f"Suspicious about {parcel['name']}")

    return effect_lines


def mission_phase(state, parcel, civ):
    clear()
    title = f"Mission Debrief: {parcel['name']} -> {civ['name']}"
    cs = state.civ_states[civ["id"]]

    desc_options = [
        "A local council requests your guidance.",
        "A small committee of very curious beings corners you.",
        "An ad-hoc festival forms around your delivery.",
        "A politely urgent message pings your multidimensional pager.",
    ]
    scenario = random.choice(desc_options)

    body = [
        scenario,
        "",
        "They ask how to lean into this new idea.",
    ]
    draw_box(title, body, color=FG_BLUE)

    options = [
        (
            "Encourage gentle experimentation.",
            {"harmony": +1, "chaos": 0, "ripple": +1},
            "You suggest small cozy pilots and lots of tea breaks.",
        ),
        (
            "Push for bold, flashy change.",
            {"harmony": 0, "chaos": +2, "ripple": +2},
            "You sketch a headline-grabbing timeline pivot.",
        ),
        (
            "Advise careful documentation and patience.",
            {"harmony": +1, "chaos": -1, "ripple": 0},
            "You gift them a color-coded, mildly adorable manual.",
        ),
    ]

    print()
    for i, (label, _, _) in enumerate(options, start=1):
        print(c(f"[{i}] {label}", FG_YELLOW))
    print()

    choice_idx = None
    while choice_idx is None:
        choice = input(c("How do you advise them? ", FG_CYAN)).strip()
        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= len(options):
                choice_idx = num - 1
                break
        print(c("That's not one of your carefully curated options.", FG_RED))

    label, deltas, flavor = options[choice_idx]
    slow_print(c(flavor, FG_WHITE), speed=TEXT_SPEED)

    cs["harmony"] += deltas["harmony"]
    cs["chaos"] += deltas["chaos"]
    state.ripple_index = max(0, min(MAX_RIPPLE, state.ripple_index + deltas["ripple"]))

    print()
    show_ripple_status(state)
    wait_for_enter()


def paradox_phase(state):
    state.paradoxes_triggered += 1
    clear()
    title = "Paradox Alert"
    body = [
        "Timeline threads begin to tangle into an aesthetically concerning knot.",
        "Somewhere, a committee of probability waves clears its throat.",
    ]
    draw_box(title, body, color=FG_RED)
    print()

    scenarios = [
        {
            "text": "Two civilizations invent the same board game, but with opposing rules.",
            "options": [
                (
                    "Let them argue it out. It's character-building.",
                    {"ripple": +3, "harmony_all": 0},
                    "The debate becomes a multiverse-wide reality show.",
                ),
                (
                    "Quietly standardize the rules in the archives.",
                    {"ripple": -3, "harmony_all": -1},
                    "Some timelines grumble about 'patch notes', but it works.",
                ),
                (
                    "Create a crossover tournament with both rule sets.",
                    {"ripple": -1, "harmony_all": +1},
                    "Chaos becomes camaraderie, with themed snacks.",
                ),
            ],
        },
        {
            "text": "A parcel of Fireworks arrives exactly five minutes before its own invention.",
            "options": [
                (
                    "Label it 'research preview' and shrug.",
                    {"ripple": +2, "harmony_all": 0},
                    "History textbooks add a mysterious asterisk.",
                ),
                (
                    "Carefully re-route it to a timeline that already had fireworks.",
                    {"ripple": -3, "harmony_all": 0},
                    "Paradox diffused with minimal glitter.",
                ),
                (
                    "Host a cross-temporal safety workshop.",
                    {"ripple": -1, "harmony_all": +1},
                    "Everyone leaves with earplugs and fond memories.",
                ),
            ],
        },
    ]

    scenario = random.choice(scenarios)
    slow_print(c(scenario["text"], FG_WHITE), speed=TEXT_SPEED)
    print()

    for i, (label, _, _) in enumerate(scenario["options"], start=1):
        print(c(f"[{i}] {label}", FG_YELLOW))

    choice_idx = None
    while choice_idx is None:
        choice = input(c("Choose a paradox patch: ", FG_CYAN)).strip()
        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= len(scenario["options"]):
                choice_idx = num - 1
                break
        print(c("The paradox remains unimpressed by that input.", FG_RED))

    label, deltas, flavor = scenario["options"][choice_idx]
    print()
    slow_print(c(flavor, FG_WHITE), speed=TEXT_SPEED)

    # Apply to all civs
    for cs in state.civ_states.values():
        cs["harmony"] += deltas["harmony_all"]

    state.ripple_index = max(0, min(MAX_RIPPLE, state.ripple_index + deltas["ripple"]))
    state.paradoxes_resolved += 1

    print()
    show_ripple_status(state)
    wait_for_enter()


def check_final_puzzle_unlock(state):
    if state.unlocked_final:
        return True
    if len(state.delivered) < 8:
        return False
    avg_harmony = sum(cs["harmony"] for cs in state.civ_states.values()) / len(state.civ_states)
    if avg_harmony < -1:
        return False
    if state.ripple_index > int(MAX_RIPPLE * 0.8):
        return False

    clear()
    title = "Multiverse Alignment Threshold Reached"
    body = [
        "Branches of reality begin humming in an almost-chord.",
        "A final, delicate adjustment could harmonize them all... or scatter them like confetti.",
    ]
    draw_box(title, body, color=FG_GREEN)
    print()
    show_ripple_status(state)
    print()
    ans = input(c("Attempt the 'Harmonize the Multiverse' protocol now? (y/n): ", FG_CYAN)).strip().lower()
    if ans.startswith("y"):
        state.unlocked_final = True
        return True
    return False


def final_harmony_puzzle(state):
    clear()
    title = "Harmonize the Multiverse"
    body = [
        "You enter the Lounge Between Timelines, where realities overlap like cozy blankets.",
        "A console awaits you, displaying the emotional waveform of every civilization you've visited.",
        "To stabilize everything, you must tune three core parameters.",
    ]
    draw_box(title, body, color=FG_MAGENTA)
    print()
    score = 0

    # Step 1
    print(c("Step 1: Choose the guiding principle.", FG_CYAN, BOLD))
    opts1 = [
        ("Maximize spectacle at all costs.", 0, "Fireworks forever, naps never."),
        ("Cozy connection and mutual understanding.", 1, "Tea, stories, and reasonable snack budgets."),
        ("Endless paperwork to prevent surprises.", 0, "Everything predictable, nothing delightful."),
    ]
    for i, (label, _, _) in enumerate(opts1, start=1):
        print(c(f"[{i}] {label}", FG_YELLOW))
    choice = ask_option(len(opts1))
    _, val, desc = opts1[choice]
    slow_print(c(desc, FG_WHITE), speed=TEXT_SPEED)
    score += val
    print()

    # Step 2
    print(c("Step 2: Broadcast one idea to every civilization at once.", FG_CYAN, BOLD))
    opts2 = [
        ("Tea", 1, "The multiverse exhales in unison."),
        ("Fireworks", 0, "Colorful, loud, mildly singed."),
        ("Time Management", 0, "Everyone is on time and vaguely stressed."),
    ]
    for i, (label, _, _) in enumerate(opts2, start=1):
        print(c(f"[{i}] {label}", FG_YELLOW))
    choice = ask_option(len(opts2))
    _, val, desc = opts2[choice]
    slow_print(c(desc, FG_WHITE), speed=TEXT_SPEED)
    score += val
    print()

    # Step 3
    print(c("Step 3: Set the tempo of causality.", FG_CYAN, BOLD))
    opts3 = [
        ("Slow and steady, with room for naps.", 1, "History becomes a well-paced cozy novel."),
        ("Chaotic jazz solo.", 0, "Exciting, but hard to schedule."),
        ("Endless bureaucratic queue.", 0, "Nothing breaks, but nothing starts."),
    ]
    for i, (label, _, _) in enumerate(opts3, start=1):
        print(c(f"[{i}] {label}", FG_YELLOW))
    choice = ask_option(len(opts3))
    _, val, desc = opts3[choice]
    slow_print(c(desc, FG_WHITE), speed=TEXT_SPEED)
    score += val

    print()
    slow_print(c("The console hums, analyzing your choices...", FG_WHITE), speed=TEXT_SPEED)
    time.sleep(1.0)
    print()

    # Determine ending
    if score >= 3 and state.ripple_index <= PARADOX_THRESHOLD:
        ending_golden_harmony(state)
    elif score >= 2 and state.ripple_index < MAX_RIPPLE:
        ending_bittersweet(state)
    else:
        ending_chaotic_carousel(state)


def ask_option(max_num):
    while True:
        ans = input(c("Choose: ", FG_CYAN)).strip()
        if ans.isdigit():
            num = int(ans)
            if 1 <= num <= max_num:
                return num - 1
        print(c("The console blinks politely. Try a listed option.", FG_RED))


# ==========================
# Endings & Credits
# ==========================


def ending_golden_harmony(state):
    clear()
    title = "Ending: Golden Harmony"
    body = [
        "Timelines settle into a resonant chord that feels like the first sip of warm tea.",
        "Sky Nomads trade wind stories with Atlantis engineers.",
        "Robot Gardeners host cross-dimensional farmers' markets.",
        "The Floating Cat Republic unionizes nap zones across realities.",
        "Even the Bureaucracy Dimension discovers the concept of 'short form'.",
    ]
    draw_box(title, body, color=FG_GREEN)
    print()
    slow_print(c("Your deliveries didn't just avoid disaster.", FG_WHITE), speed=TEXT_SPEED)
    slow_print(c("They composed a multiverse where possibility feels gentle and kind.", FG_WHITE), speed=TEXT_SPEED)
    print()
    show_ripple_status(state)
    wait_for_enter()
    credits()


def ending_bittersweet(state):
    clear()
    title = "Ending: Bittersweet Mosaic"
    body = [
        "The multiverse stabilizes, mostly.",
        "Some timelines glow with cozy cooperation; others remain a bit spicy.",
        "Paradox-resistant paperwork circulates alongside pizza-fueled festivals.",
        "A few worlds still debate board game rules, but now it's mostly for fun.",
    ]
    draw_box(title, body, color=FG_YELLOW)
    print()
    slow_print(c("You steered infinity away from catastrophe and toward something livable.", FG_WHITE), speed=TEXT_SPEED)
    slow_print(c("Not perfect. But wonderfully, stubbornly possible.", FG_WHITE), speed=TEXT_SPEED)
    print()
    show_ripple_status(state)
    wait_for_enter()
    credits()


def ending_chaotic_carousel(state):
    clear()
    title = "Ending: Cozy Chaotic Carousel"
    body = [
        "Reality never quite settles.",
        "Timeline branches loop and twist like a cosmic theme park.",
        "Fireworks misfire into underwater karaoke bars.",
        "Dino senators debate fashion trends with floating cats in formal capes.",
        "And yet... somehow, everyone keeps finding room for naps and tea.",
    ]
    draw_box(title, body, color=FG_MAGENTA)
    print()
    slow_print(c("You didn't so much harmonize the multiverse as teach it to improvise.", FG_WHITE), speed=TEXT_SPEED)
    slow_print(c("It's chaotic. It's cozy. It's home.", FG_WHITE), speed=TEXT_SPEED)
    print()
    show_ripple_status(state)
    wait_for_enter()
    credits()


def credits():
    clear()
    lines = [
        "Courier of Possibilities",
        "A tiny multiverse management adventure.",
        "",
        "Design, code, and improbable logistics:  WiThley (with your good taste)",
        "Concept parcels: Electricity, Tea, Pizza, and friends",
        "Timelines stabilized: hopefully yours, a little bit, too.",
    ]
    draw_box("Credits", lines, color=FG_CYAN)
    print()
    slow_print(c("Thank you for delivering possibilities.", FG_WHITE), speed=TEXT_SPEED)
    slow_print(c("You can always replay to explore different branches.", FG_WHITE), speed=TEXT_SPEED)
    print()


# ==========================
# Main Game Loop
# ==========================


def main_loop():
    state = GameState()
    title_screen()
    intro_cinematic()

    while not state.unlocked_final and not state.game_over:
        state.turn += 1
        parcel = choose_parcel(state)
        civ = choose_civilization(state)

        ripple_animation(state, parcel, civ)
        clear()
        show_civ_ascii(civ)
        print()
        slow_print(c(f"You hand over the parcel of {parcel['name']}.", FG_WHITE), speed=TEXT_SPEED)
        print()

        effect_lines = apply_parcel_effects(state, parcel, civ)
        type_lines([c(line, FG_WHITE) for line in effect_lines], speed=TEXT_SPEED)
        print()
        show_ripple_status(state)
        print()
        wait_for_enter()

        mission_phase(state, parcel, civ)

        if state.ripple_index >= PARADOX_THRESHOLD:
            paradox_phase(state)

        if check_final_puzzle_unlock(state):
            break

        

        clear()
        print(c("=== COURIER STATUS ===", FG_CYAN, BOLD))
        print()
        show_ripple_status(state)
        print()
        print(c("[Enter] Continue deliveries", FG_YELLOW))
        print(c("[Q]      Retire for now", FG_YELLOW))
        ans = input(c("Choice: ", FG_CYAN)).strip().lower()
        if ans == "q":
            state.game_over = True
            break

    if state.unlocked_final and not state.game_over:
        final_harmony_puzzle(state)
    elif state.game_over:
        clear()
        slow_print(c("You place your courier bag on the hook and let the timelines simmer.", FG_WHITE), speed=TEXT_SPEED)
        slow_print(c("They'll be here, humming with possibility, when you return.", FG_WHITE), speed=TEXT_SPEED)
        print()


    
    
if __name__ == "__main__":
    try:


        main_loop()
    except KeyboardInterrupt:
        print("\n" + c("Courier link gracefully closed.", FG_CYAN))


