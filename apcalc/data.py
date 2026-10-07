"""Names and IDs shared by the world and the game.

The Unity game (APItems.cs, APLocations.cs) is the source of truth; this is
its mirror. test_data compares the two against test/unity_tables.json, which
is exported from the game itself (tools/export_unity_tables.cs), so a name or
id that drifts on either side fails a test instead of a seed.

Free of Archipelago imports so it can be checked without a checkout.
"""

from __future__ import annotations

#: The Archipelago game identifier. archipelago.json and the docs filename
#: carry their own copies; test_data checks they agree.
GAME_NAME = "AP Calc"

# ── tiers and keys ─────────────────────────────────────────────────────────

EASY, MEDIUM, HARD, AP = "Easy", "Medium", "Hard", "AP"

MEDIUM_TIER = "Medium Difficulty"
HARD_TIER = "Hard Difficulty"
AP_TIER = "AP Difficulty"
TIER_ITEMS = {MEDIUM: MEDIUM_TIER, HARD: HARD_TIER, AP: AP_TIER}

#: Every key with an item and a first-use check, in the game's order (ids
#: follow it). ")" isn't here: it unlocks with "(" and is never an item.
#: (symbol, kind, tier). The item is "<kind> <clean>", where clean drops the
#: trailing "(" of a function: "Function sin", "Operator (".
KEYS: list[tuple[str, str, str]] = (
    [(str(d), "Digit", EASY) for d in range(10)]
    + [(op, "Operator", EASY) for op in ("+", "-", "*", "/")]
    + [("(", "Operator", MEDIUM), ("^", "Operator", MEDIUM), (".", "Operator", MEDIUM),
       ("!", "Operator", HARD)]
    + [("sqrt(", "Function", MEDIUM)]
    + [(f, "Function", HARD) for f in ("sin(", "cos(", "tan(", "log(", "log10(")]
    + [(f, "Function", AP) for f in ("e", "x", "y", "z",
                                      "d/dx(", "d/dy(", "d/dz(",
                                      "∫dx(", "∫dy(", "∫dz(")]
)


def clean(symbol: str) -> str:
    return symbol[:-1] if len(symbol) > 1 and symbol.endswith("(") else symbol


def key_item(symbol: str, kind: str) -> str:
    return f"{kind} {clean(symbol)}"


KEY_ITEMS = [key_item(s, k) for s, k, _ in KEYS]
KEY_TIER = {key_item(s, k): t for s, k, t in KEYS}
ITEM_FOR_SYMBOL = {s: key_item(s, k) for s, k, _ in KEYS}

DIGITS = [ITEM_FOR_SYMBOL[str(d)] for d in range(10)]
NONZERO_DIGITS = DIGITS[1:]
#: The operators a starting kit may hold: any of them makes every whole
#: number up to the first magnitude buildable from digits.
SAFE_OPERATORS = [ITEM_FOR_SYMBOL[op] for op in ("+", "-", "*")]


def kit_can_target(digits: list[int], operator: str) -> bool:
    """Whether the game can show a first target with these keys. It builds
    targets as "a op b" from the player's digits, and before any Progressive
    Magnitude only 1 to 9 fit: 5, 7, 9 with just + (or 4, 5, 6 with just *)
    can't make one, and the run would be stuck at its first target."""
    def value(a: int, b: int) -> int:
        return a + b if operator == "+" else a - b if operator == "-" else a * b
    return any(1 <= value(a, b) <= 9 for a in digits for b in digits)

# ── other items ────────────────────────────────────────────────────────────

MAGNITUDE = "Progressive Magnitude"
DECIMAL = "Progressive Decimal"
NEGATIVE = "Negative Numbers"
MAGNITUDE_COPIES = 6
DECIMAL_COPIES = 2

HINT, SKIP, FREEBIE = "Hint", "Skip", "Freebie"
POWER_UPS = [HINT, SKIP, FREEBIE]

SMALL_CREDIT = "100 Extra Credit"
BIG_CREDIT = "250 Extra Credit"
CARD_PACK = "Card Pack"
STREAK_SAVER = "Streak Saver"
PEP_TALK = "Pep Talk"
CONFETTI = "Confetti"

TRAPS = ["Freeze Trap", "Dessert Trap", "Invisibility Trap", "Clear Equation Trap", "Locked Operator Trap"]

ITEM_NAME_TO_ID: dict[str, int] = {
    MEDIUM_TIER: 400000,
    HARD_TIER: 400001,
    AP_TIER: 400002,
    **{name: 400010 + i for i, name in enumerate(KEY_ITEMS)},
    MAGNITUDE: 400050,
    DECIMAL: 400051,
    NEGATIVE: 400052,
    HINT: 400060,
    SKIP: 400061,
    FREEBIE: 400062,
    SMALL_CREDIT: 400070,
    BIG_CREDIT: 400071,
    CARD_PACK: 400072,
    STREAK_SAVER: 400073,
    PEP_TALK: 400074,
    CONFETTI: 400075,
    **{name: 400080 + i for i, name in enumerate(TRAPS)},
}


def _keys(*symbols: str) -> set[str]:
    return {ITEM_FOR_SYMBOL[s] for s in symbols}


