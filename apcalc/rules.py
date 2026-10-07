"""Access rules.

Every target in an Archipelago run is built backwards from an answer typed
with keys the player has, so solving equations never needs anything: Equation
1..N are free. What logic decides is when a key's first-use check can be done,
which needs the key, its tier (and, with tier_order sequential, the tiers
below it), and whatever else it takes to fit that key into a correct answer.

Digits, + - * /, ^ ! and sqrt( turn up in the game's own built answers, so
having the key is enough (sqrt( and ! need a digit to apply to that the
answers can use). The rest never appear in a built answer and have to be
worked in by the player, so the rules ask for the pieces of a dependable way
to do it:

  (  .           any answer can be bracketed, or a whole number written 4.0
  sin( tan(      add sin(0) / tan(0):   needs 0 and + or -
  cos(           multiply by cos(0):    needs 0 and * or /
  log( log10(    add log(1):            needs 1 and + or -
  x y z          an algebra target in that variable: x+x+x, or x*x
  e              pad an algebra answer with +e-e
  d/dx( ∫dx( …   their own variable, with + and * (d/dx(x*x), ∫dx(x+x))

These are deliberately conservative: logic may expect a little more than the
game strictly needs, never less.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.rules import Has, HasAll, HasAny, Rule

from .data import (
    AP, AP_TIER, EASY, FUNNY_NUMBERS, HARD, HARD_TIER, ITEM_FOR_SYMBOL, KEY_ITEMS, KEY_TIER, MEDIUM, MEDIUM_TIER,
    POWER_UPS, first_use_name, funny_name, power_up_name,
)
from .options import TierOrder

if TYPE_CHECKING:
    from .world import APCalcWorld


def key(symbol: str) -> str:
    return ITEM_FOR_SYMBOL[symbol]


def tier_rule(world: APCalcWorld, tier: str) -> Rule | None:
    if tier == EASY:
        return None
    if world.options.tier_order == TierOrder.option_any:
        return Has({MEDIUM: MEDIUM_TIER, HARD: HARD_TIER, AP: AP_TIER}[tier])
    chain = {MEDIUM: [MEDIUM_TIER], HARD: [MEDIUM_TIER, HARD_TIER], AP: [MEDIUM_TIER, HARD_TIER, AP_TIER]}[tier]
    return HasAll(*chain)


def _any(*symbols: str) -> Rule:
    return HasAny(*(key(s) for s in symbols))


#: What else each key needs to be worked into a correct answer (see above).
#: Keys not listed need only themselves and their tier.
EXTRA: dict[str, callable] = {
    "sqrt(": lambda: _any("1", "4", "9"),
    "!":     lambda: _any("0", "1", "2", "3"),
    "sin(":  lambda: Has(key("0")) & _any("+", "-"),
    "tan(":  lambda: Has(key("0")) & _any("+", "-"),
    "cos(":  lambda: Has(key("0")) & _any("*", "/"),
    "log(":  lambda: Has(key("1")) & _any("+", "-"),
    "log10(": lambda: Has(key("1")) & _any("+", "-"),
    "x":     lambda: _any("+", "*"),
    "y":     lambda: _any("+", "*"),
    "z":     lambda: _any("+", "*"),
    "e":     lambda: _any("x", "y", "z") & HasAll(key("+"), key("-")),
    "d/dx(": lambda: HasAll(key("x"), key("+"), key("*")),
    "d/dy(": lambda: HasAll(key("y"), key("+"), key("*")),
    "d/dz(": lambda: HasAll(key("z"), key("+"), key("*")),
    "∫dx(": lambda: HasAll(key("x"), key("+"), key("*")),
    "∫dy(": lambda: HasAll(key("y"), key("+"), key("*")),
    "∫dz(": lambda: HasAll(key("z"), key("+"), key("*")),
}


def first_use_rule(world: APCalcWorld, symbol: str) -> Rule:
    item = key(symbol)
    rule: Rule = Has(item)
    tier = tier_rule(world, KEY_TIER[item])
    if tier is not None:
        rule = rule & tier
    if symbol in EXTRA:
        rule = rule & EXTRA[symbol]()
    return rule


def funny_rule(n: int) -> Rule:
    """Reachable once n can be written as (n - d) + d with d its last digit
    and n - d ending in 0: its digits, a 0, and +. Only reachability: these
    are excluded, and the game shows them by chance."""
    digits = sorted(set(str(n)) | {"0"})
    return HasAll(*(key(d) for d in digits), key("+"))


def set_all_rules(world: APCalcWorld) -> None:
    for item in KEY_ITEMS:
        symbol = next(s for s, i in ITEM_FOR_SYMBOL.items() if i == item)
        world.set_rule(world.get_location(first_use_name(item)), first_use_rule(world, symbol))

    for power_up in POWER_UPS:
        world.set_rule(world.get_location(power_up_name(power_up)), Has(power_up))

    for n in FUNNY_NUMBERS:
        world.set_rule(world.get_location(funny_name(n)), funny_rule(n))

    # Solving N equations needs nothing the starting kit doesn't give, and
    # neither do the shop slots: their Extra Credit comes from those solves.
    world.set_completion_rule(Has("Victory"))
