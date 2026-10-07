from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from Options import OptionError

from .data import (
    BIG_CREDIT, CARD_PACK, CONFETTI, DECIMAL, DECIMAL_COPIES, FREEBIE, FUNNY_NUMBERS, GAME_NAME, HINT,
    ITEM_NAME_TO_ID, KEY_ITEMS, MAGNITUDE, MAGNITUDE_COPIES, NEGATIVE, NONZERO_DIGITS, DIGITS, PEP_TALK,
    POWER_UPS, SAFE_OPERATORS, SKIP, SMALL_CREDIT, STREAK_SAVER, TIER_ITEMS, TRAPS, kit_can_target,
)

if TYPE_CHECKING:
    from .world import APCalcWorld

P, U, F, T = (ItemClassification.progression, ItemClassification.useful,
              ItemClassification.filler, ItemClassification.trap)

#: How each item is classified when created by name. The first copy of each
#: power-up is progression (its First X Used check needs it); extra copies are
#: made with EXTRA_COPY instead. Magnitude, Decimal and Negative change what
#: targets look like but no check depends on them, so they're useful.
CLASSIFICATIONS: dict[str, ItemClassification] = {
    **{name: P for name in TIER_ITEMS.values()},
    **{name: P for name in KEY_ITEMS},
    MAGNITUDE: U, DECIMAL: U, NEGATIVE: U,
    **{name: P for name in POWER_UPS},
    SMALL_CREDIT: F, BIG_CREDIT: F, PEP_TALK: F, CONFETTI: F,
    CARD_PACK: U, STREAK_SAVER: U,
    **{name: T for name in TRAPS},
}

#: Extra power-ups: a spare Freebie is a solved equation, so it's useful.
EXTRA_COPY = {HINT: F, SKIP: F, FREEBIE: U}

#: What fills the rest of the pool, by weight. Power-ups here are extra copies.
FILLER_WEIGHTS = {
    SMALL_CREDIT: 20, BIG_CREDIT: 10, HINT: 14, SKIP: 10, FREEBIE: 6,
    CARD_PACK: 8, STREAK_SAVER: 8, PEP_TALK: 12, CONFETTI: 12,
}
#: Items that may go anywhere, excluded locations included.
PLAIN_FILLER = {SMALL_CREDIT: 2, BIG_CREDIT: 1, PEP_TALK: 1, CONFETTI: 1}


class APCalcItem(Item):
    game = GAME_NAME


def create_item(world: APCalcWorld, name: str, classification: ItemClassification | None = None) -> APCalcItem:
    return APCalcItem(name, classification if classification is not None else CLASSIFICATIONS[name],
                      ITEM_NAME_TO_ID[name], world.player)


def _weighted(world: APCalcWorld, weights: dict[str, int]) -> str:
    names = list(weights)
    return world.random.choices(names, weights=[weights[n] for n in names])[0]


def plain_filler_name(world: APCalcWorld) -> str:
    """Filler or a trap: never useful, so it can land on an excluded check."""
    if world.random.randint(0, 99) < world.options.trap_chance:
        return world.random.choice(TRAPS)
    return _weighted(world, PLAIN_FILLER)


def _filler_item(world: APCalcWorld) -> APCalcItem:
    if world.random.randint(0, 99) < world.options.trap_chance:
        return create_item(world, world.random.choice(TRAPS))
    name = _weighted(world, FILLER_WEIGHTS)
    return create_item(world, name, EXTRA_COPY.get(name))


def choose_starting_kit(world: APCalcWorld) -> list[str]:
    """A non-zero digit, two more digits and one of + - *. Without it no
    equation can be built, so nothing could be checked at the start and the
    seed couldn't generate. Drawn again until the game can build a first
    target from it (kit_can_target). The game draws its own the same way when
    tested without a server (APItems.RandomStartingKit)."""
    while True:
        first = world.random.choice(NONZERO_DIGITS)
        rest = [d for d in DIGITS if d != first]
        kit = [first] + world.random.sample(rest, 2)
        kit.append(world.random.choice(SAFE_OPERATORS))
        if kit_can_target([DIGITS.index(d) for d in kit[:3]], kit[3].split(" ", 1)[1]):
            return kit


def create_all_items(world: APCalcWorld) -> None:
    capacity = len(world.multiworld.get_unfilled_locations(world.player))

    kit = set(choose_starting_kit(world))
    for name in sorted(kit):
        world.push_precollected(create_item(world, name))

    pool: list[Item] = [create_item(world, name) for name in TIER_ITEMS.values()]
    pool += [create_item(world, name) for name in KEY_ITEMS if name not in kit]
    pool += [create_item(world, MAGNITUDE) for _ in range(MAGNITUDE_COPIES)]
    pool += [create_item(world, DECIMAL) for _ in range(DECIMAL_COPIES)]
    pool.append(create_item(world, NEGATIVE))
    pool += [create_item(world, name) for name in POWER_UPS]

    if len(pool) > capacity:
        raise OptionError(f"{GAME_NAME}: {len(pool)} required items but only {capacity} checks. "
                          f"Raise goal_count or use equation_checks: every.")

    # The funny numbers only take filler or traps, so make sure there's at
    # least one plain item for each before the weighted mix.
    plain = min(len(FUNNY_NUMBERS), capacity - len(pool))
    pool += [create_item(world, plain_filler_name(world)) for _ in range(plain)]
    pool += [_filler_item(world) for _ in range(capacity - len(pool))]
    world.multiworld.itempool += pool
