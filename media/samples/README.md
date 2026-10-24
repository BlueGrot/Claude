# Drum samples

Put sample files in this folder and list them in `manifest.json`. Any voice listed there replaces
the synthesized drum; voices left out stay synthesized. The game loads the files when the audio starts
(it needs to be served over http, as on itch.io or the local preview; opening the html file directly
skips the samples and keeps the synth).

The game starts with an 8-bit chip kit, which is always synthesized. Samples replace the drums of the
hi-fi sound set, which comes with a genre unlock later in the game. The Observatory (ambient stage) keeps
its own soft synthesized kit.

## Voices

| Voice | Used for | Suggested length |
|---|---|---|
| `kick` | kick track, kick ghost notes, Sub Drop | 0.4–0.6 s |
| `snare` | snare track, snare ghost notes, fills into choruses | 0.3–0.5 s |
| `hat` | closed hi-hat (and hat ghost notes) | 0.08–0.2 s |
| `hatOpen` | open hat on the last offbeat of every second bar (choked by the next closed hat) | 0.5–0.8 s |
| `crash` | crash track and chorus downbeats | 2–3 s, faded out |
| `rim` | rim clicks in breakdowns | 0.1–0.2 s |

## Crowd (optional)

Two more voices replace the synthetic crowd that swells with HYPE. Unlike the drums, they work in every sound set.

| Voice | Used for | Suggested length |
|---|---|---|
| `crowd` | the crowd bed: one seamless loop (only the first file of the first layer is used) | 8–20 s, loops cleanly |
| `cheer` | cheers at the end of songs and when the hype is high | 1–3 s each, 4–8 round robins |

Keep them distant and dry-ish (a little room is fine): the game sets them back in its own reverb. Normalize the loop to
about −12 dBFS RMS and the cheers to peak around −3 dBFS; use `gain` to trim.

## How to render them

- **Format:** WAV, 16 or 24 bit, 44.1 or 48 kHz. Mono for kick, snare and rim; stereo is fine for hats and crash.
  Avoid MP3: its encoder padding puts silence in front of the hit.
- **Start on the transient.** No silence before the hit: the game schedules each note sample-accurately.
- **Dry.** No bus compression, limiting or reverb: the game adds its own room, glue compressor and limiter.
  Per-drum EQ and transient shaping are fine.
- **Velocity layers:** 3–4 per voice, soft to hard, rendered at their real dynamics. Do not normalize the layers
  separately; normalize each voice as a whole so its hardest hit peaks around −1 dBFS.
  Ghost notes always use the softest layer; every other note picks its layer by how hard it is played.
- **Round robins:** 3–4 per layer. They are played in rotation, with a touch of random level and pitch on top.

Roughly 6 voices × 4 layers × 4 round robins is about 100 files and ~6 MB as 24-bit mono WAV.

## manifest.json

```json
{
  "voices": {
    "kick":    { "rootHz": 50, "gain": 1.0,
                 "layers": [["kick_v1_rr1.wav", "kick_v1_rr2.wav", "kick_v1_rr3.wav"],
                            ["kick_v2_rr1.wav", "kick_v2_rr2.wav", "kick_v2_rr3.wav"],
                            ["kick_v3_rr1.wav", "kick_v3_rr2.wav", "kick_v3_rr3.wav"]] },
    "snare":   { "layers": [["snare_v1_rr1.wav", "snare_v1_rr2.wav"], ["snare_v2_rr1.wav", "snare_v2_rr2.wav"]] },
    "hat":     { "gain": 0.8, "layers": [["hat_v1_rr1.wav"], ["hat_v2_rr1.wav"], ["hat_v3_rr1.wav"]] },
    "hatOpen": { "layers": [["hatopen_rr1.wav", "hatopen_rr2.wav"]] },
    "crash":   { "layers": [["crash_rr1.wav", "crash_rr2.wav"]] },
    "rim":     { "layers": [["rim_rr1.wav"]] }
  }
}
```

- `layers`: soft to hard; each layer is a list of round robins.
- `gain` (optional): level trim for the voice; 1 = as rendered.
- `rootHz` (kick only, optional): the pitch of the kick's tail. If you give it, the kick is re-pitched
  to the song's key the way the synth kick is (it lands between E1 and A#1, so stay within a few semitones of that).
  Leave it out to play the kick at its own pitch.

A voice whose files fail to load is skipped (with a warning in the browser console) and stays synthesized.
