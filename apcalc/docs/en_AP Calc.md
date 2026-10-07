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

## What is the goal?

Solve as many equations as your goal count. Your run carries on afterwards, so
you can still find any checks you missed.

## What other items are there?

- **Hint, Skip, Freebie**: the first of each unlocks that power-up; every copy
  adds one to use.
- **Card Pack** (a free pack in the card shop), **Streak Saver** (your next
  wrong answer keeps your streak), **Extra Credit**, **Pep Talk**, **Confetti**.
- Traps: **Freeze**, **Dessert** (every key becomes a pastry), **Invisibility**,
  **Clear Equation** and **Locked Operator**.
