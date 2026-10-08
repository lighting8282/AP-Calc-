# AP Calc Setup Guide

## Required software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) 0.6.7 or later
- AP Calc for Windows, from the [AP Calc releases page](https://github.com/lighting8282/AP-Calc-/releases):
  extract the zip and run `AP Calc.exe`

The game isn't signed with a certificate, so the first time you run it Windows
may say **"Windows protected your PC"**. Click **More info**, then **Run
anyway**. Only download the zip from the releases page above.

When a newer version is out, the main menu says so beside the version number
in the bottom-left corner, with a link to it. (Settings > Game turns this
check off.) Update the game and `apcalc.apworld` together.

### On Android

The releases page also has `AP-Calc-<version>-Android.apk`, for phones and
tablets running Android 7.1 or later on a 64-bit ARM chip (nearly every device
from the last several years). Open it on the device; Android asks you to allow
your browser or file manager to **install unknown apps** the first time. It
plays in landscape, and Archipelago works the same as on Windows.

Saves stay on the device they were made on: the Android and Windows games
don't share them.

### In a browser (no Archipelago)

A browser version is on the way. Practice, Arcade and the story will all work
there, but it won't be able to join a multiworld: the Archipelago library the
game uses doesn't run in a browser. For Archipelago, use the Windows or
Android version.

## Installing the world

1. Get `apcalc.apworld` from the same releases page.
2. Double-click it, or copy it into Archipelago's `custom_worlds` folder.
3. Edit the release's `AP-Calc.yaml` template, or open the Archipelago
   Launcher and choose **Generate Template Options** to get `AP Calc.yaml`.

## Joining a multiworld

1. Start AP Calc. On the main menu, the note pinned beside the door shows
   which save you're on. Pick an empty save with **Change save** if you like:
   once a save joins a multiworld, it belongs to that seed.
2. Press **Archipelago** on the note.
3. Enter the server address (for example `archipelago.gg:38281`), your slot
   name, and the room's password if it has one, then **Connect**.
4. Close the panel and press **Practice**. Your starting keys are already on
   the calculator.

Items, hints and the room's chat appear in the message panel (bottom right).
If the connection drops, the game keeps trying, and anything you solve while
offline is sent as soon as it's back. Next time you start the game on that
save it reconnects by itself.

## Reporting a problem

While playing (Practice, Arcade or a duel), press Esc for the pause menu, then
**Send feedback**. It opens a GitHub issue
already filled in with the game's version and where you were, and the folder
holding the game's log. Describe what happened, then drag `Player.log` into
the issue (`Player-prev.log` instead if the game crashed: that's the log from
the run before). The log is plain text, so you can open it first and see
what's in it; it can include your server address and slot name.

The log lives in `%USERPROFILE%\AppData\LocalLow\lighting8282\AP Calc`.
The browser and Android versions don't keep one you can get at, so their
issue is filled in the same way, just without a log.

## Playing without a server

Practice, Arcade and the story are the normal game; nothing about
Archipelago touches them unless the save you're on has joined a multiworld.
