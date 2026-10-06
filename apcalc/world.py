from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World

from . import items, locations, rules, web_world
from . import options as apcalc_options
from .data import GAME_NAME, ITEM_NAME_TO_ID, LOCATION_NAME_TO_ID


class APCalcWorld(World):
    """
    AP Calc is a calculator game: a number appears, and you build an equation
    that equals it from the keys you have. In Archipelago every digit,
    operator and function is an item, so you start with three digits and one
    operator and build up to calculus, solving your way to the goal.
    """

    game = GAME_NAME
    web = web_world.APCalcWebWorld()

    options_dataclass = apcalc_options.APCalcOptions
    options: apcalc_options.APCalcOptions

    item_name_to_id = ITEM_NAME_TO_ID
    location_name_to_id = LOCATION_NAME_TO_ID

    def create_regions(self) -> None:
        locations.create_regions_and_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.APCalcItem:
        return items.create_item(self, name)

    def get_filler_item_name(self) -> str:
        return items.plain_filler_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        # What the game needs from the seed. The starting kit isn't here: it's
        # precollected, so the server sends it as the first received items.
        return {
            "goal_count": int(self.options.goal_count),
            "equation_every": int(self.options.equation_checks),
            "tier_order": int(self.options.tier_order),
            "funny_number_chance": int(self.options.funny_number_chance),
        }
