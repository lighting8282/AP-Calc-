# AP Calc

## What is this game?

AP Calc is a calculator puzzle game. A target number appears, and you build an
equation that equals it out of the calculator's keys: for a target of 20,
`4*5` or `19+1`. Typing the number itself doesn't count.

## What does randomization do to this game?

Every key is an item. You start with three digits and one operator, and the
rest — the other digits, `+ - * /`, brackets, powers, square roots, trig,
logarithms, variables and calculus — arrive from the multiworld. A key also
needs its difficulty tier (Medium, Hard or AP Difficulty) before it works.

When a key becomes usable, a note by the calculator says what it does, with an
example such as `sqrt(81) = 9`, and a button to the cheat sheet page that
covers it.

Targets are always built from keys you have, so you can always solve the one
in front of you. Other items change the targets themselves:

- **Progressive Magnitude** lets targets grow by a digit, up to seven digits.
- **Progressive Decimal** allows one, then two decimal places.
- **Negative Numbers** lets targets go below zero.
- Once you have AP Difficulty and a variable, some targets become simple
  algebra such as `3x^2`.

## What are the checks?

- **Equation 1 … N**: every solve up to your goal count (or every other one).
- **First Solve Using …**: the first correct answer that uses each of the 34
  keys.
- **First Hint / Skip / Freebie Used.**
- **Funny Numbers**: 67, 69, 420, 666, 777, 1337 and 80085 sometimes appear as
  targets once you can build them. These only hold filler or traps.
- **Shop Item 1 … N**: the Archipelago shop, a note on the card shop's board
  during a run. Each slot is a check bought with Extra Credit, cheapest first.
  Only Extra Credit earned during the run counts (solves and Extra Credit
  items), so a save that already had some can't buy the shop out on day one.
  Opening the shop shows what each slot holds and hints it to its owner. The
  `shop_slots` option sets how many (default 10, 0 for none) and `shop_price`
  scales the prices: at 100% the whole shop costs about 55 Extra Credit per
  equation of your goal.
- **Challenges**, each kind with its own option, all on by default:
  - `streak_checks`: **Streak Of 5, 10 and 25** correct answers in a row.
  - `speed_checks`: **Solve In Under 10 Seconds**, and **Under 5**, from the
    target appearing. Any target counts, so you can wait for an easy one.
  - `variety_checks`: **Solve Using 6, 8 and 10 Different Keys** in one
    answer. Padding counts: `+7-7` adds two keys.
  - `operator_checks`: **Solve Without + Or -**, and **Solve Using + - * And /**
    in one answer.

  Freebies don't count for these, though they keep a streak going.

Locations are grouped (Equations, First Uses, Funny Numbers, Shop, Streaks,
Speed, Variety, Operator Challenges) for options like `exclude_locations`.

## What is the goal?

The `goal` option picks one:

- **equations** (default): solve as many equations as your goal count.
- **cards**: collect `card_goal_count` cards that are new to your save during
  the run. Packs cost Extra Credit in the card shop, the same Extra Credit the
  Archipelago shop takes, and Card Pack items open one for free.
- **both**: the equations and the cards.

Your run carries on afterwards, so you can still find any checks you missed.

## Is there DeathLink?

Yes, with `death_link: true`. A run has no health, so every tenth wrong answer
is a death for everyone linked, and a death from someone else costs your
streak and freezes the keypad for 30 seconds.

## Can I chat or use commands in the game?

While connected, the message panel has a line for typing: chat goes to the
room, and server commands such as `!hint Digit 7` work as in the Text Client.

Items come in groups too, so `!hint Digits` hints every digit at once. The
groups: Keys, Digits, Operators, Basic Operators, Functions, Trig, Logarithms,
Variables, Derivatives, Integrals, Calculus, Easy Keys, Medium Keys, Hard Keys,
AP Keys, Difficulties, Target Range, Power-Ups, Extra Credit and Traps. They
work in `start_inventory` and plando as well.

## What other items are there?

- **Hint, Skip, Freebie**: the first of each unlocks that power-up; every copy
  adds one to use.
- **Card Pack** (a free pack in the card shop), **Streak Saver** (your next
  wrong answer keeps your streak), **Extra Credit**, **Pep Talk**, **Confetti**.
- Traps: **Freeze**, **Dessert** (every key becomes a pastry), **Invisibility**,
  **Clear Equation** and **Locked Operator**.

## Accessibility

Settings > Accessibility has a larger text size, two readable fonts (Atkinson
Hyperlegible and OpenDyslexic), blue and orange in place of green and red for
right and wrong, and reduced motion. They apply to every save.
