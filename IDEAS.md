# Feedback Loop — ideas for later

## RNG (brainstorm, 2026-10-20, rev 107)

Principle: input randomness you can play around (choices, previews) is good; output randomness that decides the run
(unlucky spawns, nothing useful offered) feels unfair. Sims show the same persona and build winning 25–100% by seed.

### Where the dice are now
| System | Rolls | Note |
|---|---|---|
| Level-up choices | 3 weighted picks (4 with Setlist): new instrument / notes / tone / passive | input randomness; only rerolls to steer |
| Setlist | songbook shuffle avoiding the last 6 songs | already a shuffle bag |
| Power-ups, requests | independent weighted rolls (Water favoured at low HP) | can repeat; no bad-luck protection |
| Dares | 2–3 of 4 | small pool, pairs repeat |
| Spawns, noise types | time-weighted random | output randomness: decides runs |
| Studio finds | fixed milestones | deliberately not random |

### Ideas
**Agency over the dice**
- Lock and banish at level-up (lock a choice for the next level-up; banish an instrument for the run; Spare Strings could give banishes).
- Preview the next level-up's options after picking an instrument, so builds can be planned.
- Requests offering two power-ups; the side you enter the ring from decides.

**Bad-luck protection**
- Level-up pity: no new instrument offered for 3 level-ups → the next guarantees one.
- Power-up shuffle bag: deal from a shuffled deck of all 10 instead of independent rolls.
- Smooth spawn clusters: cap the same noise type within a short window (the director already smooths difficulty).

**Telegraphing**
- Setlist preview before the show: songs, tempos, and which noise each favours ("SONG 2 · fast, lots of hiss").
- Elites show what they drop before you chase them.

**Run variety**
- Show modifiers: one rolled twist per show, shown up front (crowd cheers only on the backbeat; bass ×2, hats ×0.5; no power-ups but double requests).
- Song events: one per song (power cut: drums only for 8 bars; stage invasion: a swarm, then a big reward).
- Build-defining rare picks that change rules ("every kick also fires a snare"); grooves could sometimes be offered as rewards.

**Fairness**
- Daily show: seed spawns and level-ups too, not only the setlist, so daily scores compare.
- Measure first: sim 50 seeds per persona and log what decided each run (spawn wave, no power-ups, weak offers).

### Suggested order
1. Measure (sim, ~10 min).
2. Lock/banish + level-up pity.
3. Power-up shuffle bag + setlist preview.
4. Show modifiers.

## Playtest swarm (2026-10-24, rev 133)

50 simulated playtesters × ~7 shows each (351 shows, tools/playtest) plus 8 sessions of random keyboard / controller / touch input
through the real menus. No errors, crashes, impossible states or stuck screens. Longest run without a new instrument: 3 level-ups.

Balance flags (win rates; personas differ in more than one way, so these point at where to look, not at exact causes):
- AMBIENT sound: 0 / 49, average level 8, dead after ~9 hits. It halves the noise (so half the XP) and doubles damage both ways. Fixed in rev 135 (25%).
- MAIN STAGE: 2 / 28. DREAM band 13% vs FOUR / SYNTH 42%. 16-BIT 19% vs 8-BIT 49% and RAVE 59%.
- PACKED HOUSE looks like a bonus, not a twist (49%, highest level): the +40% XP outweighs the +40% noise. Twists retuned in rev 135.
- The sim never clips (its loop filler leaves headroom), so clipping is untested by it.
- The same persona still ranges widely in level reached (e.g. 6–28): an early death caps the level.
- Club tracks sounded slow: songbook songs keep their own tempo and 5 of 12 are 72–86 bpm. Fixed in rev 134 (club and Main Stage pick 98+ bpm songs), but that leaves 7 songs for those stages: the songbook needs more uptempo songs.
