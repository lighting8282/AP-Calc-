import unittest

from ..data import (
    ALL_FOUR_OPERATORS, AP_TIER, DIGITS, FUNNY_NUMBERS, HARD_TIER, ITEM_FOR_SYMBOL, ITEM_GROUPS, ITEM_NAME_TO_ID,
    KEY_ITEMS, LOCATION_GROUPS, LOCATION_NAME_TO_ID, MEDIUM_TIER, NO_PLUS_MINUS, OPERATOR_CHECKS, POWER_UPS,
    SPEED_CHECKS, STREAK_CHECKS, VARIETY_CHECKS, VARIETY_KEYS, equation_name, first_use_name, funny_name,
    kit_can_target, power_up_name, shop_name, shop_prices, variety_name,
)
from . import APCalcTestBase


def key(symbol: str) -> str:
    return ITEM_FOR_SYMBOL[symbol]


CHALLENGES = STREAK_CHECKS + SPEED_CHECKS + VARIETY_CHECKS + OPERATOR_CHECKS


class TestDefault(APCalcTestBase):
    def test_location_count(self) -> None:
        names = {loc.name for loc in self.multiworld.get_locations(self.player) if loc.address is not None}
        self.assertEqual(len(names), 50 + len(KEY_ITEMS) + len(POWER_UPS) + len(FUNNY_NUMBERS) + 10 + len(CHALLENGES))
        self.assertIn(equation_name(50), names)
        self.assertNotIn(equation_name(51), names)
        self.assertIn(shop_name(10), names)
        self.assertNotIn(shop_name(11), names)
        for name in CHALLENGES:
            self.assertIn(name, names)

    def test_challenge_slot_data(self) -> None:
        data = self.world.fill_slot_data()
        for flag in ("streak_checks", "speed_checks", "variety_checks", "operator_checks"):
            self.assertEqual(data[flag], 1)

    def test_streaks_and_speed_are_free(self) -> None:
        for name in STREAK_CHECKS + SPEED_CHECKS:
            self.assertTrue(self.can_reach_location(name))

    def test_variety_needs_plus_minus_and_digits(self) -> None:
        # The kit is three digits and one operator: never enough for 10.
        self.assertFalse(self.can_reach_location(variety_name(10)))
        self.collect_by_name(DIGITS + [key("+"), key("-")])
        for n in VARIETY_KEYS:
            self.assertTrue(self.can_reach_location(variety_name(n)))

    def test_operator_checks(self) -> None:
        self.collect_by_name([key("/")])
        self.assertTrue(self.can_reach_location(NO_PLUS_MINUS))
        self.collect_by_name([key("+"), key("-"), key("*")])
        self.assertTrue(self.can_reach_location(ALL_FOUR_OPERATORS))

    def test_shop_is_free_but_paid(self) -> None:
        # Nothing but Extra Credit, which solving earns: reachable from the start.
        for k in range(1, 11):
            self.assertTrue(self.can_reach_location(shop_name(k)))

    def test_shop_prices_in_slot_data(self) -> None:
        prices = self.world.fill_slot_data()["shop_prices"]
        self.assertEqual(len(prices), 10)
        self.assertEqual(prices, sorted(prices))
        self.assertEqual(prices[0], 50)              # one share of 2,750
        self.assertEqual(sum(prices), 50 * 55)
        self.assertTrue(all(p % 5 == 0 for p in prices))

    def test_starting_kit(self) -> None:
        kit = [item.name for item in self.multiworld.precollected_items[self.player]]
        self.assertEqual(len(kit), 4)
        self.assertEqual(sum(name.startswith("Digit ") for name in kit), 3)
        self.assertTrue(any(name != key("0") and name.startswith("Digit ") for name in kit))
        operators = [name for name in kit if name.startswith("Operator ")]
        self.assertEqual(len(operators), 1)
        self.assertIn(operators[0], [key("+"), key("-"), key("*")])
        # Precollected, so not in the pool too.
        pool = [item.name for item in self.multiworld.itempool if item.player == self.player]
        for name in kit:
            self.assertNotIn(name, pool)

    def test_equations_are_free(self) -> None:
        self.assertTrue(self.can_reach_location(equation_name(1)))
        self.assertTrue(self.can_reach_location(equation_name(50)))

    def test_funny_numbers_excluded(self) -> None:
        from BaseClasses import LocationProgressType
        for n in FUNNY_NUMBERS:
            self.assertEqual(self.multiworld.get_location(funny_name(n), self.player).progress_type,
                             LocationProgressType.EXCLUDED)

    def test_power_up_needs_its_item(self) -> None:
        self.assertFalse(self.can_reach_location(power_up_name("Hint")))
        self.collect_by_name(["Hint"])
        self.assertTrue(self.can_reach_location(power_up_name("Hint")))

    def test_sequential_tiers(self) -> None:
        # sin( is Hard: with tier_order sequential it wants Medium too.
        loc = first_use_name(key("sin("))
        self.collect_by_name([key("sin("), key("0"), key("+"), key("-"), HARD_TIER])
        self.assertFalse(self.can_reach_location(loc))
        self.collect_by_name([MEDIUM_TIER])
        self.assertTrue(self.can_reach_location(loc))

    def test_calculus_needs_its_variable(self) -> None:
        loc = first_use_name(key("d/dx("))
        self.collect_by_name([key("d/dx("), key("+"), key("-"), key("*"), MEDIUM_TIER, HARD_TIER, AP_TIER, key("y")])
        self.assertFalse(self.can_reach_location(loc))
        self.collect_by_name([key("x")])
        self.assertTrue(self.can_reach_location(loc))


