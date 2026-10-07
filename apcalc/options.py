from dataclasses import dataclass

from Options import Choice, DeathLink, OptionGroup, PerGameCommonOptions, Range

from .data import MAX_EQUATIONS, MAX_SHOP_SLOTS


class Goal(Choice):
    """
    What finishes your run. It carries on afterwards for any checks still left.

    equations: solve goal_count equations
    cards:     collect card_goal_count cards new to your save during the run,
               from packs bought with Extra Credit or Card Pack items
    both:      both of those
    """
    display_name = "Goal"
    option_equations = 0
    option_cards = 1
    option_both = 2
    default = option_equations


class GoalCount(Range):
    """How many equations the equations goal needs (every solve counts,
    freebies included), and how many Equation checks there are, whatever the
    goal."""
    display_name = "Goal Count"
    range_start = 20
    range_end = MAX_EQUATIONS
    default = 50


class CardGoalCount(Range):
    """How many cards the cards goal needs: cards that weren't in your
    collection before, collected during the run. A Standard Pack holds five
    and costs 200 Extra Credit, the same Extra Credit the shop takes."""
    display_name = "Card Goal Count"
    range_start = 5
    range_end = 100
    default = 25


class EquationChecks(Choice):
    """
    Which solves are checks.

    every:       Equation 1, 2, 3 ... up to the goal count
    every_other: Equation 2, 4, 6 ... (half as many, for fewer filler items)
    """
    display_name = "Equation Checks"
    option_every = 1
    option_every_other = 2
    default = option_every


class TierOrder(Choice):
    """
    How the three difficulty items gate keys. A key works once you have both
    its item and its tier's item.

    sequential: logic expects Medium before Hard before AP, so Hard keys are
                only in logic with Medium Difficulty too, and AP keys with all
                three
    any:        each tier stands on its own
    """
    display_name = "Tier Order"
    option_sequential = 0
    option_any = 1
    default = option_sequential


class FunnyNumberChance(Range):
    """Percentage chance a target is a funny number (67, 69, 420, 666, 777,
    1337, 80085) you haven't solved yet, once your keys can build one. These
    checks only ever hold filler or traps, since they're down to luck."""
    display_name = "Funny Number Chance"
    range_start = 0
    range_end = 50
    default = 10


class TrapChance(Range):
    """
    Percentage chance that a filler item is replaced by a trap:

    Freeze:          the keypad freezes over for 30 seconds
    Dessert:         every key shows a dessert instead of its label for 60 seconds
    Invisibility:    your equation is invisible for 60 seconds
    Clear Equation:  your equation is wiped
    Locked Operator: half your operators and functions lock for 60 seconds
    """
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 15


class ShopSlots(Range):
    """How many checks the Archipelago shop sells. You buy them in the card
    shop with Extra Credit earned during the run, and opening the shop hints
    each slot's item to its owner. They can hold anything. 0 turns it off."""
    display_name = "Shop Slots"
    range_start = 0
    range_end = MAX_SHOP_SLOTS
    default = 10


class ShopPrice(Range):
    """What the shop costs, as a percentage. At 100 the whole shop comes to
    about 55 Extra Credit per equation of your goal count (2,750 at the
    default goal of 50), cheapest slot first, so the last one is bought
    around the goal."""
    display_name = "Shop Price"
    range_start = 25
    range_end = 400
    default = 100


class APCalcDeathLink(DeathLink):
    """When you die, everyone who enabled death link dies. Of course, the
    reverse is true too.

    In AP Calc every tenth wrong answer in your run is a death, and a death
    from someone else costs your streak and freezes the keypad for 30
    seconds."""


@dataclass
class APCalcOptions(PerGameCommonOptions):
    goal: Goal
    goal_count: GoalCount
    card_goal_count: CardGoalCount
    equation_checks: EquationChecks
    tier_order: TierOrder
    funny_number_chance: FunnyNumberChance
    trap_chance: TrapChance
    shop_slots: ShopSlots
    shop_price: ShopPrice
    death_link: APCalcDeathLink


option_groups = [
    OptionGroup("Goal", [Goal, GoalCount, CardGoalCount, EquationChecks]),
    OptionGroup("Keys and Targets", [TierOrder, FunnyNumberChance]),
    OptionGroup("Shop", [ShopSlots, ShopPrice]),
    OptionGroup("Extras", [TrapChance, APCalcDeathLink]),
]

option_presets = {
    "quick": {"goal_count": 20, "equation_checks": EquationChecks.option_every, "trap_chance": 5},
    "marathon": {"goal_count": MAX_EQUATIONS, "funny_number_chance": 20, "trap_chance": 30},
}
