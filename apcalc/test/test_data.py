"""The world against the game: names, ids and tiers must match the Unity
tables exactly (unity_tables.json, exported by tools/export_unity_tables.cs)."""

import json
import pathlib
import unittest

from ..data import (
    GAME_NAME, ITEM_NAME_TO_ID, KEY_ITEMS, KEY_TIER, LOCATION_NAME_TO_ID, first_use_name,
)

ROOT = pathlib.Path(__file__).resolve().parent.parent
UNITY = json.loads((pathlib.Path(__file__).parent / "unity_tables.json").read_text(encoding="utf-8"))


class TestAgainstUnity(unittest.TestCase):
    def test_items_match(self) -> None:
        unity = {i["name"]: i["id"] for i in UNITY["items"]}
        self.assertEqual(unity, ITEM_NAME_TO_ID)

    def test_locations_match(self) -> None:
        unity = {loc["name"]: loc["id"] for loc in UNITY["locations"]}
        self.assertEqual(unity, LOCATION_NAME_TO_ID)

    def test_tiers_match(self) -> None:
        unity = {loc["name"]: loc["tier"] for loc in UNITY["locations"] if "tier" in loc}
        self.assertEqual(unity, {first_use_name(item): KEY_TIER[item] for item in KEY_ITEMS})

    def test_ids_unique(self) -> None:
        self.assertEqual(len(set(ITEM_NAME_TO_ID.values())), len(ITEM_NAME_TO_ID))
        self.assertEqual(len(set(LOCATION_NAME_TO_ID.values())), len(LOCATION_NAME_TO_ID))

    def test_manifest_matches(self) -> None:
        manifest = json.loads((ROOT / "archipelago.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["game"], GAME_NAME)
        self.assertTrue((ROOT / "docs" / f"en_{GAME_NAME}.md").is_file())
