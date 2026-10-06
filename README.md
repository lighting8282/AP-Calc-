# AP Calc — Archipelago world

The Archipelago world for **AP Calc**, a Unity calculator game: a target number
appears and you build an equation equal to it from the keys you have. Every
key is an item.

The game itself lives in its own repository (github.com/lighting8282/AP-Calc-BACKUP);
its `APItems.cs` and `APLocations.cs` are the source of truth for item and
location names and ids. `apcalc/data.py` mirrors them, and `test_data` checks
the mirror against `apcalc/test/unity_tables.json`, exported from the game with
`tools/export_unity_tables.cs`.

## Contents

| | |
|---|---|
| `apcalc/` | the world: data, options, items, locations, rules, docs, tests |
| `tools/build_apworld.py` | packages `dist/apcalc.apworld` (reproducible, verified) |
| `tools/export_unity_tables.cs` | run in the Unity editor to refresh `unity_tables.json` |
| `tests/yaml/` | solo and 4-player multiworld yamls for real generations |

## Checks (about N + 44)

- **Equation 1 … N** — N is `goal_count` (20–100); `equation_checks: every_other` halves them
- **First Solve Using <key>** — 34 keys; logic needs the key, its tier, and what it takes to fit it into an answer
- **First Hint / Skip / Freebie Used**
- **Funny Number 67, 69, 420, 666, 777, 1337, 80085** — excluded (filler and traps only)

## Items

Tiers (Medium / Hard / AP Difficulty) and 34 keys are progression; three digits
and one of `+ - *` are precollected as the starting kit. Progressive Magnitude
×6, Progressive Decimal ×2 and Negative Numbers are useful. Hint / Skip /
Freebie: first copy progression, extras filler (Freebie useful). Card Pack and
Streak Saver are useful; Extra Credit, Pep Talk and Confetti are filler; five traps.

## Development

The world is junctioned into the Archipelago source checkout:
`C:\Users\turtl\Archipelago\worlds\apcalc -> A:\Archipelago\Games\AP Calc\apcalc`.
Use that checkout's `.venv`.

    SKIP_REQUIREMENTS_UPDATE=1 python -m unittest discover -s worlds/apcalc/test -t . -p "test_*.py"
    python Generate.py --player_files_path "A:\Archipelago\Games\AP Calc\tests\yaml\multi" --spoiler 2
    python tools/build_apworld.py

## Not done yet

The game's connection to a server (Archipelago.MultiClient.Net in Unity), which
will read `goal_count`, `equation_every`, `tier_order` and
`funny_number_chance` from slot data.
