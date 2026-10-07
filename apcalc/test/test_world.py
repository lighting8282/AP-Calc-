import unittest

from ..data import (
    AP_TIER, FUNNY_NUMBERS, HARD_TIER, ITEM_FOR_SYMBOL, KEY_ITEMS, MEDIUM_TIER, POWER_UPS, equation_name,
    first_use_name, funny_name, power_up_name, shop_name, shop_prices,
)
from . import APCalcTestBase


def key(symbol: str) -> str:
    return ITEM_FOR_SYMBOL[symbol]


class TestDefault(APCalcTestBase):
    def test_location_count(self) -> None:
        names = {loc.name for loc in self.multiworld.get_locations(self.player) if loc.address is not None}
        self.assertEqual(len(names), 50 + len(KEY_ITEMS) + len(POWER_UPS) + len(FUNNY_NUMBERS) + 10)
        self.assertIn(equation_name(50), names)
        self.assertNotIn(equation_name(51), names)
        self.assertIn(shop_name(10), names)
        self.assertNotIn(shop_name(11), names)

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


class TestShopPricesAlone(unittest.TestCase):
    def test_small_shops_cost_the_same_in_total(self) -> None:
        for slots in (1, 3, 5, 10, 25):
            self.assertAlmostEqual(sum(shop_prices(50, slots, 100)), 2750, delta=slots * 5)

    def test_never_free(self) -> None:
        self.assertTrue(all(p >= 5 for p in shop_prices(20, 25, 25)))
