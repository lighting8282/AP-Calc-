from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range

from .data import MAX_EQUATIONS


class GoalCount(Range):
    """How many equations you solve to finish. Every solve counts, freebies
    included, and your run carries on afterwards for any checks still left."""
    display_name = "Goal Count"
    range_start = 20
    range_end = MAX_EQUATIONS
    default = 50


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


@dataclass
class APCalcOptions(PerGameCommonOptions):
    goal_count: GoalCount
    equation_checks: EquationChecks
    tier_order: TierOrder
    funny_number_chance: FunnyNumberChance
    trap_chance: TrapChance


option_groups = [
    OptionGroup("Goal", [GoalCount, EquationChecks]),
    OptionGroup("Keys and Targets", [TierOrder, FunnyNumberChance]),
    OptionGroup("Extras", [TrapChance]),
]

option_presets = {
    "quick": {"goal_count": 20, "equation_checks": EquationChecks.option_every, "trap_chance": 5},
    "marathon": {"goal_count": MAX_EQUATIONS, "funny_number_chance": 20, "trap_chance": 30},
}