#: Item groups, for !hint, plando and start_inventory ("!hint Digits").
ITEM_GROUPS: dict[str, set[str]] = {
    "Keys": set(KEY_ITEMS),
    "Digits": set(DIGITS),
    "Operators": {key_item(s, k) for s, k, _ in KEYS if k == "Operator"},
    "Basic Operators": _keys("+", "-", "*", "/"),
    "Functions": {key_item(s, k) for s, k, _ in KEYS if k == "Function"},
    "Trig": _keys("sin(", "cos(", "tan("),
    "Logarithms": _keys("log(", "log10("),
    "Variables": _keys("x", "y", "z"),
    "Derivatives": _keys("d/dx(", "d/dy(", "d/dz("),
    "Integrals": _keys("∫dx(", "∫dy(", "∫dz("),
    "Calculus": _keys("d/dx(", "d/dy(", "d/dz(", "∫dx(", "∫dy(", "∫dz("),
    "Easy Keys": {name for name in KEY_ITEMS if KEY_TIER[name] == EASY},
    "Medium Keys": {name for name in KEY_ITEMS if KEY_TIER[name] == MEDIUM},
    "Hard Keys": {name for name in KEY_ITEMS if KEY_TIER[name] == HARD},
    "AP Keys": {name for name in KEY_ITEMS if KEY_TIER[name] == AP},
    "Difficulties": set(TIER_ITEMS.values()),
    "Target Range": {MAGNITUDE, DECIMAL, NEGATIVE},
    "Power-Ups": set(POWER_UPS),
    "Extra Credit": {SMALL_CREDIT, BIG_CREDIT},
    "Traps": set(TRAPS),
}

# ── locations ──────────────────────────────────────────────────────────────

#: The game's goal field tops out here (Settings > Game), and so do the
#: equation checks.
MAX_EQUATIONS = 100

FUNNY_NUMBERS = [67, 69, 420, 666, 777, 1337, 80085]


def equation_name(n: int) -> str:
    return f"Equation {n}"


def first_use_name(item: str) -> str:
    return f"First Solve Using {item}"


def power_up_name(power_up: str) -> str:
    return f"First {power_up} Used"


def funny_name(n: int) -> str:
    return f"Funny Number {n}"


#: The Archipelago shop: checks bought in the card shop with Extra Credit
#: earned during the run. options.shop_slots of these exist.
MAX_SHOP_SLOTS = 25


def shop_name(k: int) -> str:
    return f"Shop Item {k}"


def shop_prices(goal_count: int, slots: int, percent: int) -> list[int]:
    """What each shop slot costs, cheapest first, in steps of 5 EC.

    However many slots it's split into, the whole shop comes to about 55 EC
    per equation of the goal (times percent/100): roughly what a run earns,
    so the last slot is bought around the goal. The k-th slot costs k shares.
    """
    if slots <= 0:
        return []
    total = goal_count * 55 * percent / 100
    share = total / (slots * (slots + 1) / 2)
    return [max(5, int(round(share * k / 5)) * 5) for k in range(1, slots + 1)]


# ── challenge checks ── each kind has its own option (options.py).

#: Correct answers in a row.
STREAKS = [5, 10, 25]
#: Seconds from a target appearing to solving it.
SPEED_SECONDS = [10, 5]
#: Different keys in one answer.
VARIETY_KEYS = [6, 8, 10]
NO_PLUS_MINUS = "Solve Without + Or -"
ALL_FOUR_OPERATORS = "Solve Using + - * And /"
OPERATOR_CHECKS = [NO_PLUS_MINUS, ALL_FOUR_OPERATORS]


def streak_name(n: int) -> str:
    return f"Streak Of {n}"


def speed_name(seconds: int) -> str:
    return f"Solve In Under {seconds} Seconds"


def variety_name(n: int) -> str:
    return f"Solve Using {n} Different Keys"


STREAK_CHECKS = [streak_name(n) for n in STREAKS]
SPEED_CHECKS = [speed_name(s) for s in SPEED_SECONDS]
VARIETY_CHECKS = [variety_name(n) for n in VARIETY_KEYS]

LOCATION_NAME_TO_ID: dict[str, int] = {
    **{equation_name(n): 200000 + n for n in range(1, MAX_EQUATIONS + 1)},
    **{first_use_name(item): 300000 + i for i, item in enumerate(KEY_ITEMS)},
    **{power_up_name(p): 300100 + i for i, p in enumerate(POWER_UPS)},
    **{funny_name(n): 300200 + i for i, n in enumerate(FUNNY_NUMBERS)},
    **{shop_name(k): 300300 + k - 1 for k in range(1, MAX_SHOP_SLOTS + 1)},
    **{name: 300400 + i for i, name in enumerate(STREAK_CHECKS)},
    **{name: 300410 + i for i, name in enumerate(SPEED_CHECKS)},
    **{name: 300420 + i for i, name in enumerate(VARIETY_CHECKS)},
    **{name: 300430 + i for i, name in enumerate(OPERATOR_CHECKS)},
}

#: Location groups, for !hint_location, exclude_locations and the like.
LOCATION_GROUPS: dict[str, set[str]] = {
    "Equations": {equation_name(n) for n in range(1, MAX_EQUATIONS + 1)},
    "First Uses": {first_use_name(item) for item in KEY_ITEMS} | {power_up_name(p) for p in POWER_UPS},
    "Funny Numbers": {funny_name(n) for n in FUNNY_NUMBERS},
    "Shop": {shop_name(k) for k in range(1, MAX_SHOP_SLOTS + 1)},
    "Streaks": set(STREAK_CHECKS),
    "Speed": set(SPEED_CHECKS),
    "Variety": set(VARIETY_CHECKS),
    "Operator Challenges": set(OPERATOR_CHECKS),
}
