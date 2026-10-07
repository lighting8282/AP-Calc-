from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location, LocationProgressType, Region

from . import items
from .data import (
    FUNNY_NUMBERS, GAME_NAME, KEY_ITEMS, LOCATION_NAME_TO_ID, POWER_UPS, equation_name, first_use_name, funny_name,
    power_up_name, shop_name,
)

if TYPE_CHECKING:
    from .world import APCalcWorld


class APCalcLocation(Location):
    game = GAME_NAME


def equation_numbers(world: APCalcWorld) -> list[int]:
    """Which Equation n checks exist: up to the goal, every one or every other."""
    step = int(world.options.equation_checks)
    return [n for n in range(step, int(world.options.goal_count) + 1, step)]


def create_regions_and_locations(world: APCalcWorld) -> None:
    # One room: everything happens at the calculator. Rules sit on the
    # locations themselves (rules.py).
    menu = Region("Menu", world.player, world.multiworld)
    calc = Region("Calculator", world.player, world.multiworld)
    world.multiworld.regions += [menu, calc]
    menu.connect(calc, "Pick Up The Calculator")

    names = [equation_name(n) for n in equation_numbers(world)]
    names += [first_use_name(item) for item in KEY_ITEMS]
    names += [power_up_name(p) for p in POWER_UPS]
    # Bought with Extra Credit, which every solve earns: always reachable,
    # just paid for, so they take any item.
    names += [shop_name(k) for k in range(1, int(world.options.shop_slots) + 1)]
    calc.add_locations({n: LOCATION_NAME_TO_ID[n] for n in names}, APCalcLocation)

    # Funny numbers turn up by chance, so they may only hold filler or traps.
    calc.add_locations({funny_name(n): LOCATION_NAME_TO_ID[funny_name(n)] for n in FUNNY_NUMBERS}, APCalcLocation)
    for n in FUNNY_NUMBERS:
        world.get_location(funny_name(n)).progress_type = LocationProgressType.EXCLUDED

    # The goal: the game reports it when the run's count reaches goal_count.
    calc.add_event("Goal Count Reached", "Victory", location_type=APCalcLocation, item_type=items.APCalcItem)
