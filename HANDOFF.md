# Feedback Loop: handoff (2026-10-24, rev 131 → 144)

For a local Claude Code session picking up from a cloud session.

## Where the code is

- Repo `BlueGrot/Claude`, branch `claude/youthful-noether-7j5pwa` (no PR opened). The game is at the repo root:
  `index.html` (the whole game, one file), `CHANGELOG.md`, `IDEAS.md`, `tools/`, `media/`, `revisions/`.
- **Your local folder (`~/dev/feedback-loop`) is probably still at r131.** Bring it up to date before working:
  clone the branch, or copy `index.html`, `CHANGELOG.md`, `IDEAS.md` and `tools/` over from it. Check `REV` in
  `index.html`: it should read 144.
- History is in git now, one commit per revision. New snapshots in `revisions/` are optional.
- The live build is the claude.ai artifact https://claude.ai/artifact/BLiDjnXhNtnZ95Stmov38P (rev 144). To update it:
  `python3 tools/build_hosted.py out.html`, then publish `out.html` to that URL.

## Conventions (unchanged)

- Bump `REV` in `index.html` and add a row at the top of `CHANGELOG.md` with every change.
- Comment density and style: match the surrounding code (dense one-liners, a trailing `//` comment saying why).
- **Gotcha found tonight:** a `//` comment followed by code on the same line silently disables that code (`...playingfor(`).
  Two of these had muted the title theme and the controller pick. Keep a line break after every trailing comment.

## What changed tonight (rev 132–144)

| Rev | Change |
|---|---|
| 132 | Power-ups dealt from a shuffled deck; level-up pity (3 level-ups with no new instrument guarantees one) |
| 133 | Setlist screen before each show (from show 2); song "leans" (each song favours one noise); 5 show twists from show 7; controller dare labels LB/RB/LT |
| 134 | Club and Main Stage pick only 98+ bpm songbook songs (about 40% of club songs used to be slow ballads) |
| 135 | Ambient sound winnable (`AMB_K`: XP ×2, noise HP ×0.5, damage ×1.25, 0.65× ramp clock); twists retuned |
| 136 | Every power-up changes the sound (echo delay, hall, presence, air, gulp, riser); power-up effect stage after the master low-pass |
| 137 | Beat presses ignored during TAPE STOP; a PERFECT press gives one invincible frame (`P.perf`) |
| 138 | Drop-ready orb glows gold and trembles; THE DROP / SUB DROP use `AU.bigBoom` (saturated sine sub, audible on phones) |
| 139 | New fast venues THE WAREHOUSE (140–150 bpm) and THE STADIUM (160–172); sounds unlock slow to fast (Ambient, Vaporwave, 16-bit, Rave, Trance); slow sounds play fewer songs on fast stages |
| 140–142 | Quiet break layer on the fast stages; Breakbeat groove gives kick and snare +40% there |
| 143 | Fix: the title theme was silent (comment swallowed `themeFade`'s loop) |
| 144 | 16-bit ALIAS lands 220+ px away, with a warning ring; rave tracks match venue length, sing only in breakdowns, scramble the loop after breakdowns |

## Balance testing (tools/playtest, tools/sim.js)

Serve the folder (`python3 -m http.server 8765`), then from `tools/playtest/`:

- **Sweep:** `swarm.js` (50 personas, `personas.js`) plus `monkey.js` (random keyboard, controller and touch through the menus).
  `summary.py` reports bugs first, then win rates. See `tools/playtest/README.md`.
- **Like-for-like:** `compare_cfgs.js` builds batches of the same 10 playtesters with one factor varied. Run them with
  `batch.js <port> <cfgs.json> <out.jsonl> <worker> <workers> [setup js]` and read them with `by_tag.py`.
  **Use this for balance decisions.** The sweep confounds factors: it made Main Stage and Dream Pop look broken when they weren't.
- `sim.js` cfg options added tonight: `twist`, `pref` (note placement), `loop` (lock 16ths on or off), and telemetry
  (`dry`, `pu`, `grooveF`, `hitBy`, `bad`).
- Noise: the same batch rerun swings about ±10 points in win rate at n=40. Only trust larger gaps.
- Careful with `pkill -f <pattern>`: if the pattern also appears in your own shell command, it kills that shell.

## Current balance (controlled sims, 40 shows a row)

- Sounds at the Club: 8-bit about 20%, 16-bit 18%, Rave 20%, Trance 12–15%, Ambient about 25% (earlier test).
- Venues for late-game players: Main Stage 18%, Warehouse 12%, Stadium 5%.
- Bands at the Club: Solo 10%, Rhythm 12%, Dream 15%, Synth 18%.
- Twists vs none (about 27%): END NIGHT 15%, HOT CROWD 25%, PACKED HOUSE 32%, ROADIE 28%, NO MONITORS 22%.

## Open items / next steps

1. **Polish before release** (your call: the market is full of AI slop, so it ships polished). Suggested: a first-hour
   onboarding pass with a new player, and a feel pass on the new screens (setlist screen, twists, drop glow).
2. **Listen to tonight's audio.** Everything new was measured, not heard: power-up effects, `bigBoom`, the break layer.
   Levels are single numbers in `AU.fx`, `AU.bigBoom` and the break layer in `scheduleAudio`.
3. **More uptempo songs in the songbook** (`tools/songbook.py` / `songbook.json`): the Club and Main Stage rotate only 7 (98+ bpm).
4. Breakbeat bonus matters at the Warehouse (10% vs 2% wins) but barely at the Stadium. Optional: scale it up there.
5. The sim never clips (its loop filler leaves headroom), so clipping balance is untested.
6. Ideas not done: lock/banish at level-up, real drum & bass breakbeat patterns (the drums are always the player's loop).