class TestAnyTierOrder(APCalcTestBase):
    options = {"tier_order": "any"}

    def test_tier_alone(self) -> None:
        loc = first_use_name(key("sin("))
        self.collect_by_name([key("sin("), key("0"), key("+"), key("-"), HARD_TIER])
        self.assertTrue(self.can_reach_location(loc))


class TestSmallestPool(APCalcTestBase):
    # The tightest legal settings: 10 equation checks for 45 required items.
    options = {"goal_count": 20, "equation_checks": "every_other", "trap_chance": 100}

    def test_every_other(self) -> None:
        names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        self.assertIn(equation_name(2), names)
        self.assertNotIn(equation_name(1), names)
        self.assertIn(equation_name(20), names)


class TestMarathon(APCalcTestBase):
    options = {"goal_count": 100, "funny_number_chance": 50, "trap_chance": 0}


class TestDefaultSlotData(APCalcTestBase):
    def test_goal_and_death_link_defaults(self) -> None:
        data = self.world.fill_slot_data()
        self.assertEqual(data["goal"], 0)               # equations
        self.assertEqual(data["card_goal_count"], 25)
        self.assertEqual(data["death_link"], 0)


class TestCardGoal(APCalcTestBase):
    options = {"goal": "cards", "card_goal_count": 40, "death_link": True}

    def test_slot_data(self) -> None:
        data = self.world.fill_slot_data()
        self.assertEqual(data["goal"], 1)
        self.assertEqual(data["card_goal_count"], 40)
        self.assertEqual(data["death_link"], 1)

    def test_victory_needs_nothing(self) -> None:
        # Cards come from Extra Credit, which solving earns.
        self.assertBeatable(True)


class TestBothGoal(APCalcTestBase):
    options = {"goal": "both", "goal_count": 20, "card_goal_count": 5}

    def test_slot_data(self) -> None:
        data = self.world.fill_slot_data()
        self.assertEqual((data["goal"], data["goal_count"], data["card_goal_count"]), (2, 20, 5))
        # Equation checks still follow goal_count.
        names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        self.assertIn(equation_name(20), names)


class TestNoShop(APCalcTestBase):
    options = {"shop_slots": 0}

    def test_no_shop_locations(self) -> None:
        names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        self.assertNotIn(shop_name(1), names)
        self.assertEqual(self.world.fill_slot_data()["shop_prices"], [])


class TestBigShop(APCalcTestBase):
    options = {"shop_slots": 25, "shop_price": 400, "goal_count": 100}

    def test_prices(self) -> None:
        prices = self.world.fill_slot_data()["shop_prices"]
        self.assertEqual(len(prices), 25)
        self.assertEqual(prices, sorted(prices))
        # 100 x 55 x 4 = 22,000, give or take the rounding to 5s.
        self.assertAlmostEqual(sum(prices), 22000, delta=25 * 5)


class TestNoChallenges(APCalcTestBase):
    options = {"streak_checks": False, "speed_checks": False, "variety_checks": False, "operator_checks": False}

    def test_no_challenge_locations(self) -> None:
        names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        for name in CHALLENGES:
            self.assertNotIn(name, names)
        data = self.world.fill_slot_data()
        for flag in ("streak_checks", "speed_checks", "variety_checks", "operator_checks"):
            self.assertEqual(data[flag], 0)


class TestOnlyStreaks(APCalcTestBase):
    options = {"speed_checks": False, "variety_checks": False, "operator_checks": False}

    def test_only_streaks(self) -> None:
        names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        self.assertTrue(set(STREAK_CHECKS) <= names)
        self.assertFalse(set(SPEED_CHECKS + VARIETY_CHECKS + OPERATOR_CHECKS) & names)


class TestGroups(unittest.TestCase):
    def test_item_groups(self) -> None:
        for group, names in ITEM_GROUPS.items():
            self.assertNotIn(group, ITEM_NAME_TO_ID, f"group {group} shadows an item")
            self.assertTrue(names, group)
            self.assertTrue(names <= set(ITEM_NAME_TO_ID), group)
        self.assertEqual(ITEM_GROUPS["Digits"], set(DIGITS))
        self.assertEqual(ITEM_GROUPS["Keys"], set(KEY_ITEMS))
        self.assertEqual(len(ITEM_GROUPS["Operators"]) + len(ITEM_GROUPS["Functions"]), len(KEY_ITEMS) - 10)
        self.assertEqual(ITEM_GROUPS["Calculus"], ITEM_GROUPS["Derivatives"] | ITEM_GROUPS["Integrals"])

    def test_location_groups(self) -> None:
        grouped: set[str] = set()
        for group, names in LOCATION_GROUPS.items():
            self.assertNotIn(group, LOCATION_NAME_TO_ID, f"group {group} shadows a location")
            self.assertTrue(names <= set(LOCATION_NAME_TO_ID), group)
            grouped |= names
        self.assertEqual(grouped, set(LOCATION_NAME_TO_ID))   # every location is in a group


class TestStartingKit(unittest.TestCase):
    def test_kit_can_target(self) -> None:
        self.assertFalse(kit_can_target([5, 7, 9], "+"))   # every sum is over 9
        self.assertFalse(kit_can_target([4, 5, 6], "*"))
        self.assertFalse(kit_can_target([0, 5, 7], "*"))   # 0 isn't a target either
        self.assertTrue(kit_can_target([0, 5, 7], "+"))
        self.assertTrue(kit_can_target([3, 8, 9], "*"))
        self.assertTrue(kit_can_target([5, 7, 9], "-"))

    def test_every_kit_has_a_first_target(self) -> None:
        import random
        from types import SimpleNamespace
        from ..items import choose_starting_kit
        for seed in range(2000):
            kit = choose_starting_kit(SimpleNamespace(random=random.Random(seed)))
            digits = [DIGITS.index(d) for d in kit[:3]]
            self.assertTrue(kit_can_target(digits, kit[3].split(" ", 1)[1]), kit)
            self.assertEqual(len(set(kit)), 4)
            self.assertNotEqual(digits[0], 0)


class TestShopPricesAlone(unittest.TestCase):
    def test_small_shops_cost_the_same_in_total(self) -> None:
        for slots in (1, 3, 5, 10, 25):
            self.assertAlmostEqual(sum(shop_prices(50, slots, 100)), 2750, delta=slots * 5)

    def test_never_free(self) -> None:
        self.assertTrue(all(p >= 5 for p in shop_prices(20, 25, 25)))
